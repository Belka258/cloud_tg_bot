# Краткая документация по работе с EVS

Импортуем SDK по Huawei Cloud для работы c EVS

```py
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkevs.v2 import *
```

Импортируем error для работы внутри класса

```py
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

Получить json строку всех EVS:
```py
get_json_of_ecs()
```

Получить есть ли такое название EVS:
```py
check_evs_name(<имя_evs>)
```

Создать EVS:
```py
create_new_evs(<имя_evs>, <тип_диска>, <размер_диска>, <зона доступности>)
```

Получить id EVS по имени:
```py
_get_volume_id_by_name(<имя_evs>)
```

Получить id EVS по имени и зоне доступности:
```py
_get_volume_id_by_name_and_az(<имя_evs>, <зона_доступности>)
```

Удалить EVS по имени:
```py
delete_evs_by_name(<имя_evs>)
```

Поменять имя EVS:
```py
change_name_of_evs(<старое_имя>, <новое_имя>)
```

Получить json строку всех ECS:
```py
get_json_of_ecs()
```

Получить index EVS по имени:
```py
_get_volume_index_by_name(<имя_evs>)
```

Расширить диск по имени EVS:
```py
expand_disk_by_name(<имя_evs>, <новый размер>)
```


