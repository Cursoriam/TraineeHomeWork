from rest_framework import serializers


class FeedGetResponse(serializers.Serializer):
    feed = serializers.ListField()
