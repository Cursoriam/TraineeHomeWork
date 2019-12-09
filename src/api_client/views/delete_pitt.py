from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from pitter import exceptions
from pitter.utils import check_token
from pitter.models import Pitt


class DeletePittView(APIView):
    @classmethod
    @swagger_auto_schema(
        tags=['Pitt: delete_pitt'],
        responses={
            204: exceptions.ExceptionResponse,
            403: exceptions.ExceptionResponse,
            400: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление pitt\'а',
        operation_description='Удаление pitt\'а пользователя',
    )
    def delete(cls, request, pitt_id):
        """
        Запрос на удаление pitt'a
        :param request:
        :param login:
        :param pitt_id:
        :return:
        """
        client = check_token(request)
        try:
            pitt = Pitt.objects.get(id=pitt_id)
        except Pitt.DoesNotExist:
            raise exceptions.InvalidUserError(message='Ivalid pitt_id')

        try:
            Pitt.objects.get(user_id=client.id, id=pitt_id)
        except Pitt.DoesNotExist:
            raise exceptions.InvalidUserError(message='Forbidden', status_code=403)

        pitt.delete()
        client.pitts.filter(id=pitt_id).delete()

        try:
            Pitt.objects.get(id=pitt_id)
        except Pitt.DoesNotExist:
            raise exceptions.InvalidUserError(message='Pitt successfully '
                                                      'deleted',
                                              status_code=204)
