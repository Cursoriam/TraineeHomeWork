from typing import Dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from pitter import exceptions
from pitter.utils import check_token
from pitter.models import Pitt
from pitter.models import Client


class DeletePittView(APIView):
    @classmethod
    @swagger_auto_schema(
        tags=['Pitter: client'],
        operation_summary='Удаление pitt\'а',
        operation_description='Удаление pitt\'а пользователя',
    )
    def delete(cls, request, login, pitt_id):
        check_token(request)
        try:
            client = Client.objects.get(login=login)
        except Client.DoesNotExist:
            raise exceptions.InvalidUserError()

        try:
            pitt = Pitt.objects.get(pitt_id=pitt_id)
        except Pitt.DoesNotExist:
            raise exceptions.InvalidUserError(message='Ivalid pitt_id')

        pitt.delete()
        client.pitts.filter(pitt_id=pitt_id).delete()

        try:
            pitt = Pitt.objects.get(pitt_id=pitt_id)
        except Pitt.DoesNotExist:
            raise exceptions.InvalidUserError(message='Pitt deleted', status_code=204)
