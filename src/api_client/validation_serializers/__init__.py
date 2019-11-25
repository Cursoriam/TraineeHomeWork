from typing import List, Callable

from .client_serializers import ClientPostRequest
from .client_serializers import ClientPostResponse
from .client_serializers import ClientLoginRequest

__all__: List[Callable] = [
    'ClientPostRequest',
    'ClientPostResponse',
    'ClientLoginRequest',
]
