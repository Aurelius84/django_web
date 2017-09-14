from django.db import models
from smart_selects.db_fields import ChainedForeignKey
import django.utils.timezone as timezone
import hashlib

# Create your models here.

TAGS = {
    "党建团建": ["党章党史", "团章团史", "入党入团", "党务工作", "团务工作", "干部培训", "基层团建"],
    "创业就业":
    ["职场人际", "创业就业方向", "创业资质", "创业团队", "创业项目", "创业投资", "工作机会", "求职面试", "实习兼职"],
    "教育成长": ["校园教育", "家庭教育", "社会教育", "投资理财", "校园生活"],
    "理想信念": ["生活理想", "职业理想", "道德理想", "社会理想"],
    "情感家庭": ["亲情", "友情", "婚恋", "生育"],
    "人文科技": ["哲学社会", "文学艺术", "历史地理", "科学技术", "工业技术", "运输工程", "环境安全"],
    "社团公益": ["社团组织", "学生组织", "公益志愿", "社会实践"],
    "身心健康": ["保健养生", "美容健体", "身体健康", "心理咨询", "体育运动"],
    "政策法规": ["时事热点", "国情政策", "经济政治", "文化社会", "生态文明", "法律法规"],
    "生活休闲": ["衣食住行", "户外休闲", "娱乐活动", "数码游戏", "生活服务"],
    "权益维护":
    ["妇女权益保障", "劳动者权益保障", "消费者权益保护", "社会保障", "未成年人保护", "咨询求助", "知识产权保护"]
}


class YouthFirstCate(models.Model):
    FIRST_TAGS = tuple([(k, k) for k in TAGS] + [('unknown', 'unknown')])
    name = models.CharField(
        max_length=255,
        choices=FIRST_TAGS,
        default='unknown',
        unique=True,
        verbose_name='一级类目')
    timestamp = timezone.now
    created = models.DateTimeField('创建时间', default=timestamp)
    modified = models.DateTimeField('修改时间', default=timestamp)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(YouthFirstCate, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name_plural = '青年之声一级类目关系表'


class YouthSecondCate(models.Model):
    SECOND_TAGS = [(k, [[v, v] for v in val])
                   for k, val in TAGS.items()] + [('unknown', 'unknown')]
    first_class = models.ForeignKey(YouthFirstCate)
    name = models.CharField(
        max_length=255,
        choices=SECOND_TAGS,
        default='unknown',
        # unique=True,
        verbose_name='二级类目')
    timestamp = timezone.now
    created = models.DateTimeField('创建时间', default=timestamp)
    modified = models.DateTimeField('修改时间', default=timestamp)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(YouthSecondCate, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        unique_together = (("first_class", "name"))
        verbose_name_plural = '青年之声二级类目关系表'


class YouthForumData(models.Model):
    question_text = models.TextField(max_length=800, verbose_name='问题文本')
    # make question_text unique
    question_hash = models.CharField(max_length=32, unique=True)

    timestamp = timezone.now
    created = models.DateTimeField('创建时间', default=timestamp)
    modified = models.DateTimeField('修改时间', default=timestamp)
    first_class = models.ForeignKey(YouthFirstCate, verbose_name='一级类目')
    mlHit = models.CharField(
        max_length=10,
        choices=[("T", "Right"), ("F", "Wrong"), ("unknown", "unknown")],
        default='unknown',
        verbose_name='机器分类')
    second_class = ChainedForeignKey(
        YouthSecondCate,
        chained_field="first_class",
        chained_model_field="first_class",
        show_all=False,
        auto_choose=True,
        verbose_name='二级类目',
        sort=True)

    def was_tagged_manually(self):
        """标识是否为人工标注"""

        return 'unknown' not in [self.first_class.name, self.second_class.name]

    was_tagged_manually.admin_order_field = 'modified'
    was_tagged_manually.boolean = True
    was_tagged_manually.short_description = '已人工标注?'

    def was_check_manually(self):
        """标识是否人工纠正过"""
        return "unknown" != self.mlHit

    was_check_manually.admin_order_field = 'modified'
    was_check_manually.boolean = True
    was_check_manually.short_description = '已人工审核?'

    def __str__(self):
        return self.question_text

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        m = hashlib.md5()
        m.update(self.question_text.encode('utf8'))
        # 十六进制
        self.question_hash = m.hexdigest()
        return super(YouthForumData, self).save(*args, **kwargs)

    class Meta:
        ordering = ['modified']
        verbose_name_plural = '青年之声人工标注语料库'
