# common/context_processors/menu_context.py

from .models import SettingMenus
from administration.models import CompanyWebsite

def menu_context(request):
    try:
        company = CompanyWebsite.objects.get(url=request.META['HTTP_HOST']).company.name 
        nv1menus = SettingMenus.objects.filter(cat__company__name=company, cat__application="common", index=0).all()
    except:
        nv1menus = None

    return {
        'nv1menus': nv1menus,
    }
