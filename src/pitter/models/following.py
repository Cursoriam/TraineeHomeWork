from __future__ import annotations

from django.db import models
from django.db.models import QuerySet

from pitter.models.base import BaseModel


class Following(BaseModel):
    following_id = models.CharField(max_length=50, default='')
    follower_id = models.CharField(max_length=50, default='')

    @staticmethod
    def to_dict(self):
        return dict(
            following_id=self.following_id,
            follower_id=self.follower_id,
        )

    @staticmethod
    def create_following(following_id: str, follower_id: str):
        return Following.objects.create(
            following_id=following_id,
            follower_id=follower_id,
        )

    @staticmethod
    def get_follows() -> QuerySet:
        return Following.objects.find().order_by('created_at')

    def __str__(self):
        return self.follower_id
