from firebase_admin import messaging

from ..models.push_token import PushToken


class PushNotificationUtil:

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
