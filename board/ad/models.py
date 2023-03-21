from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class Ad(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemeisters', 'Гилдмастеры'),
        ('questgivers', "Квестгиверы"),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potionmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
         )
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=128)
    text = RichTextUploadingField(blank=True, null=True)
    category = models.CharField(max_length=15, choices=TYPE, default='tanks')

    def preview(self):
        t = self.text
        x1 = t.find('<img', 0, len(t)-1)
        x2 = t.find('>', x1, len(t)-1)
        if x1 == -1:
            return t[0:124]+"..."
        else:
            t1 = t[0:x1] + t[x2+1:len(t)-1]
            return t1[0:124]+"..."

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}: {self.author.username}'


class UserResponse(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True)
    text = models.TextField()
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='us_resp')
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('ad_list')
