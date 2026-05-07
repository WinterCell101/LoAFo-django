from django.contrib import admin
from .models import Item, ItemImage


# 1. This tells Django how to show images INSIDE the Item page
class ItemImageInline(admin.TabularInline):  # Use TabularInline for a clean list
    model = ItemImage
    extra = 1  # Shows one empty slot to add a new image


# 2. This configures the main Item admin page
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # This adds the images section to the bottom of the item edit page
    inlines = [ItemImageInline]

    # This makes the main list view much easier to read at a glance
    list_display = ('item_id', 'created_at', 'item_name', 'item_status', 'owner_name')

    # Adds a sidebar filter for faster navigation
    list_filter = ('item_status', 'category', 'location', 'created_at')

    # Adds a search bar
    search_fields = ('item_brand', 'location' 'owner_name', 'id')

    # Optional: Make the timestamp fields read-only so they can't be manually edited
    readonly_fields = ('created_at', 'updated_at')

admin.site.site_header = "LoAFo Admin Portal"
admin.site.site_title = "LoAFo"
admin.site.index_title = "Welcome to LoAFo Management"

# Note: You don't need to register ItemImage separately if it's already an inline,
# but you can if you want to manage images one by one.
from django.contrib import admin

# Register your models here.
