"""
URL configuration for emenu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
#   
    path('', views.home, name='home'),   # 👈 Landing page
     path('clear_table/<int:table_number>/', views.clear_table_session, name='clear_table'),
#  
# >>>>>>>  
    path('<int:id>/', views.table_home, name='table_home'),
    # path('', views.home, name='home'),
    path('',views.generate_qr,name='generate_qr'),
    path('table_home/',views.table_home,name='table_home'),
    path('admin/',admin.site.urls),
    path('counter/',include('counter.urls')),
    path('kitchen/',include('kitchen.urls')),
    path('table/',include('table.urls')),
    path('remove_order_item/',views.remove_order_item,name='remove_order_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
