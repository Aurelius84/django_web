from django.contrib import admin

from .models import YouthForumData

# Register your models here.


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3


class YouthForumDataAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'first_class', 'second_class', 'was_tagged_manually')
    list_display_links = ('question_text',)
    list_editable = ('first_class', 'second_class')
    list_filter = ['first_class', 'second_class']
    search_fields = ['question_text']
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
