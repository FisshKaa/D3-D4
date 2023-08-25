from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Post
import time

@shared_task
def send_notification(subscriber_email, news_title):
    send_mail(
        subject='Новая новость',
        message=f'На сайте была опубликована новая новость: {news_title}',
        from_email='primer.bot@yandex.ru',
        recipient_list=[subscriber_email],
    )

@shared_task
def send_weekly_newsletter(subscriber_email):
    week_ago = datetime.now() - timedelta(week=1)
    latest_news = Post.objects.filter(created__gte=week_ago)

    newsletter = "Последние новости:\n"
    for post in latest_news:
        newsletter += f"- {post.title}"

    send_mail(
        subject = 'Еженедельные новости',
        message = newsletter,
        from_email='primer.bot@yandex.ru',
        recipient_list=[subscriber_email],
    )
