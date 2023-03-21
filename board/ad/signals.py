from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Ad, UserResponse
from board.settings import SITE_URL


def send_notifications(preview, pk, title, title1, users):
    html_content = render_to_string(
        'page_mail.html',
        {
           'title': title,
           'title1': title1,
           'text': preview,
           'link': f'{SITE_URL}/ad/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='mviktor8208@yandex.ru',
        to=users,
    )

    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()  # отсылаем


def send_notifications_ur(title, text, pk, status, title1, user_mail):
    html_content = render_to_string(
        'ur_mail.html',
        {
            'title': title,
            'title1': title1,
            'text': text,
            'status': status,
            'link': f'{SITE_URL}/ad/ur_list/{pk}/ur_update',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title1,
        body='',
        from_email='mviktor8208@yandex.ru',
        to=user_mail,
    )

    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()  # отсылаем



@receiver(post_save, sender=Ad)
def ad_mail_user(sender, instance, created, raw, **kwargs,):
    if created:
        title1 = f'На нашем сайте появилось новое объявление'
    else:
        title1 = f'На нашем сайте обновилось существующее объявление'

    users = User.objects.all()
    users = [s.email for s in users]

    send_notifications(instance.preview, instance.pk, instance.title, title1, users)


@receiver(post_save, sender=UserResponse)
def ad_mail_user(sender, instance, created,  raw, **kwargs):
    if created:
        title1 = f'На ваше объявление оставили отклик'
        user_mail = {instance.ad.author.email}
        userr = instance.ad.author.username
    else:
        title1 = f'Ваш отзыв на объявление БЫЛ ПРИНЯТ'
        user_mail = {instance.author.email}
        userr = instance.author.username

    send_notifications_ur(instance.ad.title, instance.text, instance.pk, instance.status, title1, user_mail)
