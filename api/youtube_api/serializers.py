from rest_framework import serializers

from .models import YoutubeData

class YoutubeVideoSerializer(serializers.ModelSerializer):
	class Meta:
		model = YoutubeData
		fields = ['title', 'published_at', 'description', 'thumbnail_urls']