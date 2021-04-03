from firebase_admin import messaging

from ..models.push_token import PushToken


class PushNotificationUtil:

    #"ewI8Fweudkj6pPIh0Tz__a:APA91bFMOpqwZMBmNB6s3g30H3nJ2uzpSJf2uE2sLvU5VZabQEy3tItB6yrumQ5fInTYowv3MXJneFD_gbjXra9lhBDJ9_sqLgLfIcw0OmAZbyuXfP7wA8cN1BJkQKVfBXbyYitinofA"
    @staticmethod
    def sendSingleNotification(token):
        message = messaging.Message(notification=messaging.Notification(title="test", body="here"),
                                    token=token)
        return messaging.send(message)

    @staticmethod
    def sendToUser(user, **kwargs):
        tokens = user.get_push_tokens()
        message = messaging.MulticastMessage(tokens=list(tokens), **kwargs)
        response = messaging.send_multicast(message)
        return response
