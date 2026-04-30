from django.shortcuts import render,redirect, get_object_or_404
from events.models import EventsList,outdoorimages,indoorimages,veg_menu,non_veg_menu,FinalCateringDetails,Enquiry, OrderManagement
from events.forms import EnquiryForm
from events.utils import send_mail_view
from django.contrib.auth.models import User

# Create your views here.

def events_description(request, id=0):
    event = EventsList.objects.get(id=id)
    return render(request, "events/eventsDescription.html", {"events": event})

def slotbooking(request, id=0):
    event = get_object_or_404(EventsList, id=id)

    if request.method == 'POST':
        request.session['event_name'] = event.name
        request.session['event_date'] = request.POST.get('event_date')
        request.session['event_time'] = request.POST.get('event_time')
        return redirect('next')  # Or wherever you're going

    indoor_imgs = indoorimages.objects.filter(eventName=event)
    outdoor_imgs = outdoorimages.objects.filter(eventName=event)

    context = {
        'event': event,
        'indoor_images': indoor_imgs,
        'outdoor_images': outdoor_imgs
    }
    return render(request, 'events/slotbooking.html', context)



def indoor_images(request,event_id):
    event = get_object_or_404(EventsList, id=event_id)
    indoor_imgs = indoorimages.objects.filter(eventName = event)
    context = {
        'event': event,
        'indoor_images': indoor_imgs,}
    return render(request, 'events/indoorimages.html', context)


def outdoor_images(request, event_id):
    event = get_object_or_404(EventsList, id=event_id)
    outdoor_imgs = outdoorimages.objects.filter(eventName = event)
    context = {
        'event': event,
        'outdoor_images': outdoor_imgs,}
    return render(request, 'events/outdoorimages.html', context)        
    
def next_page(request):
    return render(request, 'events/next.html')

def catering_view(request):
    context = {
        'veg_menu': veg_menu.objects.all(),
        'non_veg_menu' : non_veg_menu.objects.all()
    }
    return render(request, 'events/next.html', context)

from events.models import veg_menu, non_veg_menu, ExtraMenuItem

def get_menu_items(menu_num, menu_type):
    if menu_type == 'veg':
        if menu_num == '1':
            return veg_menu.objects.filter(id__in=[1, 2, 3])
        elif menu_num == '2':
            return veg_menu.objects.filter(id__in=[4, 5, 6])
        elif menu_num == '3':
            return veg_menu.objects.filter(id__in=[7, 8, 9])
    else:
        if menu_num == '1':
            return non_veg_menu.objects.filter(id__in=[1, 2, 3])
        elif menu_num == '2':
            return non_veg_menu.objects.filter(id__in=[4, 5, 6])
        elif menu_num == '3':
            return non_veg_menu.objects.filter(id__in=[7, 8, 9])
    return veg_menu.objects.none()

def customize(request):
    # Get or fallback from session
    menu_num = request.GET.get('menu') or request.session.get('menu_num', '1')
    menu_type = request.GET.get('type') or request.session.get('menu_type', 'veg')

    # Store in session
    request.session['menu_num'] = menu_num
    request.session['menu_type'] = menu_type

    # Get selected items for the menu
    selected_items = get_menu_items(menu_num, menu_type)
    selected_ids = list(selected_items.values_list('id', flat=True))
    request.session['selected_menu_items'] = selected_ids

    # Get extra replacement items
    extra_items = ExtraMenuItem.objects.filter(type=menu_type).exclude(id__in=selected_ids)

    # ✅ FIX: Indented properly now
    if request.method == 'POST':
        final_ids = request.POST.getlist('final_items')
        request.session['final_menu'] = [int(i) for i in final_ids]
        return redirect('final_details')

    return render(request, 'events/customize.html', {
        'menu_type': menu_type,
        'menu_num': menu_num,
        'selected_items': selected_items,
        'extra_items': extra_items,
        'required_count': len(selected_items)
    })

def get_menu_items(menu_num, menu_type):
    if menu_type == 'veg':
        return veg_menu.objects.filter(menu_number=menu_num)
    else:
        return non_veg_menu.objects.filter(menu_number=menu_num)


def final_details(request):
    event_name = request.session.get('event_name', '')
    event_type = request.session.get('event_type', '')
    return render(request, 'events/final_details.html', {
        'event_name': event_name,
        'event_type': event_type
    })

