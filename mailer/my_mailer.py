import logging
from typing import Any

from django.conf import settings
from django.core import mail
from django.template.loader import get_template

from mailer.mailerCom.messages import SimpleMessage, AttachmentMessage
from mailer.mailerCom.utils import MailerUtils

EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_HOST = settings.EMAIL_HOST

logger = logging.getLogger(__name__)


class Mailer(MailerUtils):
    """
    Send email messages ce_helper class`
    """

    # @shared_task
    def send_messages(self, context, t_name):
        """
        Send mails using html templates
        Input:  email_type = number for required template
                context    = parameters required to render selected template
                to_mails   = list of emails
        Output: Celery Task that mails in the background
        """
        subject = context["subject"]
        messages = self.__generate_messages(
            subject, context, t_name, context["recipients"]
        )
        return messages
        # self.__send_mail(messages)

    def __send_mail(self, message: [SimpleMessage, AttachmentMessage, Any]):
        """
        Send email messages
        :param message:
        :return:
        """
        try:
            connection = mail.get_connection(
                host=EMAIL_HOST,
                port="587",
                username=EMAIL_HOST_USER,
                password=EMAIL_HOST_PASSWORD,
                use_tls=True,
                use_ssl=False,
            )
            connection.open()
            connection.send_messages(message)
            connection.close()
        except Exception as error:
            logger.exception(error)

    def __generate_messages(self, subject, context, template, to_emails):
        """
        Generate email message from Django template
        :param subject: Email message subject
        :param template: Email template
        :param to_emails: to email address[es]
        :return:
        """
        messages = []
        message_template = get_template(template)
        message_content = message_template.render(context)

        message = SimpleMessage(
            subject=subject, body=message_content, recipients=to_emails
        )
        return message
        # else:
        #     for recipient in to_emails:
        #         message = EmailMessage(
        #             subject,
        #             body=message_content,
        #             to=[recipient],
        #             from_email=EMAIL_HOST_USER,
        #         )
        #         message.content_subtype = "html"
        #         messages.append(message)
        #         if attachments:
        #             result = self.get_info_bip_url(attachments)
        #             content_type = result.get("content_type")
        #             response = result.get("response")
        #             file_name = f"tMerchant_file{result.get('extension')}"
        #             message.attach(file_name, response.content, content_type)
        #     return messages