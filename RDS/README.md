# Краткая документация по работе с RDS

Импортуем SDK по Huawei Cloud для работы c RDS

```py
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkrds.v3 import *
```

Импортируем VPC и error для работы внутри класса

```py
from VPC.VPC import VPC

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

Получить id RDS по имени:
```py
_get_instance_id_by_name(<имя_rds>)
```

Получить есть ли такое название RDS:
```py
check_rds_name(<имя_rds>)
```

Получить json строку всех RDS:
```py
get_json_of_rds()
```

Удалить RDS по имени:
```py
delete_rds_by_name(<имя_rds>)
```

Получить json строку всех доступных серверов для RDS:
```py
get_json_flavors_of_rds(<название_движка_базы_данных>)
```

Поменять имя RDS:
```py
change_name_of_rds(<старое_имя>, <новое_имя>)
```

Получить id VPC, Subnet, Security Group по их именам:
```py
get_vpc_subnet_security_group_id(<имя_vpc>, <имя_subnet>, <имя_security_group>)
```

Создать RDS:
```py
create_new_rds(<имя_rds>, <тип_базы_данных>,
               <версия_базы_данных>, <адрес_flavor>(flavor_ref), 
               <тип_диска>, <размер_диска>,
               <регион>, <зона_доступности>,
               <имя_vpc>, <имя_subnet>,
               <имя_security_group>, <пароль_для_rds>)
```