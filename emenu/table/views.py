

# table/views.py
from django.shortcuts import render, get_object_or_404

from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from .models import FoodItem, NotSubmittedItem, SubmittedItem, Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# # import qrcode
# from io import BytesIO
# from django.http import HttpResponse
# from django.shortcuts import redirect


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    food_items = FoodItem.objects.filter(category=category)
    return render(request, 'index.html', {
        'category': category,
        'food_items': food_items,
    })


def about(request):
    return render(request, 'about.html')
  
def  testimonial(request):
    return render(request , 'testimonial.html')

  
def  booking(request):
    return render(request , 'booking.html')

def contact(request):
    return render(request ,'contact.html')

def bill(request):
    return render(request ,'bill.html')

def submit_order(request):
    not_submitted_items = NotSubmittedItem.objects.all()
    total_bill = 0

    for item in not_submitted_items:
        total_price = item.price * item.quantity
        SubmittedItem.objects.create(
            food_item=item.food_item,
            name=item.name,
            price=item.price,
            image=item.image,
            quantity=item.quantity,
            total_price=total_price,
            tableNumber = item.tableNumber,
            status='pending'

        )
        total_bill += total_price
    table_number=request.session.get('table_number')
    print(f"Table number from session: {table_number}")
    NotSubmittedItem.objects.all().delete()  # Clear NotSubmitted items
    # not_submitted_items = NotSubmittedItem.objects.all()  # Fetch all the selected items
    submitted_items = SubmittedItem.objects.filter(tableNumber=table_number)
    # print(submitted_items)
    # return render(request, 'order.html', {'total_bill': total_bill})

    return render(request, 'order.html', {'not_submitted_items': not_submitted_items  ,'submitted_items':submitted_items ,  'total_bill': total_bill})




from django.http import JsonResponse
from .models import NotSubmittedItem, FoodItem

def add_not_submitted_item(request):
    if request.method == "POST":
        food_item_id = request.POST.get('item_id')  # Use 'food_item' as ForeignKey to FoodItem
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity'))
        image_url = request.POST.get('image_url')
        table_number = request.POST.get('table_number')
        if not table_number:
            # Handle missing table number
            return HttpResponse("Table number is required.", status=400)

        # Fetch the FoodItem instance
        try:
            food_item = FoodItem.objects.get(id=food_item_id)
        except FoodItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Food item not found'}, status=404)

        # Check if the item is already in the not submitted list
        item, created = NotSubmittedItem.objects.get_or_create(
            food_item=food_item,  # Using ForeignKey to FoodItem
            defaults={
                'name': name,
                'price': price,
                'quantity': quantity,
                'image': image_url,  # Assuming you handle image uploads elsewhere
                'tableNumber': table_number
            }
        )
        if not created:
            # If the item already exists, update the quantity
            item.quantity += quantity
            item.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



def order(request):
    table_number=request.session.get('table_number')
    print(f"Table number from session in order view: {table_number}")

    not_submitted_items = NotSubmittedItem.objects.all()  # Fetch all the selected items
    submitted_items = SubmittedItem.objects.filter(tableNumber=table_number)
    return render(request, 'order.html', {'not_submitted_items': not_submitted_items  ,'submitted_items':submitted_items })


# views.py

from django.shortcuts import get_object_or_404, redirect
from .models import SubmittedItem

def cancel_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(NotSubmittedItem, id=item_id)
        item.delete()
        return redirect('order')  # Redirect to the order view
    


from django.shortcuts import redirect
from django.contrib import messages
from .models import SubmittedItem

def cancel_item_finish(request):
    if request.method == 'POST':
        # Get the current table number from the session
        table_number = request.session.get('table_number')

        if table_number is not None:
            # Delete items in SubmittedItem where the table_number matches the current session table number
            SubmittedItem.objects.filter(tableNumber=table_number).delete()
            # Clear the table number from the session
            del request.session['table_number']
            messages.success(request, "Thank you for visiting! Your table session has ended.")
        else:
            messages.warning(request, "No table session found.")

    return redirect('table_home')


# def cancel_item_finish(request):
#     # Fetch the table number from the session
#     table_number = request.session.get('table_number')
#     request.session['table_number'] = table_number
#     print(f"Table number set in session: {request.session['table_number']}")

#     if table_number is not None:
#         # Delete all SubmittedItem entries for the current table number
#         SubmittedItem.objects.filter(table_number=table_number).delete()

#         # Optionally, add a success message or perform additional logic
#         # e.g., redirect to the home page or an order page
#         return redirect('table_home')  # Change 'home' to your desired redirect URL

#     # If no table number is found, you may want to handle it accordingly
#     return redirect('table_home')  # Redirecting in case of no table number


# from django.shortcuts import redirect
# # from .models import SubmittedItem

# def cancel_item_finish(request):
#     # pass
#     # Fetch the table number from the session
#     table_number = request.session.get('table_number')
#     # print(table_number)

