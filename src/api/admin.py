from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from .models import (
    Predication
)


class PredicationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'age', 'gender')}),
        (_('Readings'), {'fields': (
            'resting_bp_s', 'cholestrol', 'fasting_blood_sugar', 'old_peak', 'st_slope', 'exercise_angina',
            'max_heart_rate', 'resting_ecg')}),
        (_('Sensors'), {'fields': ('chest_pain_type', 'target')}),
    )
    list_display = ['pk', 'user', 'age', 'gender', 'chest_pain_type', 'cholestrol', 'created_on']
    list_filter = ['target', 'st_slope', 'exercise_angina', 'resting_ecg']


admin.site.register(Predication, PredicationAdmin)
