from django.contrib import admin
from .models import Habit, HabitLog, DailyReflection


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'frequency', 'tracking_type', 'is_active', 'created_at']
    list_filter = ['frequency', 'tracking_type', 'is_active', 'created_at']
    search_fields = ['name', 'user__email']
    readonly_fields = ['created_at']


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'value', 'completed', 'created_at']
    list_filter = ['completed', 'date', 'created_at']
    search_fields = ['habit__name', 'habit__user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(DailyReflection)
class DailyReflectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'day_rating', 'mood', 'mood_intensity', 'created_at']
    list_filter = ['mood', 'date', 'created_at']
    search_fields = ['user__email', 'notes', 'gratitude']
    readonly_fields = ['created_at', 'updated_at', 'mood_score']
    date_hierarchy = 'date'

