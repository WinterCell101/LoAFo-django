from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Item, ItemImage

def home(request):
    # 1. Get the selected location from the URL (?location=Library)
    selected_location = request.GET.get('location')

    # 2. Get unique locations from the 'Item' model to display in sidebar
    # We use .exclude(location__isnull=True).exclude(location='') to keep the list clean
    all_locations = Item.objects.exclude(location__isnull=True).exclude(location='') \
                        .values_list('location', flat=True).distinct().order_by('location')

    # 3. Initialize the querysets
    found_items = Item.objects.filter(item_status='FOUND').order_by('-item_id')
    lost_items = Item.objects.filter(item_status='LOST').order_by('-item_id')

    # 4. Apply filtering if a location was clicked in the sidebar
    if selected_location:
        found_items = found_items.filter(location=selected_location)
        lost_items = lost_items.filter(location=selected_location)

    context = {
        'found_items': found_items,
        'found_count': found_items.count(),
        'lost_items': lost_items,
        'lost_count': lost_items.count(),
        'locations': all_locations, # Passed to sidebar loop
    }
    return render(request, 'homepage.html', context)


def report_item(request):
    if request.method == 'POST':
        # 1. Handle the color logic BEFORE creating the object
        color = request.POST.get('color')
        if color == 'other':
            color = request.POST.get('custom_color')

        # 2. Create the Item object ONCE
        new_item = Item.objects.create(
            item_status=request.POST.get('report_type'),
            item_name=request.POST.get('name'),
            category=request.POST.get('category'),
            sub_category=request.POST.get('sub_category'),
            color=color,
            location=request.POST.get('location'),
            exact_location=request.POST.get('Trademark'),
            additional_location=request.POST.get('additional_info'),
            owner_name=request.POST.get('owner_name'),
            contact_info=request.POST.get('contact_info')
        )

        # 3. Save Multiple Images (up to 5)
        images = request.FILES.getlist('images')
        for img in images[:5]:
            ItemImage.objects.create(item=new_item, image=img)

        # --- INSERT SUCCESS MESSAGE HERE ---
        messages.success(request, "Successfully Submitted!!")
        # ------------------------------------

        return redirect('home')

    return redirect('home')


def search_items(request):
    query = request.GET.get('q', '').strip()
    results = Item.objects.all()

    if query:

        if query.isdigit():
            Q(item_id__icontains=query)
            search_filter = Q(item_id=query) | Q(item_name__icontains=query)
        else:
            search_filter = (
                Q(item_name__icontains=query) |
                Q(category__icontains=query) |
                Q(sub_category__icontains=query) |
                Q(location__icontains=query) |
                Q(exact_location__icontains=query)
            )
        results = results.filter(search_filter)

    found_items = results.filter(item_status='FOUND').order_by('-id')
    lost_items = results.filter(item_status='LOST').order_by('-id')

    context = {
        'found_items': found_items,
        'lost_items': lost_items,
        'query': query,
        'found_count': found_items.count(),
        'lost_count': lost_items.count(),
    }
    return render(request, 'homepage.html', context)