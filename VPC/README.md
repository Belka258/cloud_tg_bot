# Краткая документация по работе с VPC

Импортуем SDK по Huawei Cloud для работы c VPC

```py
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkvpc.v2 import *
```

Импортируем time и error для работы внутри класса

```py
import time

from error import error
```

Конструктор принимает AccessKey, SecretKey, ProjectID.

```py
__init__(ak, sk, project_id)
```

Настройка конфигов, реквизитов и клиента:
```py
_set_configs()

_set_client()
```

Получить json строку всех VPC:
```py
get_json_of_vpc()
```

Получить json строку всех VPC Subnets:
```py
get_json_of_subnets()
```

Получить есть ли такое название VPC:
```py
check_vpc_name(<имя_vpc>)
```

Получить есть ли такое название VPC Subnet:
```py
check_subnet_name(<имя_vpc_subnet>)
```

Создать VPC:
```py
create_new_vpc(<cidr>, <имя_vpc>, <описание>(необязательно))
```

Получить id VPC по имени:
```py
get_vpc_id_by_name(<имя_vpc>)
```

Получить id VPC Subnet по имени:
```py
get_subnet_id_by_name(<имя_vpc_subnet>)
```

Получить id VPC Security Group по имени:
```py
get_security_group_id_by_name(<имя_vpc_security group>)
```

Поменять имя VPC:
```py
change_name_of_vpc(<старое_имя_vpc>, <новое_имя_vpc>)
```

Поменять имя VPC Subnet:
```py
change_name_of_subnet(<старое_имя_vpc_subnet>, <новое_имя_vpc_subnet>)
```

Создать VPC Subnet:
```py
create_new_subnet(<имя_vpc_subnet>, <cidr>, <имя_vpc>,
                  <gateway_ip>, <ipv6-bool>, <dhcp-bool>
                  <описание>,
                  <первичный_ip_dns>, <вторичный_ip_dns>)
```

Удалить все VPC Subnets из VPC:
```py
delete_subnets_from_vpc(<имя_vpc>)
```

Удалить VPC по имени:
```py
delete_vpc_by_name(<имя_vpc>)
```

Удалить VPC Subnet по имени:
```py
delete_subnet_from_vpc(<имя_vpc_subnet>)
```

Получить id VPC по имени VPC Subnet:
```py
_get_vpc_id_by_subnet_name(<имя_vpc_subnet>)
```

Получить json строку всех VPC Security Group:
```py
get_json_of_security_groups()
```