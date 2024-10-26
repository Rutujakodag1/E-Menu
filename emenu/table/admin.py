



from django.contrib import admin

from table.models import Category, FoodItem, NotSubmittedItem, SubmittedItem,orders

# Admin configuration for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


from .models import FoodItem

class FoodItemAdmin(admin.ModelAdmin):
    # your custom admin settings here
    pass

admin.site.register(FoodItem, FoodItemAdmin)

# Admin configuration for NotSubmittedItem model
@admin.register(NotSubmittedItem)
class NotSubmittedItemAdmin(admin.ModelAdmin):

    list_display = ('food_item', 'name', 'quantity', 'price', 'tableNumber')  # Specify the fields you want to display
    list_filter = ('food_item', 'tableNumber')  # Optional: Add filters for easier navigation
    search_fields = ('name', 'food_item__name')

    


class SubmittedItemAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'name', 'quantity', 'total_price', 'tableNumber')  # Specify the fields you want to display
    list_filter = ('food_item', 'tableNumber')  # Optional: Add filters for easier navigation
    search_fields = ('name', 'food_item__name')  # Optional: Add a search field

# Register the model with the custom admin class
admin.site.register(SubmittedItem, SubmittedItemAdmin)



# Admin interface for Orders
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('tableNumber', 'name', 'quantity', 'total_price')  # Display all fields
    list_filter = ('tableNumber',)  # Filter by table number
    search_fields = ('name',)  # Search by name

# Register the model with the custom admin class
admin.site.register(orders, OrdersAdmin)