def submit_final_details(request):
    if request.method == 'POST':
        data = request.POST
        detail = FinalCateringDetails.objects.create(
            event_name=data.get('event_name'),
            event_type=data.get('event_type'),
            total_people=int(data.get('total_people')),
            food_type=data.get('food_type'),
            menu_type=int(data.get('menu_type')),
            no_of_suppliers=int(data.get('no_of_suppliers')),
            cake_required=int(data.get('cake_required')),
            welcome_drinks='welcome_drinks' in data,
            welcome_chats='welcome_chats' in data,
            pan='pan' in data
        )
        return redirect('confirmation', id=detail.id)
    return redirect('final_details')

def confirmation(request, id):
    detail = get_object_or_404(FinalCateringDetails, id=id)
    return render(request, 'events/confirmation.html', {
        'details': detail,
        'event_date': request.session.get('event_date', 'N/A'),
        'event_time': request.session.get('event_time', 'N/A')
    })

def calculate_price(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detail = get_object_or_404(FinalCateringDetails, id=id)

        # 🟩 Fetch matching event for basic package price
        event = EventsList.objects.filter(name=detail.event_name).first()
        basic_package_price = event.price if event else 0

        # Menu price
        if detail.food_type == 'veg':
            menu = veg_menu.objects.filter(menu_number=detail.menu_type).first()
        else:
            menu = non_veg_menu.objects.filter(menu_number=detail.menu_type).first()

        menu_price = menu.price if menu else 0

        # Calculations
        total_menu_price = menu_price * detail.total_people
        cake_price = detail.cake_required * 500
        supplier_price = detail.no_of_suppliers * 350
        maintenance_charge = 1000
        cleaning_charge = 1000

        subtotal = total_menu_price + cake_price + supplier_price + maintenance_charge + cleaning_charge + basic_package_price
        gst = subtotal * 0.06
        total_cost = subtotal + gst

        return render(request, 'events/final_price.html', {
            'details': detail,
            'menu_price': menu_price,
            'total_menu_price': total_menu_price,
            'cake_price': cake_price,
            'supplier_price': supplier_price,
            'maintenance_charge': maintenance_charge,
            'cleaning_charge': cleaning_charge,
            'gst': round(gst, 2),
            'total_cost': round(total_cost, 2),
            'basic_package_price': basic_package_price
        })

    return redirect('next')


def success(request):
    return render(request, "events/success.html")

def enquiry_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'events/enquiry_thanks.html')
    else:
        form = EnquiryForm()
    return render(request, 'events/enquire.html', {'form': form})


def finalize_order(request):
    if request.method == 'POST':
        detail_id = request.POST.get('detail_id')
        detail = get_object_or_404(FinalCateringDetails, id=detail_id)
        email = request.user.email
        print(email)
        event = EventsList.objects.filter(name=detail.event_name).first()
        basic_package_price = event.price if event else 0

        if detail.food_type == 'veg':
            menu = veg_menu.objects.filter(menu_number=detail.menu_type).first()
        else:
            menu = non_veg_menu.objects.filter(menu_number=detail.menu_type).first()

        menu_price = menu.price if menu else 0
        total_menu_price = menu_price * detail.total_people
        cake_price = detail.cake_required * 500
        supplier_price = detail.no_of_suppliers * 350
        maintenance_charge = 1000
        cleaning_charge = 1000

        subtotal = total_menu_price + cake_price + supplier_price + maintenance_charge + cleaning_charge + basic_package_price
        gst = round(subtotal * 0.06, 2)
        total_cost = round(subtotal + gst, 2)

        # ✅ Check if an order already exists
        order, created = OrderManagement.objects.update_or_create(
            catering_detail=detail,
            defaults={
                'basic_package_price': basic_package_price,
                'menu_price': menu_price,
                'total_menu_price': total_menu_price,
                'cake_price': cake_price,
                'supplier_price': supplier_price,
                'maintenance_charge': maintenance_charge,
                'cleaning_charge': cleaning_charge,
                'gst': gst,
                'total_cost': total_cost
            }
        )
        send_mail_view(
            email=email,
            event_name=event.name,
            grand_total=total_cost,
            event_date=request.session.get('event_date', 'Not Provided'),
            event_time=request.session.get('event_time', 'Not Provided')
)

        return redirect('success')

    return redirect('next')
