from rest_framework import serializers
from .models import Habit, HabitLog, DailyReflection


class HabitSerializer(serializers.ModelSerializer):
    """
    Serializer for Habit model.
    """
    logs_count = serializers.SerializerMethodField()
    current_streak = serializers.SerializerMethodField()
    
    class Meta:
        model = Habit
        fields = [
            'id', 'name', 'description', 'frequency', 'tracking_type',
            'target_value', 'color', 'icon', 'created_at', 'is_active',
            'logs_count', 'current_streak'
        ]
        read_only_fields = ['created_at']
    
    def get_logs_count(self, obj):
        """Total number of logs for this habit"""
        return obj.logs.count()
    
    def get_current_streak(self, obj):
        """Calculate current streak of consecutive days"""
        from django.utils import timezone
        from datetime import timedelta
        
        logs = obj.logs.filter(completed=True).order_by('-date')
        if not logs.exists():
            return 0
        
        streak = 0
        current_date = timezone.now().date()
        
        for log in logs:
            if log.date == current_date or log.date == current_date - timedelta(days=1):
                streak += 1
                current_date = log.date - timedelta(days=1)
            else:
                break
        
        return streak
    
    def create(self, validated_data):
        """Automatically assign the user from the request"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class HabitLogSerializer(serializers.ModelSerializer):
    """
    Serializer for HabitLog model.
    """
    habit_name = serializers.CharField(source='habit.name', read_only=True)
    habit_color = serializers.CharField(source='habit.color', read_only=True)
    habit_tracking_type = serializers.CharField(source='habit.tracking_type', read_only=True)
    habit_target_value = serializers.IntegerField(source='habit.target_value', read_only=True)
    
    class Meta:
        model = HabitLog
        fields = [
            'id', 'habit', 'habit_name', 'habit_color', 'habit_tracking_type',
            'habit_target_value', 'date', 'value', 'completed', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        """Ensure the habit belongs to the current user"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            habit = data.get('habit')
            if habit and habit.user != request.user:
                raise serializers.ValidationError("You can only log your own habits.")
        return data
    
    def create(self, validated_data):
        """Auto-mark as completed if value >= target for counter habits"""
        habit = validated_data['habit']
        value = validated_data.get('value', 0)
        
        if habit.tracking_type == 'counter':
            validated_data['completed'] = value >= habit.target_value
        elif habit.tracking_type == 'boolean':
            validated_data['completed'] = value >= 1
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Auto-mark as completed if value >= target for counter habits"""
        habit = instance.habit
        value = validated_data.get('value', instance.value)
        
        if habit.tracking_type == 'counter':
            validated_data['completed'] = value >= habit.target_value
        elif habit.tracking_type == 'boolean':
            validated_data['completed'] = value >= 1
        
        return super().update(instance, validated_data)


class DailyReflectionSerializer(serializers.ModelSerializer):
    """
    Serializer for DailyReflection model.
    """
    mood_score = serializers.ReadOnlyField()
    
    class Meta:
        model = DailyReflection
        fields = [
            'id', 'date', 'day_rating', 'mood', 'mood_intensity',
            'notes', 'gratitude', 'mood_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Automatically assign the user from the request"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, data):
        """Ensure user doesn't create multiple reflections for the same date"""
        request = self.context.get('request')
        date = data.get('date')
        
        if request and hasattr(request, 'user') and date:
            # Check if updating existing instance
            if self.instance:
                # Allow update of the same instance
                if DailyReflection.objects.filter(
                    user=request.user, date=date
                ).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError(
                        "A reflection for this date already exists."
                    )
            else:
                # Creating new instance
                if DailyReflection.objects.filter(user=request.user, date=date).exists():
                    raise serializers.ValidationError(
                        "A reflection for this date already exists."
                    )
        
        return data
