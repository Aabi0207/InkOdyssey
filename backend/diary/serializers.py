from rest_framework import serializers
from .models import DiaryEntry, ContentBlock


class ContentBlockSerializer(serializers.ModelSerializer):
    """Serializer for ContentBlock model"""
    
    class Meta:
        model = ContentBlock
        fields = (
            'id',
            'block_type',
            'order',
            'text_content',
            'media_file',
            'media_url',
            'caption',
            'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def validate(self, data):
        """Validate that the content matches the block type"""
        block_type = data.get('block_type')
        text_content = data.get('text_content')
        media_file = data.get('media_file')
        media_url = data.get('media_url')
        
        if block_type == 'text' and not text_content:
            raise serializers.ValidationError(
                {'text_content': 'Text blocks must have text content.'}
            )
        elif block_type in ['image', 'video'] and not (media_file or media_url):
            raise serializers.ValidationError(
                {'media_file': f'{block_type.capitalize()} blocks must have a media file or URL.'}
            )
        
        return data


class DiaryEntrySerializer(serializers.ModelSerializer):
    """Serializer for DiaryEntry model with nested content blocks"""
    
    content_blocks = ContentBlockSerializer(many=True, read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = DiaryEntry
        fields = (
            'id',
            'title',
            'author',
            'author_email',
            'author_name',
            'content_blocks',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')


class DiaryEntryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating diary entries with content blocks"""
    
    content_blocks = ContentBlockSerializer(many=True, required=False)
    
    class Meta:
        model = DiaryEntry
        fields = ('id', 'title', 'content_blocks', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        """Create diary entry with content blocks"""
        content_blocks_data = validated_data.pop('content_blocks', [])
        
        # Create the diary entry
        diary_entry = DiaryEntry.objects.create(**validated_data)
        
        # Create content blocks
        for block_data in content_blocks_data:
            ContentBlock.objects.create(diary_entry=diary_entry, **block_data)
        
        return diary_entry
    
    def update(self, instance, validated_data):
        """Update diary entry and optionally update content blocks"""
        content_blocks_data = validated_data.pop('content_blocks', None)
        
        # Update diary entry fields
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        # If content blocks are provided, delete old ones and create new ones
        if content_blocks_data is not None:
            instance.content_blocks.all().delete()
            for block_data in content_blocks_data:
                ContentBlock.objects.create(diary_entry=instance, **block_data)
        
        return instance


class DiaryEntryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing diary entries"""
    
    author_email = serializers.EmailField(source='author.email', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    content_blocks_count = serializers.IntegerField(
        source='content_blocks.count',
        read_only=True
    )
    
    class Meta:
        model = DiaryEntry
        fields = (
            'id',
            'title',
            'author_email',
            'author_name',
            'content_blocks_count',
            'created_at',
            'updated_at'
        )
        read_only_fields = fields
