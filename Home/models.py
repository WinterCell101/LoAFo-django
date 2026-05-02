from django.db import models

class Item(models.Model):
    STATUS_CHOICES = [
        ('LOST', 'Lost Item'),
        ('FOUND', 'Found Item'),
    ]
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('documents', 'Documents'),
        ('personal', 'Personal'),
        ('others', 'Others'),
    ]
    SUBCATEGORY_CHOICES = [
        ('electronics', (
             ('smartphone', 'Smartphone'),
             ('laptop', 'Laptop'),
             ('earphones', 'Earphones'),
             ('charger', 'Charger'),
             ('other', 'Other'),
        )),
        ('documents',(
            ('student ID', 'Student ID'),
            ('national ID', 'National ID'),
            ('passport', 'Passport'),
            ('ATM Card', 'ATM Card'),
            ('Other', 'Other'),
        )),
        ('personal',(
            ('wallet', 'Wallet'),
            ('keys', 'Keys'),
            ('backpack', 'Backpack'),
            ('watch', 'Watch'),
            ('other', 'Other')
        )),
        ('others',(
            ('water bottle', 'Water Bottle'),
            ('umbrella', 'Umbrella'),
            ('books', 'Books'),
            ('tools', 'Tools'),
            ('other', 'Other'),
         ))
    ]
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('silver/grey', 'Silver/Grey'),
        ('blue', 'Blue'),
        ('red', 'Red'),
        ('gold', 'Gold'),
        ('other', 'Other'),
    ]

    item_id = models.AutoField(primary_key=True)
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='LOST')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    sub_category = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, null=True, blank=True)
    item_name = models.CharField(max_length=50, null=True, blank=True)  # This is for the name of the item
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, null=True, blank=True)

    location = models.CharField(max_length=150, null=True, blank=True)
    exact_location = models.CharField(max_length=150, null=True, blank=True)
    additional_location = models.CharField(max_length=150, null=True, blank=True)

    owner_name = models.CharField(max_length=100, null=True, blank=True)
    contact_info = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_status} - {self.item_name or 'Unnamed Item'}"

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.item.item_brand} ({self.item.id})"
# Create your models here.
