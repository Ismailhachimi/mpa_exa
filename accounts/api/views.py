#
import jwt

import coreapi
import coreschema

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

from rest_framework import exceptions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, NOT
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes, schema
from rest_framework.authentication import SessionAuthentication
from rest_framework.schemas import AutoSchema, ManualSchema

from accounts.api.permissions import IsUserOrOwnerOrAdmin, IsClient
from accounts.api.serializers import *

from accounts.models import User
from accounts.services import generate_access_token, generate_refresh_token
from accounts.services import JWTAuthentication


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True).order_by('joined_at')

    authentication_classes = (JWTAuthentication, SessionAuthentication, )
    permission_classes = []

    def get_serializer_class(self):
        if self.action in ['list']:
            return ListUserSerializer
        if self.action in ['create']:
            return CreateUserSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return RetrieveUserSerializer

    def get_queryset(self):
        user = self.request.user
        # skill = self.kwargs.get("skill")
        # queryset.filter(skill=skill)
        if self.action in ['list']:
            return self.queryset.filter(groups__name='freelancer')
        if self.action in ['create', 'update', 'partial_update']:
            return self.queryset
        return self.queryset

    def get_permissions(self):
        permission_classes = []

        if self.action in ['create']:
            return [NOT(IsAuthenticated())]

        if self.action in ['list']:
            permission_classes = [IsAuthenticated, IsClient]

        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsUserOrOwnerOrAdmin]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

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
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    @action(methods=['GET'], detail=False, url_path='current')
    # @method_decorator(csrf_protect)
    # TODO : find whether csrf is needed and how to make it work
    def get_current_user(self, request, *args, **kwargs):
        user = request.user
        serialized_user = RetrieveUserSerializer(user).data
        return Response(serialized_user)


get_token_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form",
                  type="string", description="email here"),
    coreapi.Field("password", required=True, location="form",
                  type="string", description="password field")
])


@api_view(['POST'])
@permission_classes([AllowAny])
@schema(get_token_schema)
@ensure_csrf_cookie  # make django send a csrftoken cookie with a response,
def get_token(request):
    email = request.data.get('email')
    password = request.data.get('password')

    response = Response()
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'email and password required')

    user = User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is not activated')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')

    return get_token_response(user)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token(request):
    """
    Note: X-CSRFTOKEN is needed in headers for this view
    """
    response = Response()

    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    return get_token_response(user)


def get_token_response(user: User):
    response = Response()
    serialized_user = RetrieveUserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(
        key='refreshtoken',
        value=refresh_token,
        httponly=True,
        secure=False
    )
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response
