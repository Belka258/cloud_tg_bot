from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkims.v2 import *

from error import error

class IMS:
    def __init__(self, ak: str, sk: str, project_id: str):
        self._endpoint = "https://ims.ru-moscow-1.hc.sbercloud.ru"
        self._ak = ak
        self._sk = sk
        self._project_id = project_id

        self._config = None
        self._credentials = None
        self._client = None

        self._set_configs()
        self._set_client()

        self._json_of_ims = self.get_json_of_ims()

    def _set_configs(self):
        self._config = HttpConfig.get_default_config()
        self._config.ignore_ssl_verification = True
        self._credentials = BasicCredentials(self._ak, self._sk, self._project_id)

    def _set_client(self):
        self._client = ImsClient.new_builder() \
            .with_http_config(self._config) \
            .with_credentials(self._credentials) \
            .with_endpoint(self._endpoint) \
            .build()

    def get_json_of_ims(self):
        try:
            request = ListImagesRequest()
            response = self._client.list_images(request)
            return response.images
        except exceptions.ClientRequestException as e:
            error(e)
