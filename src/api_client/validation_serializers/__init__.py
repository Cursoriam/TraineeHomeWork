from typing import List, Callable

from .client_serializers import ClientPostRequest
from .client_serializers import ClientPostResponse

__all__: List[Callable] = [
    'ClientPostRequest',
    'ClientPostResponse',
]
