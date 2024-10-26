

# table/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('booking/',views.booking , name="booking"),
    path('bill/', views.bill, name='bill'),
    path('order/', views.order, name='order'),
    path('about/',views.about , name='about'),
    path('contact/',views.contact , name="contact"),
    path('testimonial/',views.testimonial , name="testimonial"),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('submit-order-final/', views.submit_order, name='submit_order_final'),
    path('add_not_submitted_item/', views.add_not_submitted_item, name='add_not_submitted_item'),
    path('table/cancel_item/<int:item_id>/', views.cancel_item, name='cancel_item'),
   path('table/cancel_item_finish/', views.cancel_item_finish, name='cancel_item_finish'),
    path('add_to_submitted_item/', views.add_to_submitted_item, name='add_to_submitted_item'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('submit_all/', views.submit_all_items, name='submit_all_items'),
    path('set_table_number/', views.set_table_number, name='set_table_number'),
    # path('generate_qr/', views.generate_qr, name='generate_qr'),
    # path('auto_submit/<int:item_id>/', views.auto_submit_item, name='auto_submit_item'),
    path('submit_item/<int:item_id>/', views.submit_item, name='submit_item'),


]

