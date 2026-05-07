from django.contrib import admin
from .models import Item, ItemImage
from .services import post_to_facebook


@admin.action(description="Post selected to Facebook")
def make_facebook_post(modeladmin, request, queryset):
    for item in queryset:
        # 1. Compile the message using your new model methods
        item_link = f"http://127.0.0.1:8000/items/{item.item_id}/"

        message = (
            f"📢 LOST ITEM ALERT!\n\n"
            f"{item.get_formatted_description()}\n\n"
            f"{item.get_contact_info()}\n"
            f"View Details: {item_link}/"
        )

        # 2. Get the first image associated with this item
        image_obj = item.images.first()  # Uses the related_name or default set
        image_path = image_obj.image.path if image_obj else None

        # 3. Send to Facebook
        result = post_to_facebook(message, image_path, item_link)

        if 'id' in result or 'post_id' in result:
            modeladmin.message_user(request, f"Successfully posted {item.item_name or 'Item'}")
        else:
            error_msg = result.get('error', {}).get('message', 'Unknown Error')
            modeladmin.message_user(request, f"Failed to post {item.item_name or 'Item'}: {error_msg}", level='ERROR')

# 1. This tells Django how to show images INSIDE the Item page
class ItemImageInline(admin.TabularInline):  # Use TabularInline for a clean list
    model = ItemImage
    extra = 1  # Shows one empty slot to add a new image


# 2. This configures the main Item admin page
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # This combines the Facebook action with your layout settings
    inlines = [ItemImageInline]
    list_display = ('item_id', 'created_at', 'item_name', 'item_status', 'owner_name')
    list_filter = ('item_status', 'category', 'location', 'created_at')
    search_fields = ('item_name', 'location', 'owner_name', 'item_id')
    readonly_fields = ('created_at', 'updated_at')
    actions = [make_facebook_post] # Your one-click button is here!

admin.site.site_header = "LoAFo Admin Portal"
admin.site.site_title = "LoAFo"
admin.site.index_title = "Welcome to LoAFo Management"

# Note: You don't need to register ItemImage separately if it's already an inline,
# but you can if you want to manage images one by one.
from django.contrib import admin

# Register your models here.
