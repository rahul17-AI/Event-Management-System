from django.urls import path
from events import views

urlpatterns = [
    path('<int:id>',views.events_description,name='events'),
    path('slotbooking/<int:id>/',views.slotbooking, name='slotbooking'),
    path('indoor/<int:event_id>/', views.indoor_images, name='indoor_images'),
    path('outdoor/<int:event_id>/', views.outdoor_images, name='outdoor_images'),
    path('next/',views.catering_view,name='next'),
    path('custmoize/', views.customize, name='customize'),
    path('final/', views.final_details, name='final_details'),
    path('submit_final_details/', views.submit_final_details, name='submit_final_details'),
    path('confirmation/<int:id>/', views.confirmation, name='confirmation'),
    path('calculate_price/', views.calculate_price, name='calculate_price'),
    path('success', views.success, name='success'),
    path('enquire/', views.enquiry_view, name='enquire'),
    path('finalize_order/', views.finalize_order, name='finalize_order'),



]