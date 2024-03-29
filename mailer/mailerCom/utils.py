import logging
import mimetypes
from abc import ABC

import requests
from constance import config

logger = logging.getLogger(__name__)


class MailerUtils(ABC):
    def get_info_bip_url(self, url):
        headers = {
            "Content-Type": "application/json",
            "Authorization": config.COMPANY_INFOBIP_AUTH_TOKEN,
        }
        try:
            response = requests.get(url, headers=headers)
            content_type = response.headers["content-type"]
            extension = mimetypes.guess_extension(content_type)
            return {
                "content_type": content_type,
                "response_content": response.content,
                "extension": extension,
                "response": response,
            }
        except Exception as error:
            logger.exception(error)
            return None
