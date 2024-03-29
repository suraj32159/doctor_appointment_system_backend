import codecs
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, List, Union, ByteString

import environ

from mailer.mailerCom.ms_graph import Auth2MailerMixin

env = environ.Env()
environ.Env.read_env()

logger = logging.getLogger(__name__)


class BaseMessage(Auth2MailerMixin, ABC):
    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def get_message(self, *args, **kwargs):
        pass

    def get_body(self, content):
        return {"contentType": "html", "content": content}


class SimpleMessage(BaseMessage):
    def __init__(self, subject: str, body: Any = None, recipients: List = None):
        self._subject = subject
        self._content = body
        self._recipients = recipients
        self._message = None
        self._body = None

    def get_message(self, subject, body, recipients):
        return json.dumps(
            {
                "message": {
                    "subject": subject,
                    "body": body,
                    "toRecipients": [
                        {"emailAddress": {"address": f"{recipient}"}}
                        for recipient in recipients
                    ],
                }
            }
        )

    def send(self):
        try:
            body = self.get_body(self._content)
            message = self.get_message(self._subject, body, self._recipients)
            response = self.sendMailAsApplication(message=message)
            return response.text
        except Exception as error:
            logger.exception(error)
            return {}


class AttachmentMessage(BaseMessage):
    def __init__(
        self,
        subject: str,
        content_type: str = "text/plain",
        body: Any = None,
        recipients: List = None,
        attachment_name: str = "attachment",
        attachments: Union[ByteString, str] = None,
    ):
        self._subject = subject
        self._content_type = content_type
        self._content = body
        self._recipients = recipients
        self._message = None
        self._body = None
        self._attachment_name = attachment_name
        self._attachment = attachments

    def get_message(self, subject, body, recipients, attachment):
        message = json.dumps(
            {
                "message": {
                    "subject": subject,
                    "body": body,
                    "toRecipients": [
                        {"emailAddress": {"address": f"{recipient}"}}
                        for recipient in recipients
                    ],
                    "attachments": [
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": self._attachment_name,
                            "contentType": self._content_type,
                            "contentBytes": codecs.encode(attachment, "base64").decode(
                                "utf-8"
                            ),
                        }
                    ],
                }
            }
        )
        return message

    def send(self):
        try:
            body = self.get_body(self._content)
            message = self.get_message(
                self._subject, body, self._recipients, self._attachment
            )
            response = self.sendMailAsApplication(message=message)
            return response.text
        except Exception as error:
            logger.exception(error)
            return {}
