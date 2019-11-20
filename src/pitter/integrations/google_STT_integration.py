import magic


from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


from src.pitter.exceptions import ValidationError

class GoogleSTT:
    @classmethod
    def transcript(cls, audio: bytes) -> str:
        mime_type=magic.from_buffer(audio, mime=True)

        if mime_type not in ['audio/flac', 'audio/x-wav']:
            raise ValidationError(message='Invalid type',status_code=415)

        RATE: int = 8000 # audio rate

        # Instantiates a client
        client = speech.SpeechClient()
        content = audio
        audio_data = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code='en-US')

        # Detects speech in the audio file
        response = client.recognize(config, audio_data)
        transcripted: str = ' '
        for result in response.results:
            transcripted=transcripted+result.alternatives[0].transcript
        
        return transcripted

