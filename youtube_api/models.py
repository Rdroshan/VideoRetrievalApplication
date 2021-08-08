from django.db import models

# Create your models here.
class YoutubeData(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	video_id = models.CharField(max_length=16)
	published_at = models.DateTimeField()
	channel_id = models.CharField(max_length=64)
	title = models.TextField()
	description = models.TextField()
	thumbnail_urls = models.JSONField(default=dict)

	class Meta:
		app_label = 'youtube_api'
		db_table = 'youtube'
