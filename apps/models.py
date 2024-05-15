from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextField, ImageField, ForeignKey, CASCADE, DateTimeField, \
    ManyToManyField, URLField, SmallIntegerField, BooleanField, DecimalField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    image = ImageField(null=True)


class Category(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Blog(Model):
    image = ImageField()
    title = CharField(max_length=100)
    description = TextField()
    user = ForeignKey('apps.User', CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    category = ForeignKey('apps.Category', CASCADE)
    tag = ManyToManyField('apps.Tag', related_name='products')

    def __str__(self):
        return self.title


class Comment(Model):
    body = TextField()
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Blog', CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Worker(Model):
    name = CharField(max_length=100)
    image = ImageField(null=True, blank=True)
    profession = CharField(max_length=100)
    website = URLField(max_length=100, null=True)
    facebook = URLField(max_length=100, null=True, blank=True)
    twitter = URLField(max_length=100, null=True, blank=True)
    linkedin = URLField(max_length=100, null=True, blank=True)
    google = URLField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('worker')
        verbose_name_plural = _('workers')


class Product(Model):
    image = ImageField()
    title = CharField(max_length=100)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    rating = SmallIntegerField()
    is_stock = BooleanField(default=False)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class WishList(Model):
    product = ForeignKey('apps.Product', CASCADE)
    user = ForeignKey('apps.User', CASCADE)
    created_at = DateTimeField(auto_now_add=True)
