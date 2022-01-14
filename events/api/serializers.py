from rest_framework.serializers import ModelSerializer
from events import models


class EventSerializer(ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class CreateEventSerializer(ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            'expert',
            'main_start', 'main_end',
            'title', 'description'
        ]
        extra_kwargs = {'expert': {'required': True}}


class UpdateEventSerializer(ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            'main_start', 'main_end',
            'title', 'description',
        ]
