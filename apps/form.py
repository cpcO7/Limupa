from django.contrib.auth.hashers import make_password
from django.forms import ModelForm, ModelChoiceField

from apps.models import Comment, Blog, User


class RegisterModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'password', 'email']

    def clean_password(self):
        return make_password(self.cleaned_data.get('password'))

    # def is_valid(self):
    #     return super().is_valid()
    #
    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))


class BlogCommentModelForm(ModelForm):
    product = ModelChoiceField(queryset=Blog.objects.all())

    class Meta:
        model = Comment
        fields = ['body', 'product']
