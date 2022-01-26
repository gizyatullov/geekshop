from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    full_link = f'{settings.BASE_URL}{verify_link}'

    title = f'Подтверждение учетной записи {user.username}'
    # message = f'Для подтверждения учетной записи {user.username} на портале ' \
    #           f'{settings.DOMAIN_NAME} перейдите по ссылке:\n{full_link}'

    context = {
        'page_title': 'подтверждение регистрации',
        'title': title,
        'full_link': full_link,
    }
    message = render_to_string('authnapp/emails/register_message.html', context=context)

    print(f'from: {settings.EMAIL_HOST_USER}, to: {user.email}')

    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
