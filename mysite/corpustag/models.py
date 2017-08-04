from django.db import models

# Create your models here.


class YouthForumData(models.Model):
    question_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published')
    FIRST_TAGS = (('教育成长', '教育成长'), ('党建团建', '党建团建'))
    SECOND_TAGS = ((FIRST_TAGS[0][0], (('校园生活', '校园生活'), ('考研出国', '考研出国'))), (FIRST_TAGS[1][0], (('团务工作', '团务工作'),
                   ('党务工作', '党务工作'))), ('unknown', 'unknown'))

    first_class = models.CharField(max_length=20, choices=FIRST_TAGS, default='unknown')
    second_class = models.CharField(max_length=20, choices=SECOND_TAGS, default='unknown')

    def was_tagged_manually(self):

        return 'unknown' not in [self.first_class, self.second_class]

    was_tagged_manually.admin_order_field = 'pub_date'
    was_tagged_manually.boolean = True
    was_tagged_manually.short_description = 'already tagged?'

    def __str__(self):
        return self.question_text


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text
