from __future__ import annotations

from django.db import models
from django.db.models import QuerySet

from pitter.models.base import BaseModel


class Client(BaseModel):
    login = models.CharField(max_length=31, default="user")
    password = models.TextField(max_length=15, default='password')
    email_address=models.TextField()
    enable_notifications=models.BooleanField()

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
        )

    @staticmethod
    def create_user(login: str, password: str, email_address: str, enable_notifications: bool) -> Client:
        return Client.objects.create(
            login=login,
            password=password,
            email_address=email_address,
            enable_notifications=enable_notifications,
        )

    @staticmethod
    def get_clients() -> QuerySet:
        return Client.objects.find().order_by('created_at')

class Pitt(BaseModel):
    user_id=models.ForeignKey('Client', on_delete=models.CASCADE)
    audio_file_path=models.FilePathField()
    speech_transcription=models.CharField(max_length=256)

class Follower(BaseModel):
    user_id=models.ManyToManyField('Client')
