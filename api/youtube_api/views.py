from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# app level imports
from .models import YoutubeData
from .services import YoutubeService
from .serializers import YoutubeVideoSerializer


@api_view(http_method_names=["GET"])
def get_all_videos_data(request):

	youtube_videos_data = YoutubeService.get_all_videos()

	# paginator class
	paginator = PageNumberPagination()
	paginator.page_size = 10
	response = paginator.paginate_queryset(youtube_videos_data, request)
	return Response(YoutubeVideoSerializer(response, many=True).data)



@api_view(http_method_names=["GET"])
def search_videos(request):
	search_query = request.query_params.get('search_query')
	if not search_query:
		# Fetch all the results with pagination
			youtube_videos_data = YoutubeService.get_all_videos()
	else:
		youtube_videos_data = YoutubeService.get_videos(title_desc_search=search_query)

	# paginator class
	paginator = PageNumberPagination()
	paginator.page_size = 10
	response = paginator.paginate_queryset(youtube_videos_data, request)
	return Response(YoutubeVideoSerializer(response, many=True).data)


@api_view(http_method_names=["POST"])
def cron_fetch_and_store(request):
	YoutubeService.fetch_videos_and_store()
	return Response({})
