from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.exceptions import APIException


class MessageStatusCodeException(APIException):
    default_detail = 'A server error occurred.'

    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        self.detail = message


class AppErrorException(APIException):
    default_detail = 'A server error occurred.'

    def __init__(self, title=None, text=None, nav_back_at_dismiss=False, icon=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        self.detail = {
            "appError": {
                "title": title,
                "text": text,
                "navBackAtDismiss": nav_back_at_dismiss,
                "icon": icon
            }
        }
