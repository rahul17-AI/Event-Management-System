from django.db import models

# Create your models here.

class EventsList(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    descriptions = models.TextField()
    image = models.ImageField(upload_to='event', blank=True, null=True)

    def __str__(self):
        return self.name
    
class EventType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class indoorimages(models.Model):
    eventName = models.ForeignKey(EventsList,related_name='eventLists',on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType,related_name='evenTypes',on_delete=models.CASCADE)
    indoorimg = models.ImageField(upload_to='indoorimg',blank=True,null=True)

    def __str__(self):
        return f"{self.eventName.name} (Indoor)"

class outdoorimages(models.Model):
    eventName = models.ForeignKey(EventsList,related_name='eventlists',on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType,related_name='eventypes',on_delete=models.CASCADE)
    outdoorimg = models.ImageField(upload_to='outdoorimg',blank=True,null=True)

    def __str__(self):
        return f"{self.eventName.name} (Outdoor)"

class veg_menu(models.Model):
    price = models.IntegerField()
    item = models.TextField()
    menu_number = models.IntegerField()


class non_veg_menu(models.Model):
    price = models.IntegerField()
    item = models.TextField()
    menu_number = models.IntegerField()



class FinalCateringDetails(models.Model):
    event_name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    total_people = models.PositiveIntegerField()
    food_type = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')])
    menu_type = models.IntegerField()  # Stores 1, 2, or 3
    no_of_suppliers = models.PositiveIntegerField()
    cake_required = models.PositiveIntegerField(help_text="0 means no cake")
    welcome_drinks = models.BooleanField(default=False)
    welcome_chats = models.BooleanField(default=False)
    pan = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event_name} - {self.event_type}"
    
class ExtraMenuItem(models.Model):
    item = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')])

    def __str__(self):
        return f"{self.item} ({self.type})"
    
class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"

class OrderManagement(models.Model):
    catering_detail = models.OneToOneField(FinalCateringDetails, on_delete=models.CASCADE, related_name='order_summary')

    basic_package_price = models.FloatField()
    menu_price = models.FloatField()
    total_menu_price = models.FloatField()
    cake_price = models.FloatField()
    supplier_price = models.FloatField()
    maintenance_charge = models.FloatField()
    cleaning_charge = models.FloatField()
    gst = models.FloatField()
    total_cost = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.catering_detail.event_name} on {self.created_at.date()}"
