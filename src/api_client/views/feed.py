from typing import Dict

from django.core.paginator import Paginator
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from pitter import exceptions
from pitter.decorators import response_dict_serializer
from pitter.utils import check_token
from pitter.utils import create_feed
from pitter.models import Pitt
from pitter.models import Client
from api_client.validation_serializers import FeedGetResponse


class FeedView(APIView):
    @classmethod
    @response_dict_serializer(FeedGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: client'],
        operation_summary='Удаление pitt\'а',
        operation_description='Удаление pitt\'а пользователя',
    )
    def get(cls, request, login, page) -> Dict[str, dict]:
        check_token(request)
        try:
            client = Client.objects.get(login=login)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()

        try:
            following = client.followings.first()
        except None:
            raise exceptions.NoFollowersError()

        feed = create_feed(client)
        paginator = Paginator(feed, 10)
        if page < paginator.num_pages or page > paginator.num_pages:
            raise exceptions.PageError
        else:
            current_page = paginator.page(page)

        return dict(feed=current_page.object_list,)
