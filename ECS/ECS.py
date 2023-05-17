from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkecs.v2 import *
from VPC.VPC import VPC

from error import error

class ECS:
    def __init__(self, ak: str, sk: str, project_id: str):
        self._endpoint = "https://ecs.ru-moscow-1.hc.sbercloud.ru"
        self._ak = ak
        self._sk = sk
        self._project_id = project_id

        self._config = None
        self._credentials = None
        self._client = None

        self._set_configs()
        self._set_client()

        self._json_of_ecs = self.get_json_of_ecs()

    def _set_configs(self):
        self._config = HttpConfig.get_default_config()
        self._config.ignore_ssl_verification = True
        self._credentials = BasicCredentials(self._ak, self._sk, self._project_id)

    def _set_client(self):
        self._client = EcsClient.new_builder() \
            .with_http_config(self._config) \
            .with_credentials(self._credentials) \
            .with_endpoint(self._endpoint) \
            .build()

    def change_name_of_ecs(self, ecs_name_old: str, ecs_name_new: str):
        try:
            if not self.check_ecs_name(ecs_name_new):
                option = UpdateServerOption(name=ecs_name_new)
                update_body = UpdateServerRequestBody(option)
                request = UpdateServerRequest(self._get_ecs_id_by_name(ecs_name_old), update_body)
                response = self._client.update_server(request)
                self._json_of_ecs = self.get_json_of_ecs()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0

    def get_json_of_ecs(self):
        try:
            request = ListServersDetailsRequest()
            response = self._client.list_servers_details(request)
            return response.servers
        except exceptions.ClientRequestException as e:
            error(e)

    def get_json_of_flavors(self):
        try:
            request = ListFlavorsRequest()
            response = self._client.list_flavors(request)
            return response.flavors
        except exceptions.ClientRequestException as e:
            error(e)

    def check_ecs_name(self, ecs_name: str):
        for ecs in self._json_of_ecs:
            if ecs.name == ecs_name:
                return True
        return False

    def _get_ecs_id_by_name(self, ecs_name: str):
        for i in range(len(self._json_of_ecs)):
            if ecs_name == self._json_of_ecs[i].name:
                return self._json_of_ecs[i].id

    def delete_ecs_by_name(self, ecs_name: str):
        try:
            ecs_id = [self._get_ecs_id_by_name(ecs_name), ]
            body = DeleteServersRequestBody(True, True, ecs_id)
            request = DeleteServersRequest(body)
            response = self._client.delete_servers(request)
            self._json_of_ecs = self.get_json_of_ecs()
            return True
        except exceptions.ClientRequestException as e:
            error(e)
            return False

    def create_new_ecs(self, ecs_name: str,
                       flavor_ref: str,
                       image_ref: str,
                       vpc_name: str, subnet_name: str,
                       volume_type: str, volume_size: int):
        try:
            if not self.check_ecs_name(ecs_name):
                vpc = VPC(self._ak, self._sk, self._project_id)
                subnet_id = vpc.get_subnet_id_by_name(subnet_name)
                vpc_id = vpc.get_vpc_id_by_name(vpc_name)
                nics = [PostPaidServerNic(subnet_id), ]
                root_volume = PostPaidServerRootVolume(volume_type, volume_size)
                server = PostPaidServer(name=ecs_name,
                                        flavor_ref=flavor_ref, image_ref=image_ref,
                                        vpcid=vpc_id, nics=nics,
                                        root_volume=root_volume)
                server_body = CreatePostPaidServersRequestBody(server=server)
                request = CreatePostPaidServersRequest(body=server_body)
                response = self._client.create_post_paid_servers(request)
                self._json_of_ecs = self.get_json_of_ecs()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0