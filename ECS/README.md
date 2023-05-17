# Краткая документация по работе с ECS

Импортуем SDK по Huawei Cloud для работы c ECS

```py
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkecs.v2 import *
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

Поменять имя ECS:
```py
change_name_of_ecs(<старое_имя>, <новое_имя>)
```

Получить json строку всех ECS:
```py
get_json_of_ecs()
```

Получить json строку всех доступных серверов для ECS:
```py
get_json_of_flavors()
```

Получить есть ли такое название ECS:
```py
check_ecs_name(<имя_ecs>)
```


Получить id ECS по имени:
```py
_get_ecs_id_by_name(<имя_ecs>)
```

Удалить ECS по имени:
```py
delete_ecs_by_name(<имя_ecs>)
```

Создать ECS:
```py
create_new_ecs(<имя_ecs>, 
               <адрес_flavor>(flavor_ref),
               <id_образа>,  
               <имя_vpc>, <имя_subnet>,
               <тип_диска>, <размерность_диска>)
```