#     if table_number is not None:
#         # Delete all SubmittedItem entries for the current table number
#         SubmittedItem.objects.filter(tableNumber=table_number).delete()  # Use the correct field name

#         # Optionally, add a success message or perform additional logic
#         return redirect('table_home')  # Change 'home' to your desired redirect URL

#     # If no table number is found, you may want to handle it accordingly
#     return redirect('table_home')  # Redirecting in case of no table number










from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Use with caution; consider adding CSRF protection
def set_table_number(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        table_number = data.get('table_number')
        request.session['table_number'] = table_number  # Set table number in session
        print(f"Table number set in session: {table_number}")

        # print(table_number)
        # print(request.session['table_number'])
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def add_to_submitted_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        name = request.POST.get('name')
        price = request.POST.get('price')

        # Fetch the actual NotSubmittedItem
        final_item = NotSubmittedItem.objects.get(id=item_id)

        # Move item to SubmittedItem
        SubmittedItem.objects.create(
            food_item=final_item.food_item,
            name=name,
            price=price,
            image=final_item.image,  # Correct image handling
            quantity=final_item.quantity,
            total_price=final_item.price * final_item.quantity,
        )

        # Delete the item from NotSubmittedItem
        # final_item.delete()
        NotSubmittedItem.objects.all().delete()


        return JsonResponse({'message': 'Item added to order successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def decrease_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(NotSubmittedItem, id=item_id)

        # If the item's quantity is greater than 1, decrease it by 1
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            new_quantity = item.quantity
        else:
            # If the quantity is 1, remove the item from the list
            item.delete()
            new_quantity = 0

        # Return the new quantity as a JSON response
        return JsonResponse({'success': True, 'new_quantity': new_quantity})
    else:
        return JsonResponse({'success': False}, status=400)


def submit_all_items(request):
    not_submitted_items = NotSubmittedItem.objects.all()

    for item in not_submitted_items:
        # Check if the item already exists in the SubmittedItem model
        submitted_item = SubmittedItem.objects.filter(name=item.name).first()

        if submitted_item:
            # If it exists, just update the quantity
            submitted_item.quantity += item.quantity
            submitted_item.save()
        else:
            # If not, create a new SubmittedItem entry
            SubmittedItem.objects.create(
                name=item.name,
                image=item.image,
                quantity=item.quantity,
            )

        # Delete the item from NotSubmittedItem after submission
        item.delete()

    return redirect('table_home')




def save_table_number(request):
    if request.method == 'POST':
        # Get the table number from the submitted form data
        table_number = request.POST.get('table_number')
        
        # Store the table number in the user's session
        request.session['table_number'] = table_number  # This allows you to access it later
        print("Save table ",table_number)
        # Save the submitted item in the database
        SubmittedItem.objects.create(tableNumber=table_number, )  # Save other necessary fields

    # Redirect to the kitchen home page after saving
    return redirect('kitchen_home')  


# Import necessary modules

# import qrcode
# # Function to generate QR code
# def generate_qr(request):
#     # URL for the table_home page
#     table_home_url = request.build_absolute_uri('/table_home/')
    
#     # Generate QR code
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(table_home_url)
#     qr.make(fit=True)
    
#     # Create image
#     img = qr.make_image(fill='black', back_color='white')
#     buffer = BytesIO()
#     img.save(buffer, 'PNG')
#     buffer.seek(0)
    
#     # Return QR image as HTTP response
#     return HttpResponse(buffer, content_type='image/png')
# views.py
from django.http import JsonResponse
from .models import NotSubmittedItem, SubmittedItem

# def auto_submit_item(request, item_id):
#     try:
#         not_submitted_item = NotSubmittedItem.objects.get(fooditem=item_id)
        
#         # Create a new SubmittedItem from the NotSubmittedItem
#         submitted_item = SubmittedItem.objects.create(
#             food_item=not_submitted_item.food_item,
#             name=not_submitted_item.name,
#             price=not_submitted_item.price,
#             image=not_submitted_item.image,
#             quantity=not_submitted_item.quantity,
#             total_price=not_submitted_item.price * not_submitted_item.quantity,
#             tableNumber=not_submitted_item.tableNumber,
#             status='submitted'
#         )
        
#         # Remove the item from NotSubmittedItem
#         not_submitted_item.delete()
        
#         return JsonResponse({'success': True, 'submitted_item_id': submitted_item.food_item})
#     except NotSubmittedItem.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

def submit_item(request, item_id):
    # Fetch the item from NotSubmitted and delete it after transferring
    item = get_object_or_404(NotSubmittedItem, id=item_id)

    # Move item details to Submitted model
    SubmittedItem.objects.create(
        table_number=item.tableNumber,
        item_name=item.name,
        quantity=item.quantity,
        price=item.price
    )

    # Remove the item from NotSubmitted
    item.delete()

    return JsonResponse({'status': 'success', 'message': 'Item submitted successfully.'})
