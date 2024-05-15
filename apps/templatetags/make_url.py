from django.template import Library

register = Library()


@register.filter()
def make_url(request, page):
    result = '?'
    category_id = request.GET.get('category')
    if category_id:
        result += f'category={category_id}&'
    if page:
        result += f'page={page}'

    return result
#
#
# @register.filter()
# def get_query_params(value: dict, arg: str):
#     return int(value.get(arg))
