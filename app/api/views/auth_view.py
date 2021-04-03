from django.contrib import auth
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from knox.models import AuthToken

from ..models import PushToken
from ..serializers.auth_serializer import LoginSerializer
from ..serializers.user_serializer import UserRetrieveSerializer

class SignInAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        auth_token = AuthToken.objects.create(user)

        push_token = user.push_token
        if push_token:
            existing_token = PushToken.objects.filter(key=push_token).first()
            if existing_token:
                existing_token.delete()

            token = PushToken(auth_token=auth_token[0], key=push_token)
            token.save()

        return Response({
            "user": UserRetrieveSerializer(user, context=self.get_serializer_context()).data,
            "token": auth_token[1]
        })
