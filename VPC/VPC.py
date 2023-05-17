from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkvpc.v2 import *
import time

from error import error

class VPC:
    def __init__(self, ak: str, sk: str, project_id: str):
        self._endpoint = "https://vpc.ru-moscow-1.hc.sbercloud.ru"
        self._ak = ak
        self._sk = sk
        self._project_id = project_id

        self._config = None
        self._credentials = None
        self._client = None

        self._set_configs()
        self._set_client()

        self._json_of_vpc = self.get_json_of_vpc()
        self._json_of_subnets = self.get_json_of_subnets()
        self._json_of_security_groups = self.get_json_of_security_groups()

    def _set_configs(self):
        self._config = HttpConfig.get_default_config()
        self._config.ignore_ssl_verification = True
        self._credentials = BasicCredentials(self._ak, self._sk, self._project_id)

    def _set_client(self):
        self._client = VpcClient.new_builder() \
            .with_http_config(self._config) \
            .with_credentials(self._credentials) \
            .with_endpoint(self._endpoint) \
            .build()

    def get_json_of_vpc(self):
        try:
            request = ListVpcsRequest()
            response = self._client.list_vpcs(request)
            return response.vpcs
        except exceptions.ClientRequestException as e:
            error(e)

    def get_json_of_subnets(self):
        try:
            request = ListSubnetsRequest()
            response = self._client.list_subnets(request)
            return response.subnets
        except exceptions.ClientRequestException as e:
            error(e)

    def check_vpc_name(self, vpc_name: str):
        for vpc in self._json_of_vpc:
            if vpc.name == vpc_name:
                return True
        return False

    def check_subnet_name(self, subnet_name: str):
        for subnet in self._json_of_subnets:
            if subnet.name == subnet_name:
                return True
        return False

    def create_new_vpc(self, cidr: str, vpc_name: str, description: str = None):
        try:
            if not self.check_vpc_name(vpc_name):
                vpc_option = CreateVpcOption(cidr,
                                             vpc_name,
                                             description)
                vpc_body = CreateVpcRequestBody(vpc_option)
                request = CreateVpcRequest(vpc_body)
                response = self._client.create_vpc(request)
                self._json_of_vpc = self.get_json_of_vpc()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0

    def get_vpc_id_by_name(self, vpc_name: str):
        for i in range(len(self._json_of_vpc)):
            if vpc_name == self._json_of_vpc[i].name:
                return self._json_of_vpc[i].id

    def get_subnet_id_by_name(self, subnet_name: str):
        for i in range(len(self._json_of_subnets)):
            if subnet_name == self._json_of_subnets[i].name:
                return self._json_of_subnets[i].id

    def get_security_group_id_by_name(self, security_group_name: str):
        for i in range(len(self._json_of_security_groups)):
            if security_group_name == self._json_of_security_groups[i].name:
                return self._json_of_security_groups[i].id

    def _get_list_subnets_id_by_vpc_name(self, vpc_name: str):
        vpc_id = self.get_vpc_id_by_name(vpc_name)
        subnets_id = list()
        for i in range(len(self._json_of_subnets)):
            if vpc_id == self._json_of_subnets[i].vpc_id:
                subnets_id.append((vpc_id, self._json_of_subnets[i].id))
        return subnets_id
    
    def change_name_of_vpc(self, vpc_name_old: str, vpc_name_new: str):
        try:
            if not self.check_vpc_name(vpc_name_new):
                option = UpdateVpcOption(vpc_name_new)
                updated_body = UpdateVpcRequestBody(option)
                request = UpdateVpcRequest(vpc_id=self.get_vpc_id_by_name(vpc_name_old), 
                                           body=updated_body)
                self._json_of_vpc = self.get_json_of_vpc()
                response = self._client.update_vpc(request)
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0
        
    def change_name_of_subnet(self, subnet_name_old: str, subnet_name_new: str):
        try:
            if not self.check_subnet_name(subnet_name_new):
                option = UpdateSubnetOption(subnet_name_new)
                updated_body = UpdateSubnetRequestBody(option)
                request = UpdateSubnetRequest(vpc_id=self._get_vpc_id_by_subnet_name(subnet_name_old),
                                              subnet_id=self.get_subnet_id_by_name(subnet_name_old),
                                              body=updated_body)
                response = self._client.update_subnet(request)
                self._json_of_vpc = self.get_json_of_vpc()
                self._json_of_subnets = self.get_json_of_subnets()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0
    
    def create_new_subnet(self, subnet_name: str, cidr: str, vpc_name: str, gateway_ip: str, ipv6: bool = False, dhcp: bool = True,
                          description: str = None, primary_dns: str = '100.125.13.59',
                          secondary_dns: str = '100.125.65.14'):
        try:
            if self.check_vpc_name(vpc_name) and not self.check_subnet_name(subnet_name):
                vpc_id = self.get_vpc_id_by_name(vpc_name)
                subnet_option = CreateSubnetOption(subnet_name,
                                                   description,
                                                   cidr,
                                                   vpc_id,
                                                   gateway_ip,
                                                   ipv6,
                                                   dhcp,
                                                   primary_dns,
                                                   secondary_dns)
                subnet_body = CreateSubnetRequestBody(subnet_option)
                request = CreateSubnetRequest(subnet_body)
                response = self._client.create_subnet(request)
                self._json_of_subnets = self.get_json_of_subnets()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0

    def delete_subnets_from_vpc(self, vpc_name: str):
        try:
            subnets_id = self._get_list_subnets_id_by_vpc_name(vpc_name)
            for i in range(len(subnets_id)):
                request = DeleteSubnetRequest(subnets_id[i][0], subnets_id[i][1])
                response = self._client.delete_subnet(request)
            self._json_of_subnets = self.get_json_of_subnets()
            return True
        except exceptions.ClientRequestException as e:
            error(e)
            return False

    def delete_vpc_by_name(self, vpc_name: str):
        try:
            if self.delete_subnets_from_vpc(vpc_name):
                time.sleep(2)
                request = DeleteVpcRequest(self.get_vpc_id_by_name(vpc_name))
                response = self._client.delete_vpc(request)
                self._json_of_vpc = self.get_json_of_vpc()
                return 1
            return 2
        except exceptions.ClientRequestException as e:
            error(e)
            return 0

    def delete_subnet_from_vpc(self, subnet_name: str):
        try:
            request = DeleteSubnetRequest(self._get_vpc_id_by_subnet_name(subnet_name),
                                          self.get_subnet_id_by_name(subnet_name))
            response = self._client.delete_subnet(request)
            self._json_of_subnets = self.get_json_of_subnets()
            return True

        except exceptions.ClientRequestException as e:
            error(e)
            return False

    def _get_vpc_id_by_subnet_name(self, subnet_name: str):
        for i in range(len(self._json_of_subnets)):
            if subnet_name == self._json_of_subnets[i].name:
                return self._json_of_subnets[i].vpc_id

    def get_json_of_security_groups(self):
        try:
            request = ListSecurityGroupsRequest()
            response = self._client.list_security_groups(request)
            return response.security_groups
        except exceptions.ClientRequestException as e:
            error(e)