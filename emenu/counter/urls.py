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
# from .views import CounterLogin, Counter/


urlpatterns = [
    path('counter/',views.counter_home,name='counter_home'),
    path('',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),

    path('bill/<int:table_number>/', views.generate_bill, name='generate_bill'),
    path('delete_orders/<int:table_number>/', views.delete_table_orders, name='delete_table_orders'),

    path('recent_tables/', views.recent_tables_view, name='recent_tables'),  # No parameters
    # path('generate_bill/<int:table_number>/', views.generate_bill, name='generate_bill'),


    path('menu/',views.menu,name='menu'),
    path('tableList1/', views.tableList1, name='tableList1'),
    # path('tableList/',views.table_view,name='table_view'),
    path('api/get_table_receipt/<int:table_number>/', views.get_table_receipt, name='get_table_receipt'),
    path('orders/', views.counter_home, name='view_orders'),
]
