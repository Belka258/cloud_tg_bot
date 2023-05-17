from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkrds.v3 import *
from VPC.VPC import VPC

from error import error


class RDS:
    def __init__(self, ak: str, sk: str, project_id: str):
        self._endpoint = "https://rds.ru-moscow-1.hc.sbercloud.ru"
        self._ak = ak
        self._sk = sk
        self._project_id = project_id

        self._config = None
        self._credentials = None
        self._client = None

        self._set_configs()
        self._set_client()

        self._json_of_rds = self.get_json_of_rds()

    def _set_configs(self):
        self._config = HttpConfig.get_default_config()
        self._config.ignore_ssl_verification = True
        self._credentials = BasicCredentials(self._ak, self._sk, self._project_id)

    def _set_client(self):
        self._client = RdsClient.new_builder() \
            .with_http_config(self._config) \
            .with_credentials(self._credentials) \
            .with_endpoint(self._endpoint) \
            .build()

    def _get_instance_id_by_name(self, rds_name: str):
        for i in range(len(self._json_of_rds)):
            if rds_name == self._json_of_rds[i].name:
                return self._json_of_rds[i].id

    def check_rds_name(self, rds_name: str):
        for rds in self._json_of_rds:
            if rds.name == rds_name:
                return True
        return False

    def get_json_of_rds(self):
        try:
            request = ListInstancesRequest()
            response = self._client.list_instances(request)
            return response.instances
        except exceptions.ClientRequestException as e:
            error(e)

    def delete_rds_by_name(self, rds_name: str):
        try:
            request = DeleteInstanceRequest(instance_id=self._get_instance_id_by_name(rds_name))
            response = self._client.delete_instance(request)
            self._json_of_rds = self.get_json_of_rds()
            return True
        except exceptions.ClientRequestException as e:
            error(e)
            return False

    def get_json_flavors_of_rds(self, database_name: str):
        try:
            request = ListFlavorsRequest(database_name=database_name)
            response = self._client.list_flavors(request)
            return response.flavors
        except exceptions.ClientRequestException as e:
            error(e)
    
    def change_name_of_rds(self, rds_name_old: str, rds_name_new: str):
        try:
            if not self.check_rds_name(rds_name_new):
                update_body = ModifiyInstanceNameRequest(rds_name_new)
                request = UpdateInstanceNameRequest(instance_id=self._get_instance_id_by_name(rds_name_old),
                                                    body=update_body)
                response = self._client.update_instance_name(request)
                self._json_of_rds = self.get_json_of_rds()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0
    
    def get_vpc_subnet_security_group_id(self, vpc_name: str, subnet_name: str, security_group_name: str):
        vpc = VPC(self._ak, self._sk, self._project_id)
        vpc_id = vpc.get_vpc_id_by_name(vpc_name)
        subnet_id = vpc.get_subnet_id_by_name(subnet_name)
        security_group_id = vpc.get_security_group_id_by_name(security_group_name)
        return vpc_id, subnet_id, security_group_id

    # doesn't work with HA parameter (single/standby)
    def create_new_rds(self, rds_name: str,
                       type_db: str = None, version_db: str = None,
                       flavor_ref: str = None,
                       volume_type: str = None, volume_size: int = None,
                       region: str = 'ru-moscow-1', availability_zone: str = None,
                       vpc_name: str = None, subnet_name: str = None,
                       security_group_name: str = None, password: str = None
                       ):
        try:
            if not self.check_rds_name(rds_name):
                datastore = Datastore(type_db, version_db)
                volume = Volume(volume_type, volume_size)
                vpc_id, subnet_id, security_group_id = self.get_vpc_subnet_security_group_id(vpc_name,
                                                                                             subnet_name,
                                                                                             security_group_name)

                body = InstanceRequest(name=rds_name,
                                       volume=volume,
                                       datastore=datastore,
                                       flavor_ref=flavor_ref,
                                       region=region, availability_zone=availability_zone,
                                       vpc_id=vpc_id, subnet_id=subnet_id,
                                       security_group_id=security_group_id,
                                       password=password)

                request = CreateInstanceRequest(body=body)
                respone = self._client.create_instance(request)
                self._json_of_rds = self.get_json_of_rds()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0
