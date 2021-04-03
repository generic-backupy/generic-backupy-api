from django.utils import timezone
from ..utils.push_notification_util import *
#from django.contrib.auth import get_user_model
#User = get_user_model()
from ..models.user import *
from firebase_admin import messaging


def push_each_minute():
    """
    Send a push notification each  minute
    """
    one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
    user = User.objects.filter(username="mrader").first()
    PushNotificationUtil \
        .sendToUser(user,
                    notification=messaging.Notification(
                        title="each minute bro",
                        body="minute: " + str(timezone.now().minute)
                    ),
                    data={
                        "attachment": "https://via.placeholder.com/350x150/ff0000/eeeeff?text=TEST",
                        "link": "intern://test"
                    }
                    )
