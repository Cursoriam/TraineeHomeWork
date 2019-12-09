from rest_framework import serializers


class SearchPostRequest(serializers.Serializer):
    search_string = serializers.CharField()


class SearchPostResponse(serializers.Serializer):
    result = serializers.ListField()
