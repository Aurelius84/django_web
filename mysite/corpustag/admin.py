from django.contrib import admin

from .models import YouthForumData

# Register your models here.

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3


class YouthForumDataAdmin(admin.ModelAdmin):
    # 定义列表页显示元数据字段
    list_display = ('question_text', 'first_class', 'second_class',
                    'was_tagged_manually')
    # 定义可链接元数据字段
    list_display_links = ('question_text', )
    # 定义再列表页可编辑字段
    list_editable = ('first_class', 'second_class')
    # 定义列表页右侧过滤字段
    list_filter = [
        'first_class',
    ]
    # 列表页每页显示数据量
    list_per_page = 15
    # 定义列表页搜索候选元数据
    search_fields = [
        'question_text',
    ]
    fieldsets = [
        (None, {
            'fields': ['question_text', 'first_class', 'second_class']
        }),
        ('Date information', {
            'fields': ['pub_date'],
            'classes': ['collapse']
        }),
    ]


admin.site.register(YouthForumData, YouthForumDataAdmin)
