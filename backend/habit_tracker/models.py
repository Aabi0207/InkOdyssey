from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):
    """
    Represents a habit that a user wants to track.
    """
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    )
    
    TRACKING_TYPE_CHOICES = (
        ('boolean', 'Yes/No (One-time mark)'),
        ('counter', 'Counter (Multiple times)'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    tracking_type = models.CharField(max_length=20, choices=TRACKING_TYPE_CHOICES, default='boolean')
    target_value = models.PositiveIntegerField(
        default=1,
        help_text='Target value for counter type habits (e.g., 8 glasses of water)'
    )
    color = models.CharField(max_length=7, default='#2980B9', help_text='Hex color code for visual representation')
    icon = models.CharField(max_length=50, blank=True, help_text='Icon name or emoji')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"


class HabitLog(models.Model):
    """
    Represents a log entry for a habit on a specific date.
    """
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    date = models.DateField(default=timezone.now)
    value = models.PositiveIntegerField(
        default=0,
        help_text='1 for boolean habits, actual count for counter habits'
    )
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Habit Log'
        verbose_name_plural = 'Habit Logs'
        unique_together = [['habit', 'date']]
        ordering = ['-date']
        indexes = [
            models.Index(fields=['habit', '-date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.habit.name} - {self.date} - {self.value}"


class DailyReflection(models.Model):
    """
    Represents daily reflection questions and mood tracking.
    """
    MOOD_CHOICES = (
        ('terrible', 'Terrible'),
        ('bad', 'Bad'),
        ('okay', 'Okay'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
        ('peak', 'Peak'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_reflections'
    )
    date = models.DateField(default=timezone.now)
    
    # Day rating (1-10)
    day_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Rate your day from 1-10'
    )
    
    # Overall mood
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    mood_intensity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text='Intensity of the mood from 1-10'
    )
    
    # Optional notes
    notes = models.TextField(blank=True, help_text='Additional thoughts or reflections')
    
    # Gratitude (optional)
    gratitude = models.TextField(blank=True, help_text='What are you grateful for today?')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Daily Reflection'
        verbose_name_plural = 'Daily Reflections'
        unique_together = [['user', 'date']]
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.mood}"
    
    @property
    def mood_score(self):
        """Calculate mood score based on mood and intensity"""
        mood_base_scores = {
            'terrible': 1,
            'bad': 3,
            'okay': 5,
            'good': 7,
            'excellent': 9,
            'peak': 10,
        }
        base = mood_base_scores.get(self.mood, 5)
        # Adjust by intensity (normalize to 0-1 range and apply)
        adjusted = base + (self.mood_intensity / 10) * 2
        return min(10, max(1, adjusted))

