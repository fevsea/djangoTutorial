from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from polls.models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # Cannot be deleted


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (_('Date information'), {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']  # Filter sidebar
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)

admin.site.site_header = _('Polls administration')
admin.site.site_title = _('Polls admin site')
