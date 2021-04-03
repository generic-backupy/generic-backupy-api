from django.template.loader import render_to_string

from ..exceptions import AppErrorException
from ..models.user import *
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class EmailUtil:

    @staticmethod
    def send_to_user(subject: str, msg: str, user: User, from_email=getattr(settings, 'EMAIL_DEFAULT_SENDER', ''), fail_silently=False, html_message=None):
        send_mail(
            subject,
            msg,
            from_email,
            [user.email],
            fail_silently=fail_silently,
            html_message=html_message
        )

    @staticmethod
    def send_to_verified_user(subject: str, msg: str, user: User, from_email=getattr(settings, 'EMAIL_DEFAULT_SENDER', ''), fail_silently=False, html_message=None):
        if user.email_verified:
            EmailUtil.send_to_user(subject, msg, user, from_email, fail_silently, html_message)
            return True
        else:
            return False

    @staticmethod
    def send_verification_code(user: User):
        if user.email_verified:
            return None

        code = None

        if user.email_verification_code_last_request and (datetime.now(timezone.utc) - user.email_verification_code_last_request).seconds < 1*60:
            raise AppErrorException(_("too_many_requests"), _("email.verification.too_many_requests"), status_code=429)

        if user.email_verification_code_created_at:
            # use the existing code, if the verification created date is valid
            if (datetime.now(timezone.utc) - user.email_verification_code_created_at).days < 1:
                code = user.email_verification_code

        # else create a new one
        if not code:
            code, time = user.create_email_verification_code(save=False)

        user.email_verification_code_last_request = datetime.now(timezone.utc)
        user.save()
        css_part = render_to_string("email/styles.html")
        html_template = render_to_string("email/verification-code.html", {
            'code': code,
            'verify_url': getattr(settings, 'VERIFY_EMAIL_URL', ''),
            'css_part': css_part
        })
        EmailUtil.send_to_user("Verify your Account", "B", user,
                               html_message=html_template)
        return code
