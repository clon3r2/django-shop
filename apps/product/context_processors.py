from .models import Category


def category(request):
    cats = Category.objects.filter(parent__isnull=True).exclude(children__isnull=True)
    return {'cats': cats}
