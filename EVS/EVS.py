from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkevs.v2 import *

from error import error


class EVS:
    def __init__(self, ak: str, sk: str, project_id: str):
        self._endpoint = "https://evs.ru-moscow-1.hc.sbercloud.ru"
        self._ak = ak
        self._sk = sk
        self._project_id = project_id

        self._config = None
        self._credentials = None
        self._client = None

        self._set_configs()
        self._set_client()

        self._json_of_evs = self.get_json_of_evs()

    def _set_configs(self):
        self._config = HttpConfig.get_default_config()
        self._config.ignore_ssl_verification = True
        self._credentials = BasicCredentials(self._ak, self._sk, self._project_id)

    def _set_client(self):
        self._client = EvsClient.new_builder() \
            .with_http_config(self._config) \
            .with_credentials(self._credentials) \
            .with_endpoint(self._endpoint) \
            .build()

    def get_json_of_evs(self):
        try:
            CinderListAvailabilityZonesRequest()
            request = ListVolumesRequest()
            response = self._client.list_volumes(request)
            return response.volumes
        except exceptions.ClientRequestException as e:
            error(e)

    def check_evs_name(self, name: str, az: str = None):
        if az is None:
            for evs in self._json_of_evs:
                if evs.name == name:
                    return True
            return False
        else:
            for evs in self._json_of_evs:
                if evs.name == name\
                        and evs.availability_zone == az:
                    return True
            return False

    def create_new_evs(self, evs_name: str, disk_type: str, size: int, count: int, az: str):
        try:
            if not self.check_evs_name(evs_name, az):
                volume = CreateVolumeOption(name=evs_name,
                                            volume_type=disk_type,
                                            size=size,
                                            availability_zone=az,
                                            count=count)
                body = CreateVolumeRequestBody(volume=volume)
                request = CreateVolumeRequest(body)
                response = self._client.create_volume(request)
                self._json_of_evs = self.get_json_of_evs()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0

    def _get_volume_id_by_name(self, volume_name: str):
        for i in range(len(self._json_of_evs)):
            if volume_name == self._json_of_evs[i].name:
                return self._json_of_evs[i].id

    def _get_volume_id_by_name_and_az(self, volume_name: str, az: str):
        for i in range(len(self._json_of_evs)):
            if volume_name == self._json_of_evs[i].name \
                    and az == self._json_of_evs[i].availability_zone:
                return self._json_of_evs[i].id

    def delete_evs_by_name(self, evs_name, az: str = None):
        try:
            if az is None:
                request = DeleteVolumeRequest(self._get_volume_id_by_name(evs_name))
            else:
                request = DeleteVolumeRequest(self._get_volume_id_by_name_and_az(evs_name, az))
            response = self._client.delete_volume(request)
            self._json_of_evs = self.get_json_of_evs()
            return True
        except exceptions.ClientRequestException as e:
            error(e)
            return False

    def change_name_of_evs(self, evs_name_old: str, evs_name_new: str):
        try:
            if not self.check_evs_name(evs_name_new):
                option = UpdateVolumeOption(name=evs_name_new)
                update_body = UpdateVolumeRequestBody(option)
                request = UpdateVolumeRequest(self._get_volume_id_by_name(evs_name_old), update_body)
                response = self._client.update_volume(request)
                self._json_of_evs = self.get_json_of_evs()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0

    def _get_volume_index_by_name(self, volume_name: str):
        for i in range(len(self._json_of_evs)):
            if volume_name == self._json_of_evs[i].name:
                return i


    def expand_disk_by_name(self, evs_name: str, new_size: int):
        try:
            if new_size > self._json_of_evs[self._get_volume_index_by_name(evs_name)].new_size:
                os_extend = OsExtend(new_size)
                bss_param = BssParamForResizeVolume()
                body = ResizeVolumeRequestBody(bss_param, os_extend)
                request = ResizeVolumeRequest(self._get_volume_id_by_name(evs_name), body)
                response = self._client.resize_volume(request)
                self._json_of_evs = self.get_json_of_evs()
                return 1
            else:
                return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0