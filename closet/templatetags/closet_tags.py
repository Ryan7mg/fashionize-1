from django import template
from closet.models import Clothing

register = template.Library()


@register.inclusion_tag('partials/closet_list_partial.html', takes_context=True)
def closet_list(context):
    request = context['request']
    user = request.user
    clothing_type = request.GET.get('type', '')
    sort = request.GET.get('sort', 'created')

    if clothing_type:
        clothings = Clothing.objects.filter(owner=user, type=clothing_type)
        type_name = clothing_type
    else:
        # when type is empty return all cloth
        clothings = Clothing.objects.filter(owner=user)
        type_name = 'Cloth'

    if sort == 'name':
        clothings = clothings.order_by('name')
    else:
        clothings = clothings.order_by('-created_at')

    return {
        'clothings': clothings,
        'current_type': clothing_type,
        'type_name': type_name,
        'sort': sort,
        'current_sort': sort,
    }



