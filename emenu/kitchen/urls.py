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
from django.urls import path
from . import views
urlpatterns = [
    path('',views.kitchen_home,name='kitchen_home'),
    path('tableList/', views.tableList, name='tableList'),
    path('api/get_table_receipt/<int:table_number>/', views.get_table_receipt, name='get_table_receipt'),

    path('orders/', views.kitchen_home, name='view_orders'),
    path('confirm-order/<int:table_number>/', views.confirm_order, name='confirm_order'),
    path('confirm_all_orders/<int:table_number>/', views.confirm_all_orders, name='confirm_all_orders'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order')


]
