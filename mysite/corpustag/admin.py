from django.contrib import admin
from .models import YouthForumData, YouthFirstCate, YouthSecondCate
# Register your models here.


class YouthFirstCateAdmin(admin.ModelAdmin):
    # 定义列表页显示元数据字段
    list_display = ('name', 'pub_date',)
    # 定义可链接元数据字段
    list_display_links = ('pub_date', )
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
            'fields': ['pub_date'],
            'classes': ['grp-collapse grp-open']
        }),
    ]


class YouthSecondCateAdmin(admin.ModelAdmin):
    # 定义列表页显示元数据字段
    list_display = ('first_class', 'name', 'pub_date',)
    # 定义可链接元数据字段
    list_display_links = ('pub_date', )
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
            'fields': ['pub_date'],
            'classes': ['grp-collapse grp-open']
        }),
    ]


class YouthForumDataAdmin(admin.ModelAdmin):
    # 定义列表页显示元数据字段
    list_display = ('question_text', 'first_class', 'second_class',
                    'was_tagged_manually')
    # 定义可链接元数据字段
    list_display_links = ('question_text', )
    # 定义再列表页可编辑字段
    list_editable = ('first_class', 'second_class', )
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
            'classes': ['grp-collapse grp-open']
        }),
    ]


admin.site.register(YouthForumData, YouthForumDataAdmin)
admin.site.register(YouthFirstCate, YouthFirstCateAdmin)
admin.site.register(YouthSecondCate, YouthSecondCateAdmin)
