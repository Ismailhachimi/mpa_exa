from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Q

from rest_framework import exceptions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from events.api.serializers import *
from events.api.permissions import *
from events.models import Event

from accounts.models import User
from accounts.services import JWTAuthentication
from accounts.api.permissions import IsClient


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    authentication_classes = (JWTAuthentication, SessionAuthentication, )
    permission_classes = []

    # View Setup
    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateEventSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateEventSerializer
        return EventSerializer

    def get_queryset(self):
        user: User = self.request.user
        return self.queryset.filter(Q(client=user) | Q(expert=user))

    def get_permissions(self):
        """
        when creating|updateing an event,
            check whether the consult.  already has an available slot
        """
        permission_classes = [IsAuthenticated]

        if self.action in ['create', 'destroy']:
            permission_classes = [IsClient]
        return [permission() for permission in permission_classes]

    # Main Actions
    def create(self, request, *args, **kwargs):
        serializer: CreateEventSerializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        expert = serializer.validated_data['expert']
        start = serializer.validated_data['main_start']
        end = serializer.validated_data['main_end']

        # you can make a reservation at least one hour before the start
        if datetime.now(start.tzinfo) >= start - timedelta(hours=1) or start >= end:
            return Response(
                data={'message': 'Invalid start and end dates'},
                status=status.HTTP_400_BAD_REQUEST)

        if expert.groups.filter(name='freelancer').exists():

            if expert.isAvailable(start, end):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )
            else:
                return Response(
                    data={'message': 'Expert is not available'},
                    status=status.HTTP_409_CONFLICT
                )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # TODO : check availability
        # TODO : add expert validation
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # TODO : maybe replace destroy by cancel and fitler after over the status
        instance: Event = self.get_object()
        if instance.client == request.user:
            event_date = instance.main_start
            cancel_date = datetime.now(event_date.tzinfo) + timedelta(days=2)
            if event_date > cancel_date:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                message = "You can't cancel under 48 hours before your meeting."
                return Response(
                    data={'message': message},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def perform_destroy(self, instance):
        instance.delete()
