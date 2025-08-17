
from django.http import HttpResponse
# from django.contrib import redirects
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages


from table.models import SubmittedItem

import logging

from django.shortcuts import get_object_or_404, redirect
from table.models import orders
logger = logging.getLogger(__name__)
from table.models import SubmittedItem
from collections import defaultdict

from django.db.models import Sum
from kitchen.views import kitchen_home

def counter_home(request):
    confirmed_orders = SubmittedItem.objects.filter(status='confirmed').order_by('tableNumber')

    # Group orders by table number and aggregate item quantities
    orders_by_table = {}
    table_totals = {}

    for order in confirmed_orders:
        table_number = order.tableNumber
        
        if table_number not in orders_by_table:
            orders_by_table[table_number] = {}
            table_totals[table_number] = 0
        
        item_name = order.name  # Assuming 'item' is a ForeignKey and 'name' is the field
        item_quantity = order.quantity
        item_price = order.price  # Assuming 'price' is the price for a single unit

        # Calculate total price for this item (quantity * price)
        total_item_price = item_quantity * item_price

        # If the item already exists for the table, add the quantity and price; otherwise, set it
        if item_name in orders_by_table[table_number]:
            orders_by_table[table_number][item_name]['quantity'] += item_quantity
            orders_by_table[table_number][item_name]['total_price'] += total_item_price
        else:
            orders_by_table[table_number][item_name] = {
                'quantity': item_quantity,
                'price': item_price,
                'total_price': total_item_price  # Store the total price (quantity * price)
            }
        
        # Update the total bill for the table
        table_totals[table_number] += total_item_price

    context = {
        'confirmed_orders': orders_by_table,
        'table_totals': table_totals,
    }

    return render(request, 'counter/counter_home.html', context)





def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('counter_home')
        else:
            messages.error(request,'Invalid user or password..')
            return render(request,'counter/login.html')
    return render(request,"counter/login.html")

def logout_view(request):
    logout(request)
    return login_view(request)







def menu(request):
    return render(request,'counter/menu.html')

def tableList1(request):
    tab=request.GET.get('tab','recent')
    table_numbers =range(1,16)  # Example: Replace with your logic to get table numbers
    if tab == 'all':
        template_name = 'counter/tableList.html'
        context = {'table_numbers': table_numbers}
    else:
        template_name = 'counter/counter_home.html'
        context = {'table_numbers': table_numbers}

    return render(request, template_name, context)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def get_table_receipt(request, table_number):
    # print(f"Table number requested: {table_number}")
    receipt_data = {
        "1": {
            "customer_name": "John Doe",
            "order_no": "1",
            "date": "15th September 2024",
            "items": [
                {"item": "Grilled Chicken", "qty": 2, "price": "$10.00", "total": "$20.00"},
                {"item": "French Fries", "qty": 1, "price": "$05.00", "total": "$05.00"},
                {"item": "Soda", "qty": 2, "price": "$03.00", "total": "$06.00"},
            ],
            "subtotal": "$31.00",
            "tax": "$2.48",
            "total": "$33.48"
        },
        "2": {
            "customer_name": "Jane Smith",
            "order_no": "789012",
            "date": "16th September 2024",
            "items": [
                {"item": "Burger", "qty": 1, "price": "$8.00", "total": "$8.00"},
                {"item": "Salad", "qty": 1, "price": "$6.00", "total": "$6.00"},
                {"item": "Juice", "qty": 1, "price": "$4.00", "total": "$4.00"},
            ],
            "subtotal": "$18.00",
            "tax": "$1.44",
            "total": "$19.44"
        }
        # Add more table numbers as needed
    }

    # Fetch data based on table_number or return an error if not found
    data = receipt_data.get(str(table_number), {
        "error": "No data found for this table number."
    })

    return JsonResponse(data)




from .models import SubmittedItem

def generate_bill(request, table_number):
    # Get all confirmed items for the specific table
    confirmed_items = SubmittedItem.objects.filter(tableNumber=table_number, status='confirmed')

    # Dictionary to store item names and their aggregated quantity and total price
    order_summary = defaultdict(lambda: {'quantity': 0, 'total_price': 0})

    # Aggregate items by name
    for item in confirmed_items:
        if item.name in order_summary:
            order_summary[item.name]['quantity'] += item.quantity
            order_summary[item.name]['total_price'] += item.total_price
        else:
            order_summary[item.name]['quantity'] = item.quantity
            order_summary[item.name]['total_price'] = item.total_price

    # Prepare data to return as JSON
    orders = [
        {
            'item_name': item_name,
            'quantity': details['quantity'],
            'price': details['total_price'] / details['quantity'],  # Average price per item
            'total_price': details['total_price']
        }
        for item_name, details in order_summary.items()
    ]

    # Calculate total bill amount
    total_amount = sum(item['total_price'] for item in orders)

    # Return the response as JSON
    data = {
        'orders': orders,
        'total_amount': total_amount
    }

    return JsonResponse(data)

from django.shortcuts import render
from .models import SubmittedItem

def recent_tables_view(request):
    # Get the recent submitted items (bills) sorted by creation time
    recent_tables = SubmittedItem.objects.filter(status='confirmed').order_by('-created_at')[:10]  # Get the last 10 confirmed orders

    context = {
        'recent_tables': recent_tables,
    }
    return render(request, 'counter/counter_home.html', context)
def generate_bill_view(request, table_number):
    # Fetch the submitted items for the specific table number
    submitted_items = SubmittedItem.objects.filter(tableNumber=table_number, status='confirmed')
    
    context = {
        'submitted_items': submitted_items,
        'table_number': table_number,
    }
    return render(request, 'counter/bill_view.html', context)

from django.views.decorators.http import require_http_methods


@require_http_methods(["DELETE"])
def delete_table_orders(request, table_number):
    # Get all confirmed items for the specific table and delete them
    confirmed_items = SubmittedItem.objects.filter(tableNumber=table_number, status='confirmed')
    
    if confirmed_items.exists():
        confirmed_items.delete()  # Delete all items for this table
        return JsonResponse({'message': 'Orders deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'No orders found for this table'}, status=404)
