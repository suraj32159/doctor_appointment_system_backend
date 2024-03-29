from django.conf import settings
from django.core.mail import send_mail
from mailer.my_mailer import Mailer
from doctor_management_system.celery import app

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


class SendMail(Mailer):
    def send_mail_to(self, params, gmeet_link):
        context = {
            "subject": "Book Appointment Request",
            "recipients": "punarvasuaatreyaayurveda@gmail.com",
            "receiver_name": "Dr. MeghaSinh Rajput",
            "patient_name": params.get('name'),
            "contact_number": params.get('contact_number'),
            "date_time": params.get('date_time'),
            "time_interval": params.get('time_interval'),
            "location": params.get('location'),
            "gmeet_link": gmeet_link
        }
        template_name = "bookAppointmentRequest.html"
        patient_template_name = "bookingApproved.html"
        try:
            subject = f"Book Appointment Request By {params.get('name').title()}"
            message = self.send_messages(context, template_name)
            from_email = EMAIL_HOST_USER
            recipient_list = ['punarvasuaatreyaayurveda@gmail.com']

            # to Megha
            data_dr = {
                "subject": subject,
                "message": "",
                "from_email": from_email,
                "recipient_list": recipient_list,
                "html_message": message._content
            }
            # self.fire_mail(data_dr)

            # To Patient
            patient_message = self.send_messages(context, patient_template_name)
            data_patient = {
                "subject": subject,
                "message": "",
                "from_email": from_email,
                "recipient_list": [params.get('email')],
                "html_message": patient_message._content
            }
            # self.fire_mail(data_patient)
        except Exception as e:
            print(e)
        return True

    def fire_mail(self, data):
        send_mail(
            subject=data.get("subject"),
            message="",
            from_email=data.get("from_email"),
            recipient_list=data.get("recipient_list"),
            fail_silently=False,
            html_message=data.get("html_message"),
        )
        return True
