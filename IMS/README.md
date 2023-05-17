# Краткая документация по работе с IMS

Импортуем SDK по Huawei Cloud для работы c IMS

```py
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkims.v2 import *
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

Получить json строку всех IMS:
```py
get_json_of_ims()
```