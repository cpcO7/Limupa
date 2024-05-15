from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.views import ShopLeftSideBar, BlogDetailsLeftSidebar, RegisterCreateView, BlogCommentCreateView, \
    WishlistView, ShopView, ProductDetailView, AboutUsView, check_view, nimadir

urlpatterns = [
    path('', ShopLeftSideBar.as_view(), name='home_page'),
    path('detail/<int:pk>', BlogDetailsLeftSidebar.as_view(), name='detail_page'),
    path('blog-comment', BlogCommentCreateView.as_view(), name='blog_comment'),
    path('wishlist', WishlistView.as_view(), name='wishlist_page'),
    path('shop', ShopView.as_view(), name='shop_page'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_page'),
    path('about-us', AboutUsView.as_view(), name='about_us_page'),
    path('con', check_view, name='about_us_page'),
    path('liked/<int:pk>', nimadir, name='nimadir'),

    path('login-register', RegisterCreateView.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='home_page'), name='logout_page'),
    path('login-register/', LoginView.as_view(
        template_name='apps/login-register.html',
        next_page='home_page',
        redirect_authenticated_user=True
    ), name='login'),
]
