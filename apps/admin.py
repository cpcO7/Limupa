from django.contrib import admin
from django.contrib.auth.models import User, Group

from apps.models import Blog, Category, Tag, Comment, Worker, Product


@admin.register(Blog)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
