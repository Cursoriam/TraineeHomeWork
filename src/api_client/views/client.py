from typing import Dict


from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView


from src.api_client.validation_serializers import ClientPostRequest
from src.api_client.validation_serializers import ClientPostResponse
from src.pitter import exceptions
from src.pitter.decorators import request_post_serializer, response_dict_serializer
from src.pitter.integrations import GoogleSTT

class ClientView(APIView):
    parser_classes = [MultiPartParser]
    
    @classmethod
    @request_post_serializer(ClientPostRequest)
    @response_dict_serializer(ClientPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=ClientPostRequest,
        responses={
            200: ClientPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Преобразование речи в текст',
        operation_description='Преобразование речи в текст с использованием Google STT',
    )
    def post(cls, request) -> Dict[str, str]:
        transcripted: str = GoogleSTT.transcript(request.data['file'].read())

        return dict(result=transcripted)

        
        

