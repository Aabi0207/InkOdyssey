from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Count, Avg, Sum, Q
from .models import Habit, HabitLog, DailyReflection
from .serializers import HabitSerializer, HabitLogSerializer, DailyReflectionSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing habits.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only the user's habits"""
        return Habit.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active habits"""
        habits = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle the active status of a habit"""
        habit = self.get_object()
        habit.is_active = not habit.is_active
        habit.save()
        serializer = self.get_serializer(habit)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific habit"""
        habit = self.get_object()
        logs = habit.logs.all()
        
        total_logs = logs.count()
        completed_logs = logs.filter(completed=True).count()
        completion_rate = (completed_logs / total_logs * 100) if total_logs > 0 else 0
        
        # Get logs for the last 30 days
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_logs = logs.filter(date__gte=thirty_days_ago)
        
        # Calculate average value for counter habits
        avg_value = recent_logs.aggregate(Avg('value'))['value__avg'] or 0
        
        return Response({
            'total_logs': total_logs,
            'completed_logs': completed_logs,
            'completion_rate': round(completion_rate, 2),
            'average_value': round(avg_value, 2),
            'last_30_days_logs': recent_logs.count(),
        })


class HabitLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing habit logs.
    """
    serializer_class = HabitLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only logs for the user's habits"""
        habit_id = self.request.query_params.get('habit', None)
        date = self.request.query_params.get('date', None)
        
        queryset = HabitLog.objects.filter(habit__user=self.request.user)
        
        if habit_id:
            queryset = queryset.filter(habit_id=habit_id)
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                pass
        
        return queryset.select_related('habit')
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get all habit logs for today"""
        today = timezone.now().date()
        logs = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def log_habit(self, request):
        """
        Quick log a habit for today.
        Expects: { "habit_id": 1, "value": 1 }
        """
        habit_id = request.data.get('habit_id')
        value = request.data.get('value', 1)
        notes = request.data.get('notes', '')
        
        if not habit_id:
            return Response(
                {'error': 'habit_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
        except Habit.DoesNotExist:
            return Response(
                {'error': 'Habit not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        today = timezone.now().date()
        
        # Get or create log for today
        log, created = HabitLog.objects.get_or_create(
            habit=habit,
            date=today,
            defaults={'value': value, 'notes': notes}
        )
        
        if not created:
            # Update existing log
            if habit.tracking_type == 'counter':
                log.value += value
            else:
                log.value = value
            log.notes = notes
            log.completed = log.value >= habit.target_value
            log.save()
        
        serializer = self.get_serializer(log)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def date_range(self, request):
        """
        Get logs for a date range.
        Query params: start_date, end_date (YYYY-MM-DD)
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logs = self.get_queryset().filter(date__gte=start, date__lte=end)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)


class DailyReflectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing daily reflections.
    """
    serializer_class = DailyReflectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only the user's reflections"""
        date = self.request.query_params.get('date', None)
        queryset = DailyReflection.objects.filter(user=self.request.user)
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                pass
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's reflection if it exists"""
        today = timezone.now().date()
        try:
            reflection = DailyReflection.objects.get(user=request.user, date=today)
            serializer = self.get_serializer(reflection)
            return Response(serializer.data)
        except DailyReflection.DoesNotExist:
            return Response(
                {'message': 'No reflection for today yet'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get overall reflection statistics"""
        reflections = self.get_queryset()
        
        # Get last 30 days
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_reflections = reflections.filter(date__gte=thirty_days_ago)
        
        avg_day_rating = recent_reflections.aggregate(Avg('day_rating'))['day_rating__avg'] or 0
        avg_mood_intensity = recent_reflections.aggregate(Avg('mood_intensity'))['mood_intensity__avg'] or 0
        
        # Count moods
        mood_counts = recent_reflections.values('mood').annotate(count=Count('mood'))
        
        return Response({
            'total_reflections': reflections.count(),
            'last_30_days': recent_reflections.count(),
            'average_day_rating': round(avg_day_rating, 2),
            'average_mood_intensity': round(avg_mood_intensity, 2),
            'mood_distribution': list(mood_counts),
        })
    
    @action(detail=False, methods=['get'])
    def date_range(self, request):
        """
        Get reflections for a date range.
        Query params: start_date, end_date (YYYY-MM-DD)
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reflections = self.get_queryset().filter(date__gte=start, date__lte=end)
        serializer = self.get_serializer(reflections, many=True)
        return Response(serializer.data)

