from django.contrib import admin
from events.models import EventsList,EventType,indoorimages,outdoorimages,veg_menu,non_veg_menu,FinalCateringDetails,ExtraMenuItem,Enquiry

# Register your models here.

admin.site.register(EventsList)
admin.site.register(EventType)
admin.site.register(indoorimages)
admin.site.register(outdoorimages)
admin.site.register(veg_menu)
admin.site.register(non_veg_menu)
admin.site.register(FinalCateringDetails)
admin.site.register(ExtraMenuItem)
admin.site.register(Enquiry)
