from django.db import models

import datetime
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published')
    TAG_NAMES = (('教育成长', (('校园生活', '校园生活'), ('考研出国', '考研出国'), )),
                 ('党建团建', (('团务工作', '团务工作'), ('党务工作', '党务工作'), )),
                 ('unknown', 'unknown'))

    tag = models.CharField(max_length=10, choices=TAG_NAMES, default='unknown')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
