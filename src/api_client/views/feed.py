from typing import Dict

from django.core.paginator import Paginator
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from pitter import exceptions
from pitter.decorators import response_dict_serializer
from pitter.utils import check_token
from pitter.utils import create_feed
from api_client.validation_serializers import FeedGetResponse


class FeedView(APIView):
    @classmethod
    @response_dict_serializer(FeedGetResponse)
    @swagger_auto_schema(
        tags=['Client: feed'],
        responses={
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Лента',
        operation_description='Лента пользователя',
    )
    def get(cls, request, page) -> Dict[str, list]:
        """
        Запрос на демонстрацию ленты
        :param request:
        :param page:
        :return:
        """
        client = check_token(request)

        following = client.followings.first()

        if not following:
            raise exceptions.NoFollowersError()

        feed = create_feed(client)
        paginator = Paginator(feed, 25)

        if page < paginator.num_pages or page > paginator.num_pages:
            raise exceptions.PageError
        else:
            current_page = paginator.page(page)

        return dict(feed=current_page.object_list,)
