import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView

from apps.form import RegisterModelForm, BlogCommentModelForm
from apps.models import Blog, Tag, Category, Comment, Worker, Product, WishList
from apps.task import send_to_user_email


class ShopLeftSideBar(ListView, LoginRequiredMixin):
    queryset = Blog.objects.all().order_by('id')
    template_name = 'apps/blog-list-left-sidebar.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        tag = self.request.GET.get('tag')
        if category:
            queryset = queryset.filter(category__name=category)
        if tag:
            queryset = queryset.filter(tag__name=category)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = super().get_context_data(object_list=object_list, **kwargs)
        queryset['categories'] = Category.objects.prefetch_related('blog_set').annotate(blog_count=Count('blog__id'))
        queryset['tags'] = Tag.objects.all()
        queryset['categories'] = Category.objects.all()

        queryset['january'] = Blog.objects.filter(created_at__month=1, created_at__year=2024).count()
        queryset['february'] = Blog.objects.filter(created_at__month=2, created_at__year=2024).count()
        queryset['march'] = Blog.objects.filter(created_at__month=3, created_at__year=2024).count()
        queryset['april'] = Blog.objects.filter(created_at__month=4, created_at__year=2024).count()
        return queryset


class BlogDetailsLeftSidebar(DetailView):
    queryset = Blog.objects.all()
    template_name = 'apps/blog-details-left-sidebar.html'
    context_object_name = 'blog'

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = super().get_context_data(object_list=object_list, **kwargs)
        queryset['tags'] = Tag.objects.all()
        queryset['categories'] = Category.objects.all()

        queryset['january'] = Blog.objects.filter(created_at__month=1, created_at__year=2024).count()
        queryset['february'] = Blog.objects.filter(created_at__month=2, created_at__year=2024).count()
        queryset['march'] = Blog.objects.filter(created_at__month=3, created_at__year=2024).count()
        queryset['april'] = Blog.objects.filter(created_at__month=4, created_at__year=2024).count()
        return queryset


_code = []


def check_view(request):
    code = request.GET.get('confirm')
    global _code
    if code == _code[-1]:
        _code = []
        return HttpResponseRedirect('')
    else:
        return HttpResponseRedirect('login-register')


class RegisterCreateView(CreateView):
    form_class = RegisterModelForm
    template_name = 'apps/login-register.html'
    success_url = 'login-register'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            code = uuid.uuid4()
            global _code
            _code.append(code.urn.split(':')[-1])
            ip_address = request.META['HTTP_HOST'].split(':')[0]
            confirmation_link = f"http://{ip_address}:8000/con?confirm={code}"

            send_to_user_email.delay(form.cleaned_data['email'], confirmation_link)

            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class BlogCommentCreateView(CreateView):
    model = Comment
    form_class = BlogCommentModelForm
    success_url = '/'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)


class WishlistView(ListView):
    queryset = WishList.objects.all().order_by('-created_at')
    template_name = 'apps/wishlist.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = super().get_context_data(object_list=object_list, **kwargs)
        product_pks = WishList.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        queryset['liked_products'] = Product.objects.filter(pk__in=product_pks)

        return queryset


class ShopView(ListView):
    queryset = Product.objects.all().order_by('id')
    template_name = 'apps/shop-left-sidebar.html'
    context_object_name = 'products'
    paginate_by = 9


class ProductDetailView(DetailView):
    queryset = Product.objects.all().order_by('id')
    template_name = 'apps/single-product.html'
    context_object_name = 'product'


class AboutUsView(ListView):
    queryset = Worker.objects.all().order_by('id')
    template_name = 'apps/about-us.html'
    context_object_name = 'workers'


def nimadir(request, pk):
    if not request.user.is_anonymous:
        product = Product.objects.filter(pk=pk).first()
        favo, created = WishList.objects.get_or_create(product=product, user=request.user)
        if not created:
            favo.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('register')
