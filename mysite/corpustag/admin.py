from django.contrib import admin
from .models import YouthForumData, YouthFirstCate, YouthSecondCate
# Register your models here.


class YouthFirstCateAdmin(admin.ModelAdmin):
    # 定义列表页显示元数据字段
    list_display = ('name', 'modified',)
    # 定义可链接元数据字段
    list_display_links = ('modified', )
    # 定义再列表页可编辑字段
    list_editable = ('name', )
    # 定义列表页右侧过滤字段
    list_filter = [
        'name',
    ]
    # 列表页每页显示数据量
    list_per_page = 15
    # 定义列表页搜索候选元数据
    search_fields = [
        'name',
    ]
    fieldsets = [
        (None, {
            'fields': ['name', ]
        }),
        ('Date information', {
            'fields': ['created', 'modified'],
            'classes': ['grp-collapse grp-open']
        }),
    ]


class YouthSecondCateAdmin(admin.ModelAdmin):
    # 定义列表页显示元数据字段
    list_display = ('first_class', 'name', 'modified',)
    # 定义可链接元数据字段
    list_display_links = ('modified', )
    # 定义再列表页可编辑字段
    list_editable = ('name',)
    # 定义列表页右侧过滤字段
    list_filter = [
        'first_class',
    ]
    # 列表页每页显示数据量
    list_per_page = 15
    # 定义列表页搜索候选元数据
    search_fields = [
        'name',
    ]
    fieldsets = [
        (None, {
            'fields': ['first_class', 'name', ]
        }),
        ('Date information', {
            'fields': ['created', 'modified'],
            'classes': ['grp-collapse grp-open']
        }),
    ]


class YouthForumDataAdmin(admin.ModelAdmin):
    # 定义列表页显示元数据字段
    list_display = ('question_text',
                    'first_class',
                    'second_class',
                    'tags',
                    # 'mlHit',
                    'was_tagged_manually',
                    'was_check_manually'
                    )
    # 定义可链接元数据字段
    list_display_links = ('question_text', )
    # 定义再列表页可编辑字段
    list_editable = ('first_class', 'second_class', 'tags')
    # 定义列表页右侧过滤字段
    list_filter = [
        'first_class',
        'mlHit',
    ]
    # 列表页每页显示数据量
    list_per_page = 15
    # 定义列表页搜索候选元数据
    search_fields = [
        'question_text',
        # foreign_key__related_fieldname
        'second_class__name',
        'tags__name'
    ]
    fieldsets = [
        (None, {
            'fields': ['question_text', 'first_class', 'second_class', 'tags', 'mlHit']
        }),
        ('Date information', {
            'fields': ['created', 'modified'],
            'classes': ['grp-collapse grp-open']
        }),
    ]


admin.site.register(YouthForumData, YouthForumDataAdmin)
admin.site.register(YouthFirstCate, YouthFirstCateAdmin)
admin.site.register(YouthSecondCate, YouthSecondCateAdmin)
