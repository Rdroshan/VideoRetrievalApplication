# django and python imports
from django.conf import settings
from django.db.models import Q
import requests
from dateutil import parser
from django.db import IntegrityError

# app level imports
from .models import YoutubeData

# import logging
import logging
logger = logging.getLogger(__name__)


class YoutubeService:

	@staticmethod
	def get_all_videos():
		youtube_videos_data = YoutubeData.objects.all().order_by('-published_at')
		return youtube_videos_data

	@staticmethod
	def get_videos(title_desc_search):

		or_query_creation = Q()
		for search_query in title_desc_search.split(' '):
			or_query_creation |= Q(title__icontains=search_query) | Q(description__icontains=search_query)
		return YoutubeData.objects.filter(or_query_creation)

	@staticmethod
	def fetch_videos_and_store():
		# make a request call to fetch the youtube data
		google_api_keys = settings.GOOGLE_API_KEYS

		response = {}
		for api_key in google_api_keys:

			try:
				response = requests.get(f'https://www.googleapis.com/youtube/v3/search/?part=snippet&order=date&key={api_key}&type=video&q=sports&relevanceLanguage=en&publishedAfter=2021-08-07T00:00:00Z')
				# logger.info(f"youtube Response: {response}")
			except Exception as e:
				# setup logging to track what kind of error came
				logger.info(f"youtube_fetch_job - Exception: {str(e)}")
				continue

			if response.status_code in [400, 403]:
				# log the message and try with the next key
				logger.info(f"youtube_fetch_job - status code in 400 or 403 response: {response}")
				continue
			else:
				response = response.json()
				break

		# Store the data, If response is valid
		"""
		Response structure:
			{
				'items': [
					{
						'id': {'kind': 'youtube#video', 'videoId': '3fKU7ugHcIQ'},
						'snippet': {
								'publishedAt': '2021-08-08T07:30:00Z',
							    'channelId': 'UCR4z8ccOWNoUThB4VAMNBTg',
							    'title': 'Hotstar Specials The Empire | Official Trailer | REACTION!!!!',
							    'description': 'HELP WITH THE COVID situation IN INDIA HERE! https://fundraisers.giveindia.org/fundraisers/togetherforindia-stop-the-spread-help-india-fight-covid-19 ...',
							    'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/3fKU7ugHcIQ/default.jpg',
							      'width': 120,
							      'height': 90},
							     'medium': {'url': 'https://i.ytimg.com/vi/3fKU7ugHcIQ/mqdefault.jpg',
							      'width': 320,
							      'height': 180},
							     'high': {'url': 'https://i.ytimg.com/vi/3fKU7ugHcIQ/hqdefault.jpg',
							      'width': 480,
							      'height': 360}},
							    'channelTitle': 'OUR STUPID REACTIONS',
							    'liveBroadcastContent': 'none',
							    'publishTime': '2021-08-08T07:30:00Z'
						}
					}
				]
			}
		"""

		if not response:
			logger.info(f"No response")
			return 

		try:
			# Get the data required
			videos_data = response['items']
			youtube_data = []
			for video_item in videos_data:
				video_id = video_item['id']['videoId']

				# Video snippet contains all the data
				video_snippet = video_item['snippet']

				published_at = parser.parse(video_snippet['publishedAt'])
				channel_id = video_snippet['channelId']
				title = video_snippet['title']
				desc = video_snippet['description']
				thumbnails = video_snippet['thumbnails']

				thumbnail_urls = {}
				for thumbnail_type, url_data in thumbnails.items():
					thumbnail_urls[thumbnail_type] = url_data['url']

				youtube_data.append(
					YoutubeData(
						video_id=video_id,
						published_at=published_at,
						channel_id=channel_id,
						title=title,
						description=desc,
						thumbnail_urls=thumbnail_urls
					)
				)
				logger.info(f"youtube data created: {len(youtube_data)}")
		except Exception as e:
			logger.info(f"Exception occured while processing response error: {e}")
			return

		# Create data in DB
		if youtube_data:
			try:
				records_created = YoutubeData.objects.bulk_create(youtube_data, ignore_conflicts=True)
				logger.info(f"Records created: {records_created}")
			except IntegrityError as i:
				logger.info(f"Record creation failed due to integrity error: {i}")
				return
