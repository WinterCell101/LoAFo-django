from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Item, ItemImage  # Don't forget to import ItemImage


def home(request):
    found_items = Item.objects.filter(item_status='FOUND').order_by('-id')
    lost_items = Item.objects.filter(item_status='LOST').order_by('-id')

    context = {
        'found_items': found_items,
        'found_count': found_items.count(),
        'lost_items': lost_items,
        'lost_count': lost_items.count(),
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
            item_type=request.POST.get('report_type'),
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
    query = request.GET.get('q', '')
    results = Item.objects.all()

    if query:
        results = results.filter(
            Q(category__icontains=query) |
            Q(sub_category__icontains=query) |
            Q(location__icontains=query) |
            Q(exact_location__icontains=query)
        )

    context = {
        'found_items': results.filter(item_type='FOUND').order_by('-id'),
        'lost_items': results.filter(item_type='LOST').order_by('-id'),
        'query': query,
        'found_count': results.filter(item_type='FOUND').count(),
        'lost_count': results.filter(item_type='LOST').count(),
    }
    return render(request, 'homepage.html', context)