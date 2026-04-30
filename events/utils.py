from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.http import HttpResponse

def send_mail_view(email, event_name, grand_total, event_date, event_time):

    subject = 'Confirmed your booking by Eventure'
    from_email = "eventur.event123@gmail.com"
    recipient_list = [email]

    context = {
        'events': {
            'event_name': event_name,
            'grand_total': grand_total,
            'event_date': event_date,
            'event_time': event_time
        }
    }

    html_message = render_to_string('events/confirm_email_template.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully")
    except Exception as e:
        return HttpResponse(f"Error sending mail: {str(e)}")
