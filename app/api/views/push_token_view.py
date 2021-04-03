from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .base_view import BaseViewSet
from ..serializers import *
from ..models import PushToken
from knox.models import AuthToken
from firebase_admin import messaging

from ..utils.push_notification_util import PushNotificationUtil


class PushTokenViewSetPermission(BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        if request.method in ['POST']:
            return type(request.auth) is AuthToken
        return True


class PushTokenViewSet(BaseViewSet):
    serializer_class = PushTokenPostSerializer
    model_class = PushToken

    http_method_names = ['post', 'delete', 'get']

    def get_additional_permission_classes(self):
        return super(PushTokenViewSet, self).get_additional_permission_classes() + (PushTokenViewSetPermission,)

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return PushTokenRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return PushTokenPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return PushTokenListSerializer

    def get_queryset(self):
        return PushToken.objects.filter(auth_token__user=self.request.user)

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        serializer.save(auth_token=self.request.auth)

    @action(detail=False, methods=['get'], url_path='test')
    def test(self, request, *args, **kwargs):
        tokens = self.request.user.send_push_notification(
            notification=messaging.Notification(
                title=self.request.GET.get('title', "test"),
                body=self.request.GET.get('body', "body")
            ),
            data={
                "attachment": "https://via.placeholder.com/350x150/ff0000/eeeeff?text=AK+News",
                "link": "intern://test"
            }
        )

        return Response({"send": True})
