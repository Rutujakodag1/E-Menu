from django.shortcuts import render,get_object_or_404

# Create your views here.
from table.models import Category,FoodItem
from table.models import SubmittedItem

#   
def set_table_number(request):
    if request.method == "POST":
        table_number = request.POST.get("table_number")
        request.session["table_number"] = table_number
        request.session.modified = True
        return redirect("menu")   # after setting, go to menu
    return render(request, "enter_table.html")

def home(request):
    return render(request, 'home.html')

def menu_view(request):
    # check if session has table number
    table_number = request.session.get("table_number")

    # if not present → force customer to enter again
    if not table_number:
        return redirect("enter_table_number")   # name of your URL/view for entering table no.

    # else, continue as normal
    return render(request, "menu.html", {
        "table_number": table_number
    })
# def table_home(request):
#     # assign table number to session only if not already set
#     if "table_number" not in request.session:
#         request.session["table_number"] = request.GET.get("table", None)
#     return render(request, "table_home.html")

def clear_table_session(request, table_number):
    """Clear session when counter marks bill as done"""
    if request.session.get("table_number") == str(table_number):
        del request.session["table_number"]
    return redirect("home")


#  
# >>>>>>>  
def table_home(request, id=None):
    categories = Category.objects.all()
    table_number = request.session.get('table_number', None) 

#   
    if "table_number" not in request.session:
        request.session["table_number"] = request.GET.get("table", None)
        table_number = request.session.get('table_number', None)

#  
# >>>>>>>  
    if id:  # if a category ID is provided in the URL
        selected_category = get_object_or_404(Category, id=id)
    else:  # otherwise, show the first category by default
        selected_category = categories.first()

    # Get the food items for the selected category
    food_items = FoodItem.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'food_items': food_items,
        'table_number': table_number
    }


    if request.method == 'POST':
        # Get the table number from the submitted form data
        table_number = request.POST.get('table_number')
        
        # Store the table number in the user's session
        request.session['table_number'] = table_number  # This allows you to access it later

        # Save the submitted item in the database
        SubmittedItem.objects.create(tableNumber=table_number, )  # Save other necessary fields
        print(f"Current Table Number: {table_number}")
    return render(request, 'table_home.html', context)


# Import necessary modules
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect

# Function to generate QR code
def generate_qr(request):
    # URL for the table_home page
    table_home_url = request.build_absolute_uri('/table_home/')
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(table_home_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    
    # Return QR image as HTTP response
    return HttpResponse(buffer, content_type='image/png')



def remove_order_item(request, order_id):
    order = get_object_or_404(SubmittedItem, id=order_id)
    order.delete()
    return redirect('kitchen_home')  