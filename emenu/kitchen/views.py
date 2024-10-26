
from django.http import HttpResponse
# from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from table.models import SubmittedItem

from table.models import orders




# def kitchen_home(request):
#     pending_orders = SubmittedItem.objects.filter(status='pending').order_by('table_number')
#     tables_with_orders = {}
    
#     for order in pending_orders:
#         table_number = order.table_number
#         if table_number not in tables_with_orders:
#             tables_with_orders[table_number] = []
#         tables_with_orders[table_number].append(order)
#     confirmed_orders = orders.objects.filter(status='confirmed').order_by('table_number')

#     return render(request, 'kitchen/kitchen_home.html', {'tables_with_orders': tables_with_orders,'confirmed_orders': confirmed_orders})

# # def confirm_order(request, order_id):
# #     order = get_object_or_404(SubmittedItem, id=order_id)
# #     order.status = 'confirmed'  # Update status to 'confirmed'
# #     order.save()
# #     return redirect('table_home')  # Redirect back to kitchen viewable_home


# def confirm_order(request, item_id):
#     if request.method == 'POST':
#         # Get the order item using the item_id
#         item = get_object_or_404(SubmittedItem, id=item_id)
#         # Update the status or perform any action you need
#         item.status = 'confirmed'
#         item.save()
#         print(item)
#         print(item.status)
#         context = {'order':item}
#         return redirect('kitchen_home')  # Redirect to the kitchen home after confirmation






# from django.shortcuts import render, get_object_or_404, redirect
# # from .models import SubmittedItem

# def kitchen_home(request):
#     # Fetch pending and confirmed orders
#     pending_orders = SubmittedItem.objects.filter(status='pending').order_by('table_number')
#     confirmed_orders = SubmittedItem.objects.filter(status='confirmed').order_by('table_number')
    
#     # Organize pending orders by table_number
#     tables_with_orders = {}
#     for order in pending_orders:
#         table_number = order.table_number
#         if table_number not in tables_with_orders:
#             tables_with_orders[table_number] = []
#         tables_with_orders[table_number].append(order)

#     # Pass both pending and confirmed orders to the template
#     return render(request, 'kitchen/kitchen_home.html', {
#         'tables_with_orders': tables_with_orders,
#         'confirmed_orders': confirmed_orders
#     })

from django.shortcuts import render, get_object_or_404, redirect
# from .models import SubmittedItem

def kitchen_home(request):



    # if request.method == 'POST':
    #     # Check if the form is for deleting an order
    #     delete_order_id = request.POST.get('delete_order_id')
    #     if delete_order_id:
    #         order = get_object_or_404(SubmittedItem, id=delete_order_id)
    #         order.delete()
    # Fetch pending and confirmed orders

    pending_orders = SubmittedItem.objects.filter(status='pending').order_by('tableNumber')
    confirmed_orders = SubmittedItem.objects.filter(status='confirmed').order_by('tableNumber')
    
    # Organize both pending and confirmed orders by table_number
    tables_with_orders = {}
    
    # Organize pending orders by table_number
    for order in pending_orders:
        table_number = order.tableNumber
        if table_number not in tables_with_orders:
            tables_with_orders[table_number] = {'pending': [], 'confirmed': []}
        tables_with_orders[table_number]['pending'].append(order)

    # Organize confirmed orders by table_number
    for order in confirmed_orders:
        table_number = order.tableNumber
        if table_number not in tables_with_orders:
            tables_with_orders[table_number] = {'pending': [], 'confirmed': []}
        tables_with_orders[table_number]['confirmed'].append(order)

    # Pass the combined dictionary to the template
    return render(request, 'kitchen/kitchen_home.html', {
        'tables_with_orders': tables_with_orders
    })

# def confirm_order(request, item_id):
#     if request.method == 'POST':
#         # Get the order item using the item_id
#         item = get_object_or_404(SubmittedItem, id=item_id)
#         # Update the status to 'confirmed'
#         item.status = 'confirmed'
#         item.save()
        
#         # Redirect to the kitchen home after confirmation
#         return redirect('kitchen_home')

# def confirm_order(request, table_number):
#     # Fetch pending orders for the specified table
#     pending_orders = orders.objects.filter(table_number=table_number, status='pending')
    
#     # Update the status of each order to 'confirmed'
#     pending_orders.update(status='confirmed')
    
#     # Redirect back to the kitchen page (or refresh the current page)
#     return redirect('kitchen_home')



from django.shortcuts import get_object_or_404, redirect

def confirm_order(request, table_number):
    if request.method == 'POST':
        # Fetch all pending orders for the specified table
        pending_orders = SubmittedItem.objects.filter(tableNumber=table_number, status='pending')

        # Update the status of each order to 'confirmed'
        pending_orders.update(status='confirmed')
        
        # Redirect back to the kitchen home after confirmation
        return redirect('kitchen_home')

def confirm_all_orders(request, table_number):
    if request.method == 'POST':
        # Get all pending orders for the specified table
        all_orders = orders.objects.filter(tableNumber=table_number, status='pending')
        
        # Update status for all pending orders
        for order in all_orders:
            order.status = 'confirmed'
            order.save()
        
        # Redirect or render a success message
        return redirect('kitchen_home')  # Redirect to the kitchen home page

# def kitchen_home(request):
#     # Assuming there's only one active table number per request/session
#     submitted_items = SubmittedItem.objects.all()
    
#     if submitted_items.exists():
#         table_number = submitted_items.first().table_number  # Get the first table number
#     else:
#         table_number = None  # Handle the case where no orders exist

#     context = {
#         'orders': submitted_items,
#         'table_number': table_number,
#     }

#     return render(request, 'kitchen/kitchen_home.html', context)



def tableList(request):
    tab=request.GET.get('tab','recent')
    table_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]  # Example: Replace with your logic to get table numbers
    if tab == 'all':
        template_name = 'kitchen/tableList.html'
        context = {'table_numbers': table_numbers}
    else:
        template_name = 'kitchen/kitchen_home.html'
        context = {'table_numbers': table_numbers}

    return render(request, template_name, context)



def get_table_receipt(request, table_number):
    receipt_data = {
        "1": {
            "customer_name": "John Doe",
            "order_no": "123456",
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
    data = receipt_data.get(str(table_number), {
        "error": "No data found for this table number."
    })

    return JsonResponse(data)



# from table.models import orders

# def confirm_order(request, order_id):
#     try:
#         order = orders.objects.get(id=order_id)
#         order.status = 'confirmed'  # Update the status to 'confirmed'
#         order.save()
#         return redirect('view_orders')  # Redirect back to the orders page
#     except orders.DoesNotExist:
#         return JsonResponse({'error': 'Order not found'}, status=404)


def delete_order(request, order_id):
    order = get_object_or_404(SubmittedItem, id=order_id)
    order.delete()
    return redirect('kitchen_home')  # Replace 'pending_orders' with your actual view name
