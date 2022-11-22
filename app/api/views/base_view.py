from django.conf import settings

from ..exceptions import MessageStatusCodeException
from ..rms_base import *
from django.utils.translation import gettext_lazy as _


class UserCurrentConditionsPermission(BasePermission):
    def has_permission(self, request, view):
        return True # disable this later, if we want to use privacy and conditions
        user = request.user
        if user:
            path = request.path.split("/")
            if len(path) > 0 and path[3] not in ["users", "auth"]:
                privacy_version = settings.PRIVACY_VERSION
                conditions_version = settings.CONDITIONS_VERSION

                if user.privacy_version != privacy_version:
                    resp = {}
                    AppInfo(title=_("new-privacy.header"),
                            text=_("new-privacy.body"),
                            icon="document-outline",
                            info_link="https://generic-backupy.at/privacy",
                            needed_check_box_text=_("new-privacy.accept-checkbox"),
                            info_link_text=_("new-privacy.show"),
                            api_link_on_success_button="https://api.generic-backupy.at/api/v1/users/accept-privacy").append_to(resp)
                    raise MessageStatusCodeException(resp, 439)
                if user.conditions_version != conditions_version:
                    resp = {}
                    AppInfo(title=_("new-conditions.header"),
                            text=_("new-conditions.body"),
                            info_link="https://generic-backupy.at/terms-and-conditions",
                            icon="document-outline",
                            needed_check_box_text=_("new-conditions.accept-checkbox"),
                            info_link_text=_("new-conditions.show"),
                            api_link_on_success_button="https://api.generic-backupy.at/api/v1/users/accept-conditions").append_to(resp)
                    raise MessageStatusCodeException(resp, 439)
        return True


class BaseViewSet(RmsBaseViewSet):

    def get_additional_permission_classes(self):
        return (UserCurrentConditionsPermission,)

    def has_permission_put(self):
        return self.has_permission_update()

    def has_permission_update(self):
        return True

    def has_permission_partial_update(self):
        return self.has_permission_put()

    def has_permission_patch(self):
        return self.has_permission_update()
