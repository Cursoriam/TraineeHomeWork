from __future__ import annotations

from django.db import models

from pitter.models.base import BaseModel


class Pitt(BaseModel):
    user_id = models.CharField(max_length=50)
    audio_file_path = models.FilePathField()
    speech_transcription = models.CharField(max_length=1024)

    @staticmethod
    def create_pitt(user_id: str, audio_file_path: str,
                    speech_transcription: str):
        return Pitt.objects.create(
            user_id=user_id,
            audio_file_path=audio_file_path,
            speech_transcription=speech_transcription,
        )
