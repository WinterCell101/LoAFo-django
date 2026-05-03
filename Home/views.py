from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Item, ItemImage
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    selected_location = request.GET.get('location')

    all_locations = Item.objects.exclude(location__isnull=True).exclude(location='') \
                        .values_list('location', flat=True).distinct().order_by('location')

    found_items = Item.objects.filter(item_status='FOUND').order_by('-item_id')
    lost_items = Item.objects.filter(item_status='LOST').order_by('-item_id')
    claimed_items = Item.objects.filter(item_status='CLAIMED').order_by('-item_id')

    if selected_location:
        found_items = found_items.filter(location=selected_location)
        lost_items = lost_items.filter(location=selected_location)
        claimed_items = claimed_items.filter(location=selected_location)

    context = {
        'found_items': found_items,
        'found_count': found_items.count(),
        'lost_items': lost_items,
        'lost_count': lost_items.count(),
        'claimed_items': claimed_items,
        'claimed_count': claimed_items.count(),
        'locations': all_locations,
    }
    return render(request, 'homepage.html', context)


def report_item(request):
    if request.method == 'POST':
        color = request.POST.get('color')
        if color == 'other':
            color = request.POST.get('custom_color')

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

        images = request.FILES.getlist('images')
        for img in images[:5]:
            ItemImage.objects.create(item=new_item, image=img)

        messages.success(request, "Successfully Submitted!!")
        return redirect('home')

    return redirect('home')


def search_items(request):
    query = request.GET.get('q', '').strip()
    results = Item.objects.all()

    # FIX: Added the backslash '\' to prevent SyntaxError on the multi-line query
    locations_list = Item.objects.exclude(location__isnull=True).exclude(location='') \
                        .values_list('location', flat=True).distinct().order_by('location')

    if query:
        if query.isdigit():
            # Standardizing to item_id check for your 1000+ reference logic
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

    found_items = results.filter(item_status='FOUND').order_by('-item_id')
    lost_items = results.filter(item_status='LOST').order_by('-item_id')
    claimed_items = results.filter(item_status='CLAIMED').order_by('-item_id')

    context = {
        'found_items': found_items,
        'lost_items': lost_items,
        'claimed_items': claimed_items,
        'locations': locations_list,
        'query': query,
        'found_count': found_items.count(),
        'lost_count': lost_items.count(),
        'claimed_count': claimed_items.count(), # Added for consistency
    }
    return render(request, 'homepage.html', context)