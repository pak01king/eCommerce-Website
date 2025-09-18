from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string

def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = user.pk
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uid': uid, 'token': token})
    )
    subject = 'Activează-ți contul OnElite WEST'
    message = render_to_string('store/email_activation.html', {
        'user': user,
        'activation_link': activation_link,
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
