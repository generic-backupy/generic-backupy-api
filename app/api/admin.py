from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email_verified',
                           'email_verification_code',
                           'email_verification_code_created_at',
                           'email_verification_code_accepted_at',
                           'email_verification_code_last_request',
                           'reset_password_code_last_request',
                           'privacy_version',
                           'last_privacy_check',
                           'conditions_version',
                           'last_conditions_check',
                           'created_with_user_agent',
                           'created_language')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email_verified',
                           'email_verification_code',
                           'email_verification_code_created_at',
                           'email_verification_code_accepted_at',
                           'email_verification_code_last_request',
                           'reset_password_code_last_request',
                           'privacy_version',
                           'last_privacy_check',
                           'conditions_version',
                           'last_conditions_check',
                           'created_with_user_agent',
                           'created_language')}),
    )
    list_display = UserAdmin.list_display + ('created_at', )
    ordering = ('-created_at', 'username')


# Register your models here.
admin.site.register(User, CustomUserAdmin)
#admin.site.register(PasswordResetToken)
#admin.site.register(PushToken)
#admin.site.register(Tag)
