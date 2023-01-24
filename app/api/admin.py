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

class BackupJobStorageModuleSecretInline(admin.TabularInline):
    model = BackupJobStorageModuleSecret
    extra = 1

class BackupJobStorageModuleParameterInline(admin.TabularInline):
    model = BackupJobStorageModuleParameter
    extra = 1

class BackupJobStorageModuleInline(admin.TabularInline):
    model = BackupJobStorageModule
    extra = 1
    inlines = (BackupJobStorageModuleSecretInline,)

class BackupJobSecretInline(admin.TabularInline):
    model = BackupJobSecret
    extra = 1

class BackupJobParameterInline(admin.TabularInline):
    model = BackupJobParameter
    extra = 1

class BackupJobAdmin(admin.ModelAdmin):
    inlines = (BackupJobSecretInline, BackupJobParameterInline, BackupJobStorageModuleInline)


class BackupJobStorageModuleAdmin(admin.ModelAdmin):
    inlines = (BackupJobStorageModuleSecretInline, BackupJobStorageModuleParameterInline)

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(PasswordResetToken)
admin.site.register(PushToken)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(System)
admin.site.register(BackupJob, BackupJobAdmin)
admin.site.register(Backup)
admin.site.register(BackupModule)
admin.site.register(StorageModule)
admin.site.register(BackupJobStorageModule, BackupJobStorageModuleAdmin)
admin.site.register(Secret)
admin.site.register(BackupExecution)
admin.site.register(StorageExecution)
admin.site.register(Parameter)
admin.site.register(RestoreExecution)
admin.site.register(ModuleInstallationExecution)
