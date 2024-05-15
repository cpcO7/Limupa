from django.template import Library
from apps.models import WishList

register = Library()


@register.filter()
def check_like(request, pk) -> bool:
    if not request.user.is_anonymous:
        return WishList.objects.filter(user=request.user, product_id=pk).exists()
    else:
        pass
