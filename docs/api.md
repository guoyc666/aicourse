---
title: 默认模块
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"
---

# 默认模块

Base URLs:

# Authentication

- oAuth2 authentication.

  - Flow: password

  - Token URL = [/api/auth/login/](/api/auth/login/)

# Default

<a id="opIdroot__get"></a>

## GET Root

GET /

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

<a id="opIdhealth_check_api_health_get"></a>

## GET Health Check

GET /api/health

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

# 认证

<a id="opIdregister_api_auth_register_post"></a>

## POST Register

POST /api/auth/register

用户注册

> Body 请求参数

```json
{
  "username": "string",
  "full_name": "string",
  "password": "string",
  "role": "student"
}
```

### 请求参数

| 名称 | 位置 | 类型                            | 必选 | 中文名     | 说明 |
| ---- | ---- | ------------------------------- | ---- | ---------- | ---- |
| body | body | [UserCreate](#schemausercreate) | 否   | UserCreate | none |

> 返回示例

> 200 Response

```json
{
  "username": "string",
  "full_name": "string",
  "id": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "roles": []
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [UserResponse](#schemauserresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdlogin_api_auth_login_post"></a>

## POST Login

POST /api/auth/login

用户登录

> Body 请求参数

```yaml
grant_type: ""
username: ""
password: ""
scope: ""
client_id: ""
client_secret: ""
```

### 请求参数

| 名称            | 位置 | 类型   | 必选 | 中文名        | 说明 |
| --------------- | ---- | ------ | ---- | ------------- | ---- |
| body            | body | object | 否   |               | none |
| » grant_type    | body | any    | 否   | Grant Type    | none |
| »» _anonymous_  | body | string | 否   |               | none |
| »» _anonymous_  | body | null   | 否   |               | none |
| » username      | body | string | 是   | Username      | none |
| » password      | body | string | 是   | Password      | none |
| » scope         | body | string | 否   | Scope         | none |
| » client_id     | body | any    | 否   | Client Id     | none |
| »» _anonymous_  | body | string | 否   |               | none |
| »» _anonymous_  | body | null   | 否   |               | none |
| » client_secret | body | any    | 否   | Client Secret | none |
| »» _anonymous_  | body | string | 否   |               | none |
| »» _anonymous_  | body | null   | 否   |               | none |

> 返回示例

> 200 Response

```json
{
  "access_token": "string",
  "token_type": "string",
  "user": {
    "username": "string",
    "full_name": "string",
    "id": 0,
    "is_active": true,
    "created_at": "2019-08-24T14:15:22Z",
    "roles": []
  }
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [Token](#schematoken)                             |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdread_users_me_api_auth_me_get"></a>

## GET Read Users Me

GET /api/auth/me

获取当前用户信息

> 返回示例

> 200 Response

```json
{
  "username": "string",
  "full_name": "string",
  "id": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "roles": []
}
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型                            |
| ------ | ------------------------------------------------------- | ------------------- | ----------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | [UserResponse](#schemauserresponse) |

<a id="opIdlogout_api_auth_logout_post"></a>

## POST Logout

POST /api/auth/logout

用户登出

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

# 用户管理

<a id="opIdget_all_students_api_users_students__get"></a>

## GET Get All Students

GET /api/users/students/

获取所有学生列表，返回{id, name}
需要有 user:read 权限

> 返回示例

> 200 Response

```json
[{}]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response Get All Students Api Users Students Get_

| 名称                                             | 类型     | 必选  | 约束 | 中文名                                           | 说明 |
| ------------------------------------------------ | -------- | ----- | ---- | ------------------------------------------------ | ---- |
| Response Get All Students Api Users Students Get | [object] | false | none | Response Get All Students Api Users Students Get | none |

<a id="opIdget_users_api_users__get"></a>

## GET Get Users

GET /api/users/

### 请求参数

| 名称    | 位置  | 类型    | 必选 | 中文名  | 说明 |
| ------- | ----- | ------- | ---- | ------- | ---- |
| skip    | query | integer | 否   | Skip    | none |
| limit   | query | integer | 否   | Limit   | none |
| keyword | query | string  | 否   | Keyword | none |
| role_id | query | integer | 否   | Role Id | none |

> 返回示例

> 200 Response

```json
[
  {
    "username": "string",
    "full_name": "string",
    "id": 0,
    "is_active": true,
    "created_at": "2019-08-24T14:15:22Z",
    "roles": []
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **200**

_Response Get Users Api Users Get_

| 名称                             | 类型                                  | 必选  | 约束 | 中文名                           | 说明 |
| -------------------------------- | ------------------------------------- | ----- | ---- | -------------------------------- | ---- |
| Response Get Users Api Users Get | [[UserResponse](#schemauserresponse)] | false | none | Response Get Users Api Users Get | none |
| » UserResponse                   | [UserResponse](#schemauserresponse)   | false | none | UserResponse                     | none |
| »» username                      | string                                | true  | none | Username                         | none |
| »» full_name                     | any                                   | false | none | Full Name                        | none |

_anyOf_

| 名称            | 类型   | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------ | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称             | 类型                                  | 必选  | 约束 | 中文名       | 说明 |
| ---------------- | ------------------------------------- | ----- | ---- | ------------ | ---- |
| »» id            | integer                               | true  | none | Id           | none |
| »» is_active     | boolean                               | true  | none | Is Active    | none |
| »» created_at    | string(date-time)                     | true  | none | Created At   | none |
| »» roles         | [[RoleResponse](#schemaroleresponse)] | false | none | Roles        | none |
| »»» RoleResponse | [RoleResponse](#schemaroleresponse)   | false | none | RoleResponse | none |
| »»»» id          | integer                               | true  | none | Id           | none |
| »»»» name        | string                                | true  | none | Name         | none |
| »»»» description | any                                   | true  | none | Description  | none |

_anyOf_

| 名称              | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ----------------- | ------ | ----- | ---- | ------ | ---- |
| »»»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称              | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ----------------- | ---- | ----- | ---- | ------ | ---- |
| »»»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称                     | 类型                                              | 必选  | 约束 | 中文名             | 说明 |
| ------------------------ | ------------------------------------------------- | ----- | ---- | ------------------ | ---- |
| »»»» permissions         | [[PermissionResponse](#schemapermissionresponse)] | false | none | Permissions        | none |
| »»»»» PermissionResponse | [PermissionResponse](#schemapermissionresponse)   | false | none | PermissionResponse | none |
| »»»»»» id                | integer                                           | true  | none | Id                 | none |
| »»»»»» name              | string                                            | true  | none | Name               | none |
| »»»»»» description       | any                                               | true  | none | Description        | none |

_anyOf_

| 名称                | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------------- | ------ | ----- | ---- | ------ | ---- |
| »»»»»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称                | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------------- | ---- | ----- | ---- | ------ | ---- |
| »»»»»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称            | 类型 | 必选 | 约束 | 中文名   | 说明 |
| --------------- | ---- | ---- | ---- | -------- | ---- |
| »»»»»» resource | any  | true | none | Resource | none |

_anyOf_

| 名称                | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------------- | ------ | ----- | ---- | ------ | ---- |
| »»»»»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称                | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------------- | ---- | ----- | ---- | ------ | ---- |
| »»»»»»» _anonymous_ | null | false | none |        | none |

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_user_api_users__user_id__get"></a>

## GET Get User

GET /api/users/{user_id}

获取特定用户信息

### 请求参数

| 名称    | 位置 | 类型    | 必选 | 中文名  | 说明 |
| ------- | ---- | ------- | ---- | ------- | ---- |
| user_id | path | integer | 是   | User Id | none |

> 返回示例

> 200 Response

```json
{
  "username": "string",
  "full_name": "string",
  "id": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "roles": []
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [UserResponse](#schemauserresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdupdate_user_api_users__user_id__put"></a>

## PUT Update User

PUT /api/users/{user_id}

更新用户信息

> Body 请求参数

```json
{
  "full_name": "string",
  "password": "string"
}
```

### 请求参数

| 名称    | 位置 | 类型                            | 必选 | 中文名     | 说明 |
| ------- | ---- | ------------------------------- | ---- | ---------- | ---- |
| user_id | path | integer                         | 是   | User Id    | none |
| body    | body | [UserUpdate](#schemauserupdate) | 否   | UserUpdate | none |

> 返回示例

> 200 Response

```json
{
  "username": "string",
  "full_name": "string",
  "id": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "roles": []
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [UserResponse](#schemauserresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIddelete_user_api_users__user_id__delete"></a>

## DELETE Delete User

DELETE /api/users/{user_id}

删除用户（需要管理员权限）

### 请求参数

| 名称    | 位置 | 类型    | 必选 | 中文名  | 说明 |
| ------- | ---- | ------- | ---- | ------- | ---- |
| user_id | path | integer | 是   | User Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_roles_api_users_roles__get"></a>

## GET Get Roles

GET /api/users/roles/

获取角色列表（需要管理员权限）

> 返回示例

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string",
    "description": "string",
    "permissions": []
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response Get Roles Api Users Roles Get_

| 名称                                   | 类型                                  | 必选  | 约束 | 中文名                                 | 说明 |
| -------------------------------------- | ------------------------------------- | ----- | ---- | -------------------------------------- | ---- |
| Response Get Roles Api Users Roles Get | [[RoleResponse](#schemaroleresponse)] | false | none | Response Get Roles Api Users Roles Get | none |
| » RoleResponse                         | [RoleResponse](#schemaroleresponse)   | false | none | RoleResponse                           | none |
| »» id                                  | integer                               | true  | none | Id                                     | none |
| »» name                                | string                                | true  | none | Name                                   | none |
| »» description                         | any                                   | true  | none | Description                            | none |

_anyOf_

| 名称            | 类型   | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------ | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称                   | 类型                                              | 必选  | 约束 | 中文名             | 说明 |
| ---------------------- | ------------------------------------------------- | ----- | ---- | ------------------ | ---- |
| »» permissions         | [[PermissionResponse](#schemapermissionresponse)] | false | none | Permissions        | none |
| »»» PermissionResponse | [PermissionResponse](#schemapermissionresponse)   | false | none | PermissionResponse | none |
| »»»» id                | integer                                           | true  | none | Id                 | none |
| »»»» name              | string                                            | true  | none | Name               | none |
| »»»» description       | any                                               | true  | none | Description        | none |

_anyOf_

| 名称              | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ----------------- | ------ | ----- | ---- | ------ | ---- |
| »»»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称              | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ----------------- | ---- | ----- | ---- | ------ | ---- |
| »»»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称          | 类型 | 必选 | 约束 | 中文名   | 说明 |
| ------------- | ---- | ---- | ---- | -------- | ---- |
| »»»» resource | any  | true | none | Resource | none |

_anyOf_

| 名称              | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ----------------- | ------ | ----- | ---- | ------ | ---- |
| »»»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称              | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ----------------- | ---- | ----- | ---- | ------ | ---- |
| »»»»» _anonymous_ | null | false | none |        | none |

<a id="opIdcreate_role_api_users_roles__post"></a>

## POST Create Role

POST /api/users/roles/

创建角色（需要管理员权限）

> Body 请求参数

```json
{
  "name": "string",
  "description": "string",
  "permission_ids": []
}
```

### 请求参数

| 名称 | 位置 | 类型                            | 必选 | 中文名     | 说明 |
| ---- | ---- | ------------------------------- | ---- | ---------- | ---- |
| body | body | [RoleCreate](#schemarolecreate) | 否   | RoleCreate | none |

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "permissions": []
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [RoleResponse](#schemaroleresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdupdate_role_api_users_roles__role_id__put"></a>

## PUT Update Role

PUT /api/users/roles/{role_id}

更新角色（需要管理员权限）

> Body 请求参数

```json
{
  "name": "string",
  "description": "string",
  "permission_ids": [0]
}
```

### 请求参数

| 名称    | 位置 | 类型                            | 必选 | 中文名     | 说明 |
| ------- | ---- | ------------------------------- | ---- | ---------- | ---- |
| role_id | path | integer                         | 是   | Role Id    | none |
| body    | body | [RoleUpdate](#schemaroleupdate) | 否   | RoleUpdate | none |

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "permissions": []
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [RoleResponse](#schemaroleresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIddelete_role_api_users_roles__role_id__delete"></a>

## DELETE Delete Role

DELETE /api/users/roles/{role_id}

删除角色（需要管理员权限）

### 请求参数

| 名称    | 位置 | 类型    | 必选 | 中文名  | 说明 |
| ------- | ---- | ------- | ---- | ------- | ---- |
| role_id | path | integer | 是   | Role Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_permissions_api_users_permissions__get"></a>

## GET Get Permissions

GET /api/users/permissions/

获取权限列表（需要管理员权限）

> 返回示例

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string",
    "description": "string",
    "resource": "string"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response Get Permissions Api Users Permissions Get_

| 名称                                               | 类型                                              | 必选  | 约束 | 中文名                                             | 说明 |
| -------------------------------------------------- | ------------------------------------------------- | ----- | ---- | -------------------------------------------------- | ---- |
| Response Get Permissions Api Users Permissions Get | [[PermissionResponse](#schemapermissionresponse)] | false | none | Response Get Permissions Api Users Permissions Get | none |
| » PermissionResponse                               | [PermissionResponse](#schemapermissionresponse)   | false | none | PermissionResponse                                 | none |
| »» id                                              | integer                                           | true  | none | Id                                                 | none |
| »» name                                            | string                                            | true  | none | Name                                               | none |
| »» description                                     | any                                               | true  | none | Description                                        | none |

_anyOf_

| 名称            | 类型   | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------ | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称        | 类型 | 必选 | 约束 | 中文名   | 说明 |
| ----------- | ---- | ---- | ---- | -------- | ---- |
| »» resource | any  | true | none | Resource | none |

_anyOf_

| 名称            | 类型   | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------ | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

<a id="opIdassign_role_to_user_api_users__user_id__roles__role_id__post"></a>

## POST Assign Role To User

POST /api/users/{user_id}/roles/{role_id}

为用户分配角色（需要管理员权限）

### 请求参数

| 名称    | 位置 | 类型    | 必选 | 中文名  | 说明 |
| ------- | ---- | ------- | ---- | ------- | ---- |
| user_id | path | integer | 是   | User Id | none |
| role_id | path | integer | 是   | Role Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdremove_role_from_user_api_users__user_id__roles__role_id__delete"></a>

## DELETE Remove Role From User

DELETE /api/users/{user_id}/roles/{role_id}

移除用户角色（需要管理员权限）

### 请求参数

| 名称    | 位置 | 类型    | 必选 | 中文名  | 说明 |
| ------- | ---- | ------- | ---- | ------- | ---- |
| user_id | path | integer | 是   | User Id | none |
| role_id | path | integer | 是   | Role Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

# 任务管理

<a id="opIdcreate_task_api_tasks__post"></a>

## POST Create Task

POST /api/tasks/

创建新任务（教师权限）

> Body 请求参数

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z",
  "student_ids": [0]
}
```

### 请求参数

| 名称 | 位置 | 类型                            | 必选 | 中文名     | 说明 |
| ---- | ---- | ------------------------------- | ---- | ---------- | ---- |
| body | body | [TaskCreate](#schemataskcreate) | 否   | TaskCreate | none |

> 返回示例

> 200 Response

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z",
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "assigned_count": 0,
  "completed_count": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [TaskResponse](#schemataskresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdget_tasks_api_tasks__get"></a>

## GET Get Tasks

GET /api/tasks/

获取任务列表

- 教师：获取自己创建的所有任务
- 学生：获取分配给自己的所有任务

### 请求参数

| 名称  | 位置  | 类型    | 必选 | 中文名 | 说明 |
| ----- | ----- | ------- | ---- | ------ | ---- |
| skip  | query | integer | 否   | Skip   | none |
| limit | query | integer | 否   | Limit  | none |

> 返回示例

> 200 Response

```json
[
  {
    "title": "string",
    "description": "string",
    "due_date": "2019-08-24T14:15:22Z",
    "id": 0,
    "created_by_id": 0,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z",
    "assigned_count": 0,
    "completed_count": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **200**

_Response Get Tasks Api Tasks Get_

| 名称                             | 类型                                  | 必选  | 约束 | 中文名                           | 说明 |
| -------------------------------- | ------------------------------------- | ----- | ---- | -------------------------------- | ---- |
| Response Get Tasks Api Tasks Get | [[TaskResponse](#schemataskresponse)] | false | none | Response Get Tasks Api Tasks Get | none |
| » TaskResponse                   | [TaskResponse](#schemataskresponse)   | false | none | TaskResponse                     | none |
| »» title                         | string                                | true  | none | Title                            | none |
| »» description                   | any                                   | false | none | Description                      | none |

_anyOf_

| 名称            | 类型   | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------ | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称        | 类型 | 必选  | 约束 | 中文名   | 说明 |
| ----------- | ---- | ----- | ---- | -------- | ---- |
| »» due_date | any  | false | none | Due Date | none |

_anyOf_

| 名称            | 类型              | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ----------------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string(date-time) | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称             | 类型              | 必选  | 约束 | 中文名        | 说明 |
| ---------------- | ----------------- | ----- | ---- | ------------- | ---- |
| »» id            | integer           | true  | none | Id            | none |
| »» created_by_id | integer           | true  | none | Created By Id | none |
| »» created_at    | string(date-time) | true  | none | Created At    | none |
| »» updated_at    | any               | false | none | Updated At    | none |

_anyOf_

| 名称            | 类型              | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ----------------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string(date-time) | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称              | 类型 | 必选  | 约束 | 中文名         | 说明 |
| ----------------- | ---- | ----- | ---- | -------------- | ---- |
| »» assigned_count | any  | false | none | Assigned Count | none |

_anyOf_

| 名称            | 类型    | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | integer | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称               | 类型 | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ---- | ----- | ---- | --------------- | ---- |
| »» completed_count | any  | false | none | Completed Count | none |

_anyOf_

| 名称            | 类型    | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | integer | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_assigned_tasks_api_tasks_assigned__get"></a>

## GET Get Assigned Tasks

GET /api/tasks/assigned/

获取分配给当前用户的任务（学生功能）

> 返回示例

> 200 Response

```json
[
  {
    "id": 0,
    "task_id": 0,
    "student_id": 0,
    "created_at": "2019-08-24T14:15:22Z",
    "is_completed": true,
    "task": {
      "title": "string",
      "description": "string",
      "due_date": "2019-08-24T14:15:22Z",
      "id": 0,
      "created_by_id": 0,
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z",
      "assigned_count": 0,
      "completed_count": 0
    },
    "submission": {
      "content": "string",
      "file_path": "string",
      "id": 0,
      "task_id": 0,
      "student_id": 0,
      "submitted_at": "2019-08-24T14:15:22Z",
      "score": 0,
      "feedback": "string",
      "graded_at": "2019-08-24T14:15:22Z"
    }
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response Get Assigned Tasks Api Tasks Assigned Get_

| 名称                                               | 类型                                                  | 必选  | 约束 | 中文名                                             | 说明 |
| -------------------------------------------------- | ----------------------------------------------------- | ----- | ---- | -------------------------------------------------- | ---- |
| Response Get Assigned Tasks Api Tasks Assigned Get | [[AssignedTaskResponse](#schemaassignedtaskresponse)] | false | none | Response Get Assigned Tasks Api Tasks Assigned Get | none |
| » AssignedTaskResponse                             | [AssignedTaskResponse](#schemaassignedtaskresponse)   | false | none | AssignedTaskResponse                               | none |
| »» id                                              | integer                                               | true  | none | Id                                                 | none |
| »» task_id                                         | integer                                               | true  | none | Task Id                                            | none |
| »» student_id                                      | integer                                               | true  | none | Student Id                                         | none |
| »» created_at                                      | string(date-time)                                     | true  | none | Created At                                         | none |
| »» is_completed                                    | boolean                                               | true  | none | Is Completed                                       | none |
| »» task                                            | [TaskResponse](#schemataskresponse)                   | true  | none | TaskResponse                                       | none |
| »»» title                                          | string                                                | true  | none | Title                                              | none |
| »»» description                                    | any                                                   | false | none | Description                                        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称         | 类型 | 必选  | 约束 | 中文名   | 说明 |
| ------------ | ---- | ----- | ---- | -------- | ---- |
| »»» due_date | any  | false | none | Due Date | none |

_anyOf_

| 名称             | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ----------------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string(date-time) | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称              | 类型              | 必选  | 约束 | 中文名        | 说明 |
| ----------------- | ----------------- | ----- | ---- | ------------- | ---- |
| »»» id            | integer           | true  | none | Id            | none |
| »»» created_by_id | integer           | true  | none | Created By Id | none |
| »»» created_at    | string(date-time) | true  | none | Created At    | none |
| »»» updated_at    | any               | false | none | Updated At    | none |

_anyOf_

| 名称             | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ----------------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string(date-time) | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称               | 类型 | 必选  | 约束 | 中文名         | 说明 |
| ------------------ | ---- | ----- | ---- | -------------- | ---- |
| »»» assigned_count | any  | false | none | Assigned Count | none |

_anyOf_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称                | 类型 | 必选  | 约束 | 中文名          | 说明 |
| ------------------- | ---- | ----- | ---- | --------------- | ---- |
| »»» completed_count | any  | false | none | Completed Count | none |

_anyOf_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称          | 类型                                                         | 必选  | 约束 | 中文名                 | 说明 |
| ------------- | ------------------------------------------------------------ | ----- | ---- | ---------------------- | ---- |
| »» submission | [TaskSubmissionResponse](#schematasksubmissionresponse)¦null | false | none | TaskSubmissionResponse | none |
| »»» content   | any                                                          | false | none | Content                | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称          | 类型 | 必选  | 约束 | 中文名    | 说明 |
| ------------- | ---- | ----- | ---- | --------- | ---- |
| »»» file_path | any  | false | none | File Path | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称             | 类型              | 必选  | 约束 | 中文名       | 说明 |
| ---------------- | ----------------- | ----- | ---- | ------------ | ---- |
| »»» id           | integer           | true  | none | Id           | none |
| »»» task_id      | integer           | true  | none | Task Id      | none |
| »»» student_id   | integer           | true  | none | Student Id   | none |
| »»» submitted_at | string(date-time) | true  | none | Submitted At | none |
| »»» score        | any               | false | none | Score        | none |

_anyOf_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称         | 类型 | 必选  | 约束 | 中文名   | 说明 |
| ------------ | ---- | ----- | ---- | -------- | ---- |
| »»» feedback | any  | false | none | Feedback | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称          | 类型 | 必选  | 约束 | 中文名    | 说明 |
| ------------- | ---- | ----- | ---- | --------- | ---- |
| »»» graded_at | any  | false | none | Graded At | none |

_anyOf_

| 名称             | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ----------------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string(date-time) | false | none |        | none |

_or_

| 名称             | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ---- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | null | false | none |        | none |

<a id="opIdget_task_api_tasks__task_id__get"></a>

## GET Get Task

GET /api/tasks/{task_id}

获取任务详情

### 请求参数

| 名称    | 位置 | 类型    | 必选 | 中文名  | 说明 |
| ------- | ---- | ------- | ---- | ------- | ---- |
| task_id | path | integer | 是   | Task Id | none |

> 返回示例

> 200 Response

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z",
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "assigned_count": 0,
  "completed_count": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [TaskResponse](#schemataskresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdupdate_task_api_tasks__task_id__put"></a>

## PUT Update Task

PUT /api/tasks/{task_id}

更新任务（教师权限）

> Body 请求参数

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z"
}
```

### 请求参数

| 名称    | 位置 | 类型                            | 必选 | 中文名     | 说明 |
| ------- | ---- | ------------------------------- | ---- | ---------- | ---- |
| task_id | path | integer                         | 是   | Task Id    | none |
| body    | body | [TaskUpdate](#schemataskupdate) | 否   | TaskUpdate | none |

> 返回示例

> 200 Response

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z",
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "assigned_count": 0,
  "completed_count": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [TaskResponse](#schemataskresponse)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIddelete_task_api_tasks__task_id__delete"></a>

## DELETE Delete Task

DELETE /api/tasks/{task_id}

删除任务（教师权限）

### 请求参数

| 名称    | 位置 | 类型    | 必选 | 中文名  | 说明 |
| ------- | ---- | ------- | ---- | ------- | ---- |
| task_id | path | integer | 是   | Task Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdcomplete_assigned_task_api_tasks_assigned__assigned_task_id__complete__post"></a>

## POST Complete Assigned Task

POST /api/tasks/assigned/{assigned_task_id}/complete/

确认任务完成（学生功能）

### 请求参数

| 名称             | 位置 | 类型    | 必选 | 中文名           | 说明 |
| ---------------- | ---- | ------- | ---- | ---------------- | ---- |
| assigned_task_id | path | integer | 是   | Assigned Task Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

# 讨论区

<a id="opIdcreate_topic_api_topics__post"></a>

## POST Create Topic

POST /api/topics/

> Body 请求参数

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false
}
```

### 请求参数

| 名称 | 位置 | 类型                              | 必选 | 中文名      | 说明 |
| ---- | ---- | --------------------------------- | ---- | ----------- | ---- |
| body | body | [TopicCreate](#schematopiccreate) | 否   | TopicCreate | none |

> 返回示例

> 201 Response

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false,
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "created_by_name": "string",
  "replies_count": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 201    | [Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)             | Successful Response | [TopicResponse](#schematopicresponse)             |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdread_topics_api_topics__get"></a>

## GET Read Topics

GET /api/topics/

### 请求参数

| 名称   | 位置  | 类型    | 必选 | 中文名 | 说明 |
| ------ | ----- | ------- | ---- | ------ | ---- |
| skip   | query | integer | 否   | Skip   | none |
| limit  | query | integer | 否   | Limit  | none |
| search | query | any     | 否   | Search | none |

> 返回示例

> 200 Response

```json
[
  {
    "title": "string",
    "content": "string",
    "is_sticky": false,
    "is_closed": false,
    "id": 0,
    "created_by_id": 0,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z",
    "created_by_name": "string",
    "replies_count": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **200**

_Response Read Topics Api Topics Get_

| 名称                                | 类型                                    | 必选  | 约束 | 中文名                              | 说明 |
| ----------------------------------- | --------------------------------------- | ----- | ---- | ----------------------------------- | ---- |
| Response Read Topics Api Topics Get | [[TopicResponse](#schematopicresponse)] | false | none | Response Read Topics Api Topics Get | none |
| » TopicResponse                     | [TopicResponse](#schematopicresponse)   | false | none | TopicResponse                       | none |
| »» title                            | string                                  | true  | none | Title                               | none |
| »» content                          | string                                  | true  | none | Content                             | none |
| »» is_sticky                        | any                                     | false | none | Is Sticky                           | none |

_anyOf_

| 名称            | 类型    | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | boolean | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称         | 类型 | 必选  | 约束 | 中文名    | 说明 |
| ------------ | ---- | ----- | ---- | --------- | ---- |
| »» is_closed | any  | false | none | Is Closed | none |

_anyOf_

| 名称            | 类型    | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | boolean | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称             | 类型              | 必选  | 约束 | 中文名        | 说明 |
| ---------------- | ----------------- | ----- | ---- | ------------- | ---- |
| »» id            | integer           | true  | none | Id            | none |
| »» created_by_id | integer           | true  | none | Created By Id | none |
| »» created_at    | string(date-time) | true  | none | Created At    | none |
| »» updated_at    | any               | false | none | Updated At    | none |

_anyOf_

| 名称            | 类型              | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ----------------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string(date-time) | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称               | 类型 | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ---- | ----- | ---- | --------------- | ---- |
| »» created_by_name | any  | false | none | Created By Name | none |

_anyOf_

| 名称            | 类型   | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------ | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称             | 类型 | 必选  | 约束 | 中文名        | 说明 |
| ---------------- | ---- | ----- | ---- | ------------- | ---- |
| »» replies_count | any  | false | none | Replies Count | none |

_anyOf_

| 名称            | 类型    | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | integer | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdread_topic_api_topics__topic_id___get"></a>

## GET Read Topic

GET /api/topics/{topic_id}/

### 请求参数

| 名称     | 位置 | 类型    | 必选 | 中文名   | 说明 |
| -------- | ---- | ------- | ---- | -------- | ---- |
| topic_id | path | integer | 是   | Topic Id | none |

> 返回示例

> 200 Response

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false,
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "created_by_name": "string",
  "replies_count": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [TopicResponse](#schematopicresponse)             |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdupdate_topic_api_topics__topic_id___put"></a>

## PUT Update Topic

PUT /api/topics/{topic_id}/

> Body 请求参数

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false
}
```

### 请求参数

| 名称     | 位置 | 类型                              | 必选 | 中文名      | 说明 |
| -------- | ---- | --------------------------------- | ---- | ----------- | ---- |
| topic_id | path | integer                           | 是   | Topic Id    | none |
| body     | body | [TopicUpdate](#schematopicupdate) | 否   | TopicUpdate | none |

> 返回示例

> 200 Response

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false,
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "created_by_name": "string",
  "replies_count": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [TopicResponse](#schematopicresponse)             |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIddelete_topic_api_topics__topic_id___delete"></a>

## DELETE Delete Topic

DELETE /api/topics/{topic_id}/

### 请求参数

| 名称     | 位置 | 类型    | 必选 | 中文名   | 说明 |
| -------- | ---- | ------- | ---- | -------- | ---- |
| topic_id | path | integer | 是   | Topic Id | none |

> 返回示例

> 422 Response

```json
{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 204    | [No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)          | Successful Response | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdread_topic_replies_api_topics__topic_id__replies__get"></a>

## GET Read Topic Replies

GET /api/topics/{topic_id}/replies/

### 请求参数

| 名称     | 位置  | 类型    | 必选 | 中文名   | 说明 |
| -------- | ----- | ------- | ---- | -------- | ---- |
| topic_id | path  | integer | 是   | Topic Id | none |
| skip     | query | integer | 否   | Skip     | none |
| limit    | query | integer | 否   | Limit    | none |

> 返回示例

> 200 Response

```json
[
  {
    "content": "string",
    "id": 0,
    "topic_id": 0,
    "created_by_id": 0,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z",
    "created_by_name": "string"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **200**

_Response Read Topic Replies Api Topics Topic Id Replies Get_

| 名称                                                        | 类型                                    | 必选  | 约束 | 中文名                                                      | 说明 |
| ----------------------------------------------------------- | --------------------------------------- | ----- | ---- | ----------------------------------------------------------- | ---- |
| Response Read Topic Replies Api Topics Topic Id Replies Get | [[ReplyResponse](#schemareplyresponse)] | false | none | Response Read Topic Replies Api Topics Topic Id Replies Get | none |
| » ReplyResponse                                             | [ReplyResponse](#schemareplyresponse)   | false | none | ReplyResponse                                               | none |
| »» content                                                  | string                                  | true  | none | Content                                                     | none |
| »» id                                                       | integer                                 | true  | none | Id                                                          | none |
| »» topic_id                                                 | integer                                 | true  | none | Topic Id                                                    | none |
| »» created_by_id                                            | integer                                 | true  | none | Created By Id                                               | none |
| »» created_at                                               | string(date-time)                       | true  | none | Created At                                                  | none |
| »» updated_at                                               | any                                     | false | none | Updated At                                                  | none |

_anyOf_

| 名称            | 类型              | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ----------------- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string(date-time) | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

_continued_

| 名称               | 类型 | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ---- | ----- | ---- | --------------- | ---- |
| »» created_by_name | any  | false | none | Created By Name | none |

_anyOf_

| 名称            | 类型   | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ------ | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | string | false | none |        | none |

_or_

| 名称            | 类型 | 必选  | 约束 | 中文名 | 说明 |
| --------------- | ---- | ----- | ---- | ------ | ---- |
| »»» _anonymous_ | null | false | none |        | none |

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdcreate_reply_api_topics__topic_id__replies__post"></a>

## POST Create Reply

POST /api/topics/{topic_id}/replies/

> Body 请求参数

```json
{
  "content": "string"
}
```

### 请求参数

| 名称     | 位置 | 类型                              | 必选 | 中文名      | 说明 |
| -------- | ---- | --------------------------------- | ---- | ----------- | ---- |
| topic_id | path | integer                           | 是   | Topic Id    | none |
| body     | body | [ReplyCreate](#schemareplycreate) | 否   | ReplyCreate | none |

> 返回示例

> 201 Response

```json
{
  "content": "string",
  "id": 0,
  "topic_id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "created_by_name": "string"
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 201    | [Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)             | Successful Response | [ReplyResponse](#schemareplyresponse)             |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdupdate_reply_api_topics_replies__reply_id___put"></a>

## PUT Update Reply

PUT /api/topics/replies/{reply_id}/

> Body 请求参数

```json
{
  "content": "string"
}
```

### 请求参数

| 名称     | 位置 | 类型                          | 必选 | 中文名    | 说明 |
| -------- | ---- | ----------------------------- | ---- | --------- | ---- |
| reply_id | path | integer                       | 是   | Reply Id  | none |
| body     | body | [ReplyBase](#schemareplybase) | 否   | ReplyBase | none |

> 返回示例

> 200 Response

```json
{
  "content": "string",
  "id": 0,
  "topic_id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "created_by_name": "string"
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [ReplyResponse](#schemareplyresponse)             |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIddelete_reply_api_topics_replies__reply_id___delete"></a>

## DELETE Delete Reply

DELETE /api/topics/replies/{reply_id}/

### 请求参数

| 名称     | 位置 | 类型    | 必选 | 中文名   | 说明 |
| -------- | ---- | ------- | ---- | -------- | ---- |
| reply_id | path | integer | 是   | Reply Id | none |

> 返回示例

> 422 Response

```json
{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 204    | [No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)          | Successful Response | None                                              |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

# 文件资源

<a id="opIdupload_resource_api_resource_upload_post"></a>

## POST 上传资源文件

POST /api/resource/upload

> Body 请求参数

```yaml
file: ""
title: ""
type: ""
description: ""
sync_knowledge: "false"
```

### 请求参数

| 名称             | 位置 | 类型           | 必选 | 中文名         | 说明                 |
| ---------------- | ---- | -------------- | ---- | -------------- | -------------------- |
| body             | body | object         | 否   |                | none                 |
| » file           | body | string(binary) | 是   | File           | none                 |
| » title          | body | string         | 是   | Title          | 文件标题             |
| » type           | body | string         | 是   | Type           | 文件类型分类         |
| » description    | body | any            | 否   | Description    | 资源详细描述（可选） |
| »» _anonymous_   | body | string         | 否   |                | none                 |
| »» _anonymous_   | body | null           | 否   |                | none                 |
| » sync_knowledge | body | any            | 否   | Sync Knowledge | 是否同步到知识图谱   |
| »» _anonymous_   | body | boolean        | 否   |                | none                 |
| »» _anonymous_   | body | null           | 否   |                | none                 |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_resources_api_resources_get"></a>

## GET 获取文件资源列表

GET /api/resources

### 请求参数

| 名称      | 位置  | 类型    | 必选 | 中文名    | 说明 |
| --------- | ----- | ------- | ---- | --------- | ---- |
| skip      | query | integer | 否   | Skip      | none |
| limit     | query | integer | 否   | Limit     | none |
| title     | query | any     | 否   | Title     | none |
| file_type | query | any     | 否   | File Type | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_resource_api_resources__file_id__delete"></a>

## DELETE 删除文件资源

DELETE /api/resources/{file_id}

### 请求参数

| 名称    | 位置 | 类型   | 必选 | 中文名  | 说明 |
| ------- | ---- | ------ | ---- | ------- | ---- |
| file_id | path | string | 是   | File Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdupdate_resource_api_resources__file_id__put"></a>

## PUT 编辑资源信息

PUT /api/resources/{file_id}

> Body 请求参数

```json
{}
```

### 请求参数

| 名称    | 位置 | 类型   | 必选 | 中文名       | 说明 |
| ------- | ---- | ------ | ---- | ------------ | ---- |
| file_id | path | string | 是   | File Id      | none |
| body    | body | object | 否   | Request Data | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddownload_file_api_resources__filename__get"></a>

## GET 下载文件资源

GET /api/resources/{filename}

### 请求参数

| 名称     | 位置 | 类型   | 必选 | 中文名   | 说明 |
| -------- | ---- | ------ | ---- | -------- | ---- |
| filename | path | string | 是   | Filename | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

# 题库

<a id="opIdadd_question_api_question_add_post"></a>

## POST 添加题目

POST /api/question/add

> Body 请求参数

```yaml
text: ""
type: ""
options: ""
answer: ""
code_examples: ""
code_language: python
knowledge_id: ""
difficulty: "0.5"
```

### 请求参数

| 名称            | 位置 | 类型   | 必选 | 中文名        | 说明                                                                   |
| --------------- | ---- | ------ | ---- | ------------- | ---------------------------------------------------------------------- |
| body            | body | object | 否   |               | none                                                                   |
| » text          | body | string | 是   | Text          | 题目内容                                                               |
| » type          | body | string | 是   | Type          | 题目类型(choice/fill/code)                                             |
| » options       | body | any    | 否   | Options       | 选项(JSON 格式，仅选择题)                                              |
| »» _anonymous_  | body | string | 否   |               | none                                                                   |
| »» _anonymous_  | body | null   | 否   |               | none                                                                   |
| » answer        | body | string | 是   | Answer        | 正确答案（编程题可填写参考说明）                                       |
| » code_examples | body | any    | 否   | Code Examples | 编程题测试用例(JSON 数组，每项包含 input 和 output 字段，仅编程题必填) |
| »» _anonymous_  | body | string | 否   |               | none                                                                   |
| »» _anonymous_  | body | null   | 否   |               | none                                                                   |
| » code_language | body | any    | 否   | Code Language | 编程语言类型(python/c/cpp/java，仅编程题有效)                          |
| »» _anonymous_  | body | string | 否   |               | none                                                                   |
| »» _anonymous_  | body | null   | 否   |               | none                                                                   |
| » knowledge_id  | body | string | 是   | Knowledge Id  | 知识点 ID 列表(JSON 格式)                                              |
| » difficulty    | body | any    | 否   | Difficulty    | 难度系数(0-1)                                                          |
| »» _anonymous_  | body | number | 否   |               | none                                                                   |
| »» _anonymous_  | body | null   | 否   |               | none                                                                   |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_question_api_question_delete_delete"></a>

## DELETE 删除题目

DELETE /api/question/delete

### 请求参数

| 名称        | 位置  | 类型    | 必选 | 中文名      | 说明 |
| ----------- | ----- | ------- | ---- | ----------- | ---- |
| question_id | query | integer | 是   | Question Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_question_list_api_question_list_get"></a>

## GET 获取题目列表（教师）

GET /api/question/list

### 请求参数

| 名称         | 位置  | 类型    | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------- | ---- | ------------ | ---- |
| skip         | query | integer | 否   | Skip         | none |
| limit        | query | integer | 否   | Limit        | none |
| knowledge_id | query | any     | 否   | Knowledge Id | none |
| type         | query | any     | 否   | Type         | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_knowledge_nodes_api_question_knowledge_list_get"></a>

## GET 获取知识点列表

GET /api/question/knowledge/list

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

<a id="opIdget_questions_for_student_api_question_get_get"></a>

## GET 获取题目（学生）

GET /api/question/get

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 是   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdsubmit_answers_api_question_submit_post"></a>

## POST 提交答案

POST /api/question/submit

> Body 请求参数

```json
{
  "answers": [
    {
      "question_id": 0,
      "student_answer": "string"
    }
  ],
  "time_spent": 0,
  "knowledge_id": "string"
}
```

### 请求参数

| 名称 | 位置 | 类型                                  | 必选 | 中文名        | 说明 |
| ---- | ---- | ------------------------------------- | ---- | ------------- | ---- |
| body | body | [SubmitRequest](#schemasubmitrequest) | 否   | SubmitRequest | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_answer_records_api_question_record_list_get"></a>

## GET 获取答题记录列表

GET /api/question/record/list

### 请求参数

| 名称    | 位置  | 类型    | 必选 | 中文名  | 说明 |
| ------- | ----- | ------- | ---- | ------- | ---- |
| user_id | query | integer | 否   | User Id | none |
| skip    | query | integer | 否   | Skip    | none |
| limit   | query | integer | 否   | Limit   | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_answer_record_detail_api_question_record_detail_get"></a>

## GET 获取详细答题记录

GET /api/question/record/detail

### 请求参数

| 名称      | 位置  | 类型    | 必选 | 中文名    | 说明 |
| --------- | ----- | ------- | ---- | --------- | ---- |
| record_id | query | integer | 是   | Record Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

# AI 助手

<a id="opIdlist_conversations_api_ai_conversations_get"></a>

## GET List Conversations

GET /api/ai/conversations

> 返回示例

> 200 Response

```json
[
  {
    "id": "string",
    "title": "string",
    "created_at": "2019-08-24T14:15:22Z"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Conversations Api Ai Conversations Get_

| 名称                                                 | 类型                                                | 必选  | 约束 | 中文名                                               | 说明 |
| ---------------------------------------------------- | --------------------------------------------------- | ----- | ---- | ---------------------------------------------------- | ---- |
| Response List Conversations Api Ai Conversations Get | [[ConversationSummary](#schemaconversationsummary)] | false | none | Response List Conversations Api Ai Conversations Get | none |
| » ConversationSummary                                | [ConversationSummary](#schemaconversationsummary)   | false | none | ConversationSummary                                  | none |
| »» id                                                | string                                              | true  | none | Id                                                   | none |
| »» title                                             | string                                              | true  | none | Title                                                | none |
| »» created_at                                        | string(date-time)                                   | true  | none | Created At                                           | none |

<a id="opIdcreate_conversation_api_ai_conversations_post"></a>

## POST Create Conversation

POST /api/ai/conversations

> Body 请求参数

```json
{
  "title": "string"
}
```

### 请求参数

| 名称 | 位置 | 类型                                            | 必选 | 中文名             | 说明 |
| ---- | ---- | ----------------------------------------------- | ---- | ------------------ | ---- |
| body | body | [ConversationCreate](#schemaconversationcreate) | 否   | ConversationCreate | none |

> 返回示例

> 200 Response

```json
{
  "id": "string",
  "title": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [ConversationSummary](#schemaconversationsummary) |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIddelete_conversation_api_ai_conversations__conv_id__delete"></a>

## DELETE Delete Conversation

DELETE /api/ai/conversations/{conv_id}

### 请求参数

| 名称    | 位置 | 类型   | 必选 | 中文名  | 说明 |
| ------- | ---- | ------ | ---- | ------- | ---- |
| conv_id | path | string | 是   | Conv Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdrename_conversation_api_ai_conversations__conv_id__put"></a>

## PUT Rename Conversation

PUT /api/ai/conversations/{conv_id}

> Body 请求参数

```json
{
  "title": "string"
}
```

### 请求参数

| 名称    | 位置 | 类型                                            | 必选 | 中文名             | 说明 |
| ------- | ---- | ----------------------------------------------- | ---- | ------------------ | ---- |
| conv_id | path | string                                          | 是   | Conv Id            | none |
| body    | body | [ConversationCreate](#schemaconversationcreate) | 否   | ConversationCreate | none |

> 返回示例

> 200 Response

```json
{
  "id": "string",
  "title": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [ConversationSummary](#schemaconversationsummary) |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdsend_message_api_ai_conversations__conv_id__messages_post"></a>

## POST Send Message

POST /api/ai/conversations/{conv_id}/messages

> Body 请求参数

```json
{
  "user_input": "string"
}
```

### 请求参数

| 名称    | 位置 | 类型                          | 必选 | 中文名    | 说明 |
| ------- | ---- | ----------------------------- | ---- | --------- | ---- |
| conv_id | path | string                        | 是   | Conv Id   | none |
| body    | body | [MessageIn](#schemamessagein) | 否   | MessageIn | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_messages_api_ai_conversations__conv_id__messages_get"></a>

## GET Get Messages

GET /api/ai/conversations/{conv_id}/messages

### 请求参数

| 名称    | 位置 | 类型   | 必选 | 中文名  | 说明 |
| ------- | ---- | ------ | ---- | ------- | ---- |
| conv_id | path | string | 是   | Conv Id | none |

> 返回示例

> 200 Response

```json
{
  "id": "string",
  "title": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "messages": []
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [ConversationOut](#schemaconversationout)         |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdeasy_chat_api_ai_easychat_post"></a>

## POST Easy Chat

POST /api/ai/easychat

### 请求参数

| 名称 | 位置  | 类型   | 必选 | 中文名 | 说明 |
| ---- | ----- | ------ | ---- | ------ | ---- |
| msg  | query | string | 是   | Msg    | none |

> 返回示例

> 200 Response

```json
"string"
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | string                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

# 知识图谱

<a id="opIdread_graph_api_graph_get"></a>

## GET Read Graph

GET /api/graph

> 返回示例

> 200 Response

```json
{
  "nodes": [
    {
      "id": "string",
      "category": "Course",
      "name": "string",
      "description": "string",
      "depth": 0
    }
  ],
  "edges": [
    {
      "source": "string",
      "target": "string",
      "relation": "string"
    }
  ],
  "resources": [
    {
      "id": "string",
      "name": "string"
    }
  ]
}
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型                            |
| ------ | ------------------------------------------------------- | ------------------- | ----------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | [GraphDataOut](#schemagraphdataout) |

<a id="opIdupdate_graph_api_graph_put"></a>

## PUT Update Graph

PUT /api/graph

> Body 请求参数

```json
{
  "nodes": [
    {
      "id": "string",
      "category": "Course",
      "name": "string",
      "description": "string",
      "depth": 0
    }
  ],
  "edges": [
    {
      "source": "string",
      "target": "string",
      "relation": "string"
    }
  ]
}
```

### 请求参数

| 名称 | 位置 | 类型                          | 必选 | 中文名    | 说明 |
| ---- | ---- | ----------------------------- | ---- | --------- | ---- |
| body | body | [GraphData](#schemagraphdata) | 否   | GraphData | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdbatch_add_nodes_edges_api_graph_post"></a>

## POST Batch Add Nodes Edges

POST /api/graph

> Body 请求参数

```json
{
  "nodes": [
    {
      "id": "string",
      "category": "Course",
      "name": "string",
      "description": "string",
      "depth": 0
    }
  ],
  "edges": [
    {
      "source": "string",
      "target": "string",
      "relation": "string"
    }
  ]
}
```

### 请求参数

| 名称 | 位置 | 类型                          | 必选 | 中文名    | 说明 |
| ---- | ---- | ----------------------------- | ---- | --------- | ---- |
| body | body | [GraphData](#schemagraphdata) | 否   | GraphData | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_graph_api_graph_delete"></a>

## DELETE Delete Graph

DELETE /api/graph

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

<a id="opIdget_node_detail_api_api_node_detail__node_id__get"></a>

## GET Get Node Detail Api

GET /api/node/detail/{node_id}

### 请求参数

| 名称    | 位置 | 类型   | 必选 | 中文名  | 说明 |
| ------- | ---- | ------ | ---- | ------- | ---- |
| node_id | path | string | 是   | Node Id | none |

> 返回示例

> 200 Response

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "total_time": 0,
  "average_time": 0,
  "resources": [
    {
      "id": "string",
      "name": "string",
      "type": "string",
      "download_url": "string",
      "is_child": false
    }
  ],
  "prerequisites": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "successors": [
    {
      "id": "string",
      "name": "string"
    }
  ]
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [NodeDetail](#schemanodedetail)                   |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdget_all_nodes_api_node_knowledge_all_get"></a>

## GET Get All Nodes

GET /api/node/knowledge/all

> 返回示例

> 200 Response

```json
[
  {
    "id": "string",
    "name": "string"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response Get All Nodes Api Node Knowledge All Get_

| 名称                                              | 类型                                    | 必选  | 约束 | 中文名                                            | 说明 |
| ------------------------------------------------- | --------------------------------------- | ----- | ---- | ------------------------------------------------- | ---- |
| Response Get All Nodes Api Node Knowledge All Get | [[KnowledgeInfo](#schemaknowledgeinfo)] | false | none | Response Get All Nodes Api Node Knowledge All Get | none |
| » KnowledgeInfo                                   | [KnowledgeInfo](#schemaknowledgeinfo)   | false | none | KnowledgeInfo                                     | none |
| »» id                                             | string                                  | true  | none | Id                                                | none |
| »» name                                           | string                                  | true  | none | Name                                              | none |

<a id="opIdadd_node_api_node_post"></a>

## POST Add Node

POST /api/node

> Body 请求参数

```json
{
  "id": "string",
  "category": "Course",
  "name": "string",
  "description": "string",
  "depth": 0
}
```

### 请求参数

| 名称 | 位置 | 类型 | 必选 | 中文名 | 说明 |
| ---- | ---- | ---- | ---- | ------ | ---- |
| body | body | any  | 否   | Node   | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdupdate_node_api_node__node_id__put"></a>

## PUT Update Node

PUT /api/node/{node_id}

> Body 请求参数

```json
{
  "id": "string",
  "category": "Course",
  "name": "string",
  "description": "string",
  "depth": 0
}
```

### 请求参数

| 名称    | 位置 | 类型   | 必选 | 中文名 | 说明 |
| ------- | ---- | ------ | ---- | ------ | ---- |
| node_id | path | string | 是   |        | none |
| body    | body | any    | 否   | Node   | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_node_api_node__node_id__delete"></a>

## DELETE Delete Node

DELETE /api/node/{node_id}

### 请求参数

| 名称    | 位置 | 类型   | 必选 | 中文名  | 说明 |
| ------- | ---- | ------ | ---- | ------- | ---- |
| node_id | path | string | 是   | Node Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdadd_edge_api_edge_post"></a>

## POST Add Edge

POST /api/edge

> Body 请求参数

```json
{
  "source": "string",
  "target": "string",
  "relation": "string"
}
```

### 请求参数

| 名称 | 位置 | 类型                          | 必选 | 中文名    | 说明 |
| ---- | ---- | ----------------------------- | ---- | --------- | ---- |
| body | body | [GraphEdge](#schemagraphedge) | 否   | GraphEdge | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_edge_api_edge_delete"></a>

## DELETE Delete Edge

DELETE /api/edge

### 请求参数

| 名称     | 位置  | 类型   | 必选 | 中文名   | 说明 |
| -------- | ----- | ------ | ---- | -------- | ---- |
| source   | query | string | 是   | Source   | none |
| target   | query | string | 是   | Target   | none |
| relation | query | string | 是   | Relation | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

# 学习记录

<a id="opIdadd_record_api_records__post"></a>

## POST Add Record

POST /api/records/

> Body 请求参数

```json
{
  "student_id": 0,
  "resource_id": "string",
  "status": 0,
  "total_time": 0,
  "page_times": [0]
}
```

### 请求参数

| 名称 | 位置 | 类型                                                | 必选 | 中文名               | 说明 |
| ---- | ---- | --------------------------------------------------- | ---- | -------------------- | ---- |
| body | body | [LearningRecordCreate](#schemalearningrecordcreate) | 否   | LearningRecordCreate | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdadd_records_batch_api_records_batch_post"></a>

## POST Add Records Batch

POST /api/records/batch

> Body 请求参数

```json
[
  {
    "student_id": 0,
    "resource_id": "string",
    "status": 0,
    "total_time": 0,
    "page_times": [0]
  }
]
```

### 请求参数

| 名称 | 位置 | 类型                                                | 必选 | 中文名  | 说明 |
| ---- | ---- | --------------------------------------------------- | ---- | ------- | ---- |
| body | body | [LearningRecordCreate](#schemalearningrecordcreate) | 否   | Records | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_all_students_daily_records_api_records_detail__date__get"></a>

## GET Get All Students Daily Records

GET /api/records/detail/{date}

### 请求参数

| 名称 | 位置 | 类型   | 必选 | 中文名 | 说明 |
| ---- | ---- | ------ | ---- | ------ | ---- |
| date | path | string | 是   | Date   | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_all_students_daily_records_api_records_detail__date__delete"></a>

## DELETE Delete All Students Daily Records

DELETE /api/records/detail/{date}

### 请求参数

| 名称 | 位置 | 类型   | 必选 | 中文名 | 说明 |
| ---- | ---- | ------ | ---- | ------ | ---- |
| date | path | string | 是   | Date   | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_daily_records_api_records_detail__date___student_id__get"></a>

## GET Get Daily Records

GET /api/records/detail/{date}/{student_id}

### 请求参数

| 名称       | 位置 | 类型    | 必选 | 中文名     | 说明 |
| ---------- | ---- | ------- | ---- | ---------- | ---- |
| date       | path | string  | 是   | Date       | none |
| student_id | path | integer | 是   | Student Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_daily_records_api_records_detail__date___student_id__delete"></a>

## DELETE Delete Daily Records

DELETE /api/records/detail/{date}/{student_id}

### 请求参数

| 名称       | 位置 | 类型    | 必选 | 中文名     | 说明 |
| ---------- | ---- | ------- | ---- | ---------- | ---- |
| date       | path | string  | 是   | Date       | none |
| student_id | path | integer | 是   | Student Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_all_year_records_api_records__year__get"></a>

## GET Get All Year Records

GET /api/records/{year}

### 请求参数

| 名称 | 位置 | 类型    | 必选 | 中文名 | 说明 |
| ---- | ---- | ------- | ---- | ------ | ---- |
| year | path | integer | 是   | Year   | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_all_students_yearly_records_api_records__year__delete"></a>

## DELETE Delete All Students Yearly Records

DELETE /api/records/{year}

### 请求参数

| 名称 | 位置 | 类型    | 必选 | 中文名 | 说明 |
| ---- | ---- | ------- | ---- | ------ | ---- |
| year | path | integer | 是   | Year   | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_student_year_records_api_records__year___student_id__get"></a>

## GET Get Student Year Records

GET /api/records/{year}/{student_id}

### 请求参数

| 名称       | 位置 | 类型    | 必选 | 中文名     | 说明 |
| ---------- | ---- | ------- | ---- | ---------- | ---- |
| year       | path | integer | 是   | Year       | none |
| student_id | path | integer | 是   | Student Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIddelete_yearly_records_api_records__year___student_id__delete"></a>

## DELETE Delete Yearly Records

DELETE /api/records/{year}/{student_id}

### 请求参数

| 名称       | 位置 | 类型    | 必选 | 中文名     | 说明 |
| ---------- | ---- | ------- | ---- | ---------- | ---- |
| year       | path | integer | 是   | Year       | none |
| student_id | path | integer | 是   | Student Id | none |

> 返回示例

> 200 Response

```json
null
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdget_study_time_by_knowledge_api_study_time_get"></a>

## GET Get Study Time By Knowledge

GET /api/study_time

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
{
  "study_time": 0,
  "knowledge_id": "string"
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [StudyTimeOut](#schemastudytimeout)               |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdlist_study_time_all_api_study_time_all_get"></a>

## GET List Study Time All

GET /api/study_time/all

> 返回示例

> 200 Response

```json
[
  {
    "study_time": 0,
    "knowledge_id": "string"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Study Time All Api Study Time All Get_

| 名称                                                | 类型                                  | 必选  | 约束 | 中文名                                              | 说明 |
| --------------------------------------------------- | ------------------------------------- | ----- | ---- | --------------------------------------------------- | ---- |
| Response List Study Time All Api Study Time All Get | [[StudyTimeOut](#schemastudytimeout)] | false | none | Response List Study Time All Api Study Time All Get | none |
| » StudyTimeOut                                      | [StudyTimeOut](#schemastudytimeout)   | false | none | StudyTimeOut                                        | none |
| »» study_time                                       | number                                | true  | none | Study Time                                          | none |
| »» knowledge_id                                     | string                                | true  | none | Knowledge Id                                        | none |

<a id="opIdget_study_time_list_by_knowledge_api_study_time_list_get"></a>

## GET Get Study Time List By Knowledge

GET /api/study_time/list

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "study_time": 0,
    "student_id": 0,
    "student_name": "string"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **200**

_Response Get Study Time List By Knowledge Api Study Time List Get_

| 名称                                                              | 类型                                          | 必选  | 约束 | 中文名                                                            | 说明 |
| ----------------------------------------------------------------- | --------------------------------------------- | ----- | ---- | ----------------------------------------------------------------- | ---- |
| Response Get Study Time List By Knowledge Api Study Time List Get | [[StudyTimeListOut](#schemastudytimelistout)] | false | none | Response Get Study Time List By Knowledge Api Study Time List Get | none |
| » StudyTimeListOut                                                | [StudyTimeListOut](#schemastudytimelistout)   | false | none | StudyTimeListOut                                                  | none |
| »» knowledge_id                                                   | string                                        | true  | none | Knowledge Id                                                      | none |
| »» study_time                                                     | number                                        | true  | none | Study Time                                                        | none |
| »» student_id                                                     | integer                                       | true  | none | Student Id                                                        | none |
| »» student_name                                                   | string                                        | true  | none | Student Name                                                      | none |

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdlist_study_time_list_all_api_study_time_list_all_get"></a>

## GET List Study Time List All

GET /api/study_time/list/all

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "study_time": 0,
    "student_id": 0,
    "student_name": "string"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Study Time List All Api Study Time List All Get_

| 名称                                                          | 类型                                          | 必选  | 约束 | 中文名                                                        | 说明 |
| ------------------------------------------------------------- | --------------------------------------------- | ----- | ---- | ------------------------------------------------------------- | ---- |
| Response List Study Time List All Api Study Time List All Get | [[StudyTimeListOut](#schemastudytimelistout)] | false | none | Response List Study Time List All Api Study Time List All Get | none |
| » StudyTimeListOut                                            | [StudyTimeListOut](#schemastudytimelistout)   | false | none | StudyTimeListOut                                              | none |
| »» knowledge_id                                               | string                                        | true  | none | Knowledge Id                                                  | none |
| »» study_time                                                 | number                                        | true  | none | Study Time                                                    | none |
| »» student_id                                                 | integer                                       | true  | none | Student Id                                                    | none |
| »» student_name                                               | string                                        | true  | none | Student Name                                                  | none |

<a id="opIdget_average_study_time_by_knowledge_api_study_time_average_get"></a>

## GET Get Average Study Time By Knowledge

GET /api/study_time/average

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
{
  "knowledge_id": "string",
  "average_study_time": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [AverageStudyTimeOut](#schemaaveragestudytimeout) |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdlist_average_study_time_all_api_study_time_average_all_get"></a>

## GET List Average Study Time All

GET /api/study_time/average/all

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "average_study_time": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Average Study Time All Api Study Time Average All Get_

| 名称                                                                | 类型                                                | 必选  | 约束 | 中文名                                                              | 说明 |
| ------------------------------------------------------------------- | --------------------------------------------------- | ----- | ---- | ------------------------------------------------------------------- | ---- |
| Response List Average Study Time All Api Study Time Average All Get | [[AverageStudyTimeOut](#schemaaveragestudytimeout)] | false | none | Response List Average Study Time All Api Study Time Average All Get | none |
| » AverageStudyTimeOut                                               | [AverageStudyTimeOut](#schemaaveragestudytimeout)   | false | none | AverageStudyTimeOut                                                 | none |
| »» knowledge_id                                                     | string                                              | true  | none | Knowledge Id                                                        | none |
| »» average_study_time                                               | number                                              | true  | none | Average Study Time                                                  | none |

# 学习进度

<a id="opIdget_progress_by_knowledge_api_progress_get"></a>

## GET Get Progress By Knowledge

GET /api/progress

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
{
  "knowledge_id": "string",
  "progress": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [ProgressOut](#schemaprogressout)                 |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdlist_progress_all_api_progress_all_get"></a>

## GET List Progress All

GET /api/progress/all

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "progress": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Progress All Api Progress All Get_

| 名称                                            | 类型                                | 必选  | 约束 | 中文名                                          | 说明 |
| ----------------------------------------------- | ----------------------------------- | ----- | ---- | ----------------------------------------------- | ---- |
| Response List Progress All Api Progress All Get | [[ProgressOut](#schemaprogressout)] | false | none | Response List Progress All Api Progress All Get | none |
| » ProgressOut                                   | [ProgressOut](#schemaprogressout)   | false | none | ProgressOut                                     | none |
| »» knowledge_id                                 | string                              | true  | none | Knowledge Id                                    | none |
| »» progress                                     | number                              | true  | none | Progress                                        | none |

<a id="opIdget_average_progress_by_knowledge_api_progress_average_get"></a>

## GET Get Average Progress By Knowledge

GET /api/progress/average

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
{
  "knowledge_id": "string",
  "average_progress": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [AverageProgressOut](#schemaaverageprogressout)   |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdlist_average_progress_all_api_progress_average_all_get"></a>

## GET List Average Progress All

GET /api/progress/average/all

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "average_progress": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Average Progress All Api Progress Average All Get_

| 名称                                                            | 类型                                              | 必选  | 约束 | 中文名                                                          | 说明 |
| --------------------------------------------------------------- | ------------------------------------------------- | ----- | ---- | --------------------------------------------------------------- | ---- |
| Response List Average Progress All Api Progress Average All Get | [[AverageProgressOut](#schemaaverageprogressout)] | false | none | Response List Average Progress All Api Progress Average All Get | none |
| » AverageProgressOut                                            | [AverageProgressOut](#schemaaverageprogressout)   | false | none | AverageProgressOut                                              | none |
| »» knowledge_id                                                 | string                                            | true  | none | Knowledge Id                                                    | none |
| »» average_progress                                             | number                                            | true  | none | Average Progress                                                | none |

<a id="opIdget_progress_list_by_knowledge_api_progress_list_get"></a>

## GET Get Progress List By Knowledge

GET /api/progress/list

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "student_id": 0,
    "student_name": "string",
    "progress": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **200**

_Response Get Progress List By Knowledge Api Progress List Get_

| 名称                                                          | 类型                                        | 必选  | 约束 | 中文名                                                        | 说明 |
| ------------------------------------------------------------- | ------------------------------------------- | ----- | ---- | ------------------------------------------------------------- | ---- |
| Response Get Progress List By Knowledge Api Progress List Get | [[ProgressListOut](#schemaprogresslistout)] | false | none | Response Get Progress List By Knowledge Api Progress List Get | none |
| » ProgressListOut                                             | [ProgressListOut](#schemaprogresslistout)   | false | none | ProgressListOut                                               | none |
| »» knowledge_id                                               | string                                      | true  | none | Knowledge Id                                                  | none |
| »» student_id                                                 | integer                                     | true  | none | Student Id                                                    | none |
| »» student_name                                               | string                                      | true  | none | Student Name                                                  | none |
| »» progress                                                   | number                                      | true  | none | Progress                                                      | none |

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdlist_progress_list_all_api_progress_list_all_get"></a>

## GET List Progress List All

GET /api/progress/list/all

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "student_id": 0,
    "student_name": "string",
    "progress": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Progress List All Api Progress List All Get_

| 名称                                                      | 类型                                        | 必选  | 约束 | 中文名                                                    | 说明 |
| --------------------------------------------------------- | ------------------------------------------- | ----- | ---- | --------------------------------------------------------- | ---- |
| Response List Progress List All Api Progress List All Get | [[ProgressListOut](#schemaprogresslistout)] | false | none | Response List Progress List All Api Progress List All Get | none |
| » ProgressListOut                                         | [ProgressListOut](#schemaprogresslistout)   | false | none | ProgressListOut                                           | none |
| »» knowledge_id                                           | string                                      | true  | none | Knowledge Id                                              | none |
| »» student_id                                             | integer                                     | true  | none | Student Id                                                | none |
| »» student_name                                           | string                                      | true  | none | Student Name                                              | none |
| »» progress                                               | number                                      | true  | none | Progress                                                  | none |

# 知识掌握度

<a id="opIdget_mastery_list_by_knowledge_api_mastery_list_get"></a>

## GET Get Mastery List By Knowledge

GET /api/mastery/list

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "student_id": 0,
    "student_name": "string",
    "mastery": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | Inline                                            |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

### 返回数据结构

状态码 **200**

_Response Get Mastery List By Knowledge Api Mastery List Get_

| 名称                                                        | 类型                                      | 必选  | 约束 | 中文名                                                      | 说明 |
| ----------------------------------------------------------- | ----------------------------------------- | ----- | ---- | ----------------------------------------------------------- | ---- |
| Response Get Mastery List By Knowledge Api Mastery List Get | [[MasteryListOut](#schemamasterylistout)] | false | none | Response Get Mastery List By Knowledge Api Mastery List Get | none |
| » MasteryListOut                                            | [MasteryListOut](#schemamasterylistout)   | false | none | MasteryListOut                                              | none |
| »» knowledge_id                                             | string                                    | true  | none | Knowledge Id                                                | none |
| »» student_id                                               | integer                                   | true  | none | Student Id                                                  | none |
| »» student_name                                             | string                                    | true  | none | Student Name                                                | none |
| »» mastery                                                  | number                                    | true  | none | Mastery                                                     | none |

状态码 **422**

_HTTPValidationError_

| 名称               | 类型                                        | 必选  | 约束 | 中文名          | 说明 |
| ------------------ | ------------------------------------------- | ----- | ---- | --------------- | ---- |
| » detail           | [[ValidationError](#schemavalidationerror)] | false | none | Detail          | none |
| »» ValidationError | [ValidationError](#schemavalidationerror)   | false | none | ValidationError | none |
| »»» loc            | [anyOf]                                     | true  | none | Location        | none |

_anyOf_

| 名称             | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------ | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | string | false | none |        | none |

_or_

| 名称             | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ---------------- | ------- | ----- | ---- | ------ | ---- |
| »»»» _anonymous_ | integer | false | none |        | none |

_continued_

| 名称     | 类型   | 必选 | 约束 | 中文名     | 说明 |
| -------- | ------ | ---- | ---- | ---------- | ---- |
| »»» msg  | string | true | none | Message    | none |
| »»» type | string | true | none | Error Type | none |

<a id="opIdlist_mastery_list_all_api_mastery_list_all_get"></a>

## GET List Mastery List All

GET /api/mastery/list/all

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "student_id": 0,
    "student_name": "string",
    "mastery": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Mastery List All Api Mastery List All Get_

| 名称                                                    | 类型                                      | 必选  | 约束 | 中文名                                                  | 说明 |
| ------------------------------------------------------- | ----------------------------------------- | ----- | ---- | ------------------------------------------------------- | ---- |
| Response List Mastery List All Api Mastery List All Get | [[MasteryListOut](#schemamasterylistout)] | false | none | Response List Mastery List All Api Mastery List All Get | none |
| » MasteryListOut                                        | [MasteryListOut](#schemamasterylistout)   | false | none | MasteryListOut                                          | none |
| »» knowledge_id                                         | string                                    | true  | none | Knowledge Id                                            | none |
| »» student_id                                           | integer                                   | true  | none | Student Id                                              | none |
| »» student_name                                         | string                                    | true  | none | Student Name                                            | none |
| »» mastery                                              | number                                    | true  | none | Mastery                                                 | none |

<a id="opIdget_average_mastery_by_knowledge_api_mastery_average_get"></a>

## GET Get Average Mastery By Knowledge

GET /api/mastery/average

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
{
  "knowledge_id": "string",
  "average_mastery": 0
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [AverageMasteryOut](#schemaaveragemasteryout)     |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdlist_average_mastery_all_api_mastery_average_all_get"></a>

## GET List Average Mastery All

GET /api/mastery/average/all

> 返回示例

> 200 Response

```json
[
  {
    "knowledge_id": "string",
    "average_mastery": 0
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Average Mastery All Api Mastery Average All Get_

| 名称                                                          | 类型                                            | 必选  | 约束 | 中文名                                                        | 说明 |
| ------------------------------------------------------------- | ----------------------------------------------- | ----- | ---- | ------------------------------------------------------------- | ---- |
| Response List Average Mastery All Api Mastery Average All Get | [[AverageMasteryOut](#schemaaveragemasteryout)] | false | none | Response List Average Mastery All Api Mastery Average All Get | none |
| » AverageMasteryOut                                           | [AverageMasteryOut](#schemaaveragemasteryout)   | false | none | AverageMasteryOut                                             | none |
| »» knowledge_id                                               | string                                          | true  | none | Knowledge Id                                                  | none |
| »» average_mastery                                            | number                                          | true  | none | Average Mastery                                               | none |

<a id="opIdget_mastery_by_knowledge_api_mastery_get"></a>

## GET Get Mastery By Knowledge

GET /api/mastery

### 请求参数

| 名称         | 位置  | 类型   | 必选 | 中文名       | 说明 |
| ------------ | ----- | ------ | ---- | ------------ | ---- |
| knowledge_id | query | string | 否   | Knowledge Id | none |

> 返回示例

> 200 Response

```json
{
  "mastery": 0,
  "knowledge_id": "string"
}
```

### 返回结果

| 状态码 | 状态码含义                                                               | 说明                | 数据模型                                          |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [MasteryOut](#schemamasteryout)                   |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<a id="opIdlist_mastery_all_api_mastery_all_get"></a>

## GET List Mastery All

GET /api/mastery/all

> 返回示例

> 200 Response

```json
[
  {
    "mastery": 0,
    "knowledge_id": "string"
  }
]
```

### 返回结果

| 状态码 | 状态码含义                                              | 说明                | 数据模型 |
| ------ | ------------------------------------------------------- | ------------------- | -------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | Inline   |

### 返回数据结构

状态码 **200**

_Response List Mastery All Api Mastery All Get_

| 名称                                          | 类型                              | 必选  | 约束 | 中文名                                        | 说明 |
| --------------------------------------------- | --------------------------------- | ----- | ---- | --------------------------------------------- | ---- |
| Response List Mastery All Api Mastery All Get | [[MasteryOut](#schemamasteryout)] | false | none | Response List Mastery All Api Mastery All Get | none |
| » MasteryOut                                  | [MasteryOut](#schemamasteryout)   | false | none | MasteryOut                                    | none |
| »» mastery                                    | number                            | true  | none | Mastery                                       | none |
| »» knowledge_id                               | string                            | true  | none | Knowledge Id                                  | none |

# 数据模型

<h2 id="tocS_AnswerItem">AnswerItem</h2>

<a id="schemaansweritem"></a>
<a id="schema_AnswerItem"></a>
<a id="tocSansweritem"></a>
<a id="tocsansweritem"></a>

```json
{
  "question_id": 0,
  "student_answer": "string"
}
```

AnswerItem

### 属性

| 名称           | 类型    | 必选 | 约束 | 中文名         | 说明 |
| -------------- | ------- | ---- | ---- | -------------- | ---- |
| question_id    | integer | true | none | Question Id    | none |
| student_answer | string  | true | none | Student Answer | none |

<h2 id="tocS_AssignedTaskResponse">AssignedTaskResponse</h2>

<a id="schemaassignedtaskresponse"></a>
<a id="schema_AssignedTaskResponse"></a>
<a id="tocSassignedtaskresponse"></a>
<a id="tocsassignedtaskresponse"></a>

```json
{
  "id": 0,
  "task_id": 0,
  "student_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "is_completed": true,
  "task": {
    "title": "string",
    "description": "string",
    "due_date": "2019-08-24T14:15:22Z",
    "id": 0,
    "created_by_id": 0,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z",
    "assigned_count": 0,
    "completed_count": 0
  },
  "submission": {
    "content": "string",
    "file_path": "string",
    "id": 0,
    "task_id": 0,
    "student_id": 0,
    "submitted_at": "2019-08-24T14:15:22Z",
    "score": 0,
    "feedback": "string",
    "graded_at": "2019-08-24T14:15:22Z"
  }
}
```

AssignedTaskResponse

### 属性

| 名称         | 类型                                                    | 必选  | 约束 | 中文名       | 说明 |
| ------------ | ------------------------------------------------------- | ----- | ---- | ------------ | ---- |
| id           | integer                                                 | true  | none | Id           | none |
| task_id      | integer                                                 | true  | none | Task Id      | none |
| student_id   | integer                                                 | true  | none | Student Id   | none |
| created_at   | string(date-time)                                       | true  | none | Created At   | none |
| is_completed | boolean                                                 | true  | none | Is Completed | none |
| task         | [TaskResponse](#schemataskresponse)                     | true  | none |              | none |
| submission   | [TaskSubmissionResponse](#schematasksubmissionresponse) | false | none |              | none |

<h2 id="tocS_AverageMasteryOut">AverageMasteryOut</h2>

<a id="schemaaveragemasteryout"></a>
<a id="schema_AverageMasteryOut"></a>
<a id="tocSaveragemasteryout"></a>
<a id="tocsaveragemasteryout"></a>

```json
{
  "knowledge_id": "string",
  "average_mastery": 0
}
```

AverageMasteryOut

### 属性

| 名称            | 类型   | 必选 | 约束 | 中文名          | 说明 |
| --------------- | ------ | ---- | ---- | --------------- | ---- |
| knowledge_id    | string | true | none | Knowledge Id    | none |
| average_mastery | number | true | none | Average Mastery | none |

<h2 id="tocS_AverageProgressOut">AverageProgressOut</h2>

<a id="schemaaverageprogressout"></a>
<a id="schema_AverageProgressOut"></a>
<a id="tocSaverageprogressout"></a>
<a id="tocsaverageprogressout"></a>

```json
{
  "knowledge_id": "string",
  "average_progress": 0
}
```

AverageProgressOut

### 属性

| 名称             | 类型   | 必选 | 约束 | 中文名           | 说明 |
| ---------------- | ------ | ---- | ---- | ---------------- | ---- |
| knowledge_id     | string | true | none | Knowledge Id     | none |
| average_progress | number | true | none | Average Progress | none |

<h2 id="tocS_AverageStudyTimeOut">AverageStudyTimeOut</h2>

<a id="schemaaveragestudytimeout"></a>
<a id="schema_AverageStudyTimeOut"></a>
<a id="tocSaveragestudytimeout"></a>
<a id="tocsaveragestudytimeout"></a>

```json
{
  "knowledge_id": "string",
  "average_study_time": 0
}
```

AverageStudyTimeOut

### 属性

| 名称               | 类型   | 必选 | 约束 | 中文名             | 说明 |
| ------------------ | ------ | ---- | ---- | ------------------ | ---- |
| knowledge_id       | string | true | none | Knowledge Id       | none |
| average_study_time | number | true | none | Average Study Time | none |

<h2 id="tocS_Body_add_question_api_question_add_post">Body_add_question_api_question_add_post</h2>

<a id="schemabody_add_question_api_question_add_post"></a>
<a id="schema_Body_add_question_api_question_add_post"></a>
<a id="tocSbody_add_question_api_question_add_post"></a>
<a id="tocsbody_add_question_api_question_add_post"></a>

```json
{
  "text": "string",
  "type": "string",
  "options": "string",
  "answer": "string",
  "code_examples": "string",
  "code_language": "python",
  "knowledge_id": "string",
  "difficulty": 0.5
}
```

Body_add_question_api_question_add_post

### 属性

| 名称    | 类型   | 必选  | 约束 | 中文名  | 说明                       |
| ------- | ------ | ----- | ---- | ------- | -------------------------- |
| text    | string | true  | none | Text    | 题目内容                   |
| type    | string | true  | none | Type    | 题目类型(choice/fill/code) |
| options | any    | false | none | Options | 选项(JSON 格式，仅选择题)  |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称          | 类型   | 必选  | 约束 | 中文名        | 说明                                                                   |
| ------------- | ------ | ----- | ---- | ------------- | ---------------------------------------------------------------------- |
| answer        | string | true  | none | Answer        | 正确答案（编程题可填写参考说明）                                       |
| code_examples | any    | false | none | Code Examples | 编程题测试用例(JSON 数组，每项包含 input 和 output 字段，仅编程题必填) |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称          | 类型 | 必选  | 约束 | 中文名        | 说明                                          |
| ------------- | ---- | ----- | ---- | ------------- | --------------------------------------------- |
| code_language | any  | false | none | Code Language | 编程语言类型(python/c/cpp/java，仅编程题有效) |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称         | 类型   | 必选  | 约束 | 中文名       | 说明                      |
| ------------ | ------ | ----- | ---- | ------------ | ------------------------- |
| knowledge_id | string | true  | none | Knowledge Id | 知识点 ID 列表(JSON 格式) |
| difficulty   | any    | false | none | Difficulty   | 难度系数(0-1)             |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | number | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_Body_login_api_auth_login_post">Body_login_api_auth_login_post</h2>

<a id="schemabody_login_api_auth_login_post"></a>
<a id="schema_Body_login_api_auth_login_post"></a>
<a id="tocSbody_login_api_auth_login_post"></a>
<a id="tocsbody_login_api_auth_login_post"></a>

```json
{
  "grant_type": "string",
  "username": "string",
  "password": "string",
  "scope": "",
  "client_id": "string",
  "client_secret": "string"
}
```

Body_login_api_auth_login_post

### 属性

| 名称       | 类型 | 必选  | 约束 | 中文名     | 说明 |
| ---------- | ---- | ----- | ---- | ---------- | ---- |
| grant_type | any  | false | none | Grant Type | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称      | 类型   | 必选  | 约束 | 中文名    | 说明 |
| --------- | ------ | ----- | ---- | --------- | ---- |
| username  | string | true  | none | Username  | none |
| password  | string | true  | none | Password  | none |
| scope     | string | false | none | Scope     | none |
| client_id | any    | false | none | Client Id | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称          | 类型 | 必选  | 约束 | 中文名        | 说明 |
| ------------- | ---- | ----- | ---- | ------------- | ---- |
| client_secret | any  | false | none | Client Secret | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_Body_upload_resource_api_resource_upload_post">Body_upload_resource_api_resource_upload_post</h2>

<a id="schemabody_upload_resource_api_resource_upload_post"></a>
<a id="schema_Body_upload_resource_api_resource_upload_post"></a>
<a id="tocSbody_upload_resource_api_resource_upload_post"></a>
<a id="tocsbody_upload_resource_api_resource_upload_post"></a>

```json
{
  "file": "string",
  "title": "string",
  "type": "string",
  "description": "string",
  "sync_knowledge": false
}
```

Body_upload_resource_api_resource_upload_post

### 属性

| 名称        | 类型           | 必选  | 约束 | 中文名      | 说明                 |
| ----------- | -------------- | ----- | ---- | ----------- | -------------------- |
| file        | string(binary) | true  | none | File        | none                 |
| title       | string         | true  | none | Title       | 文件标题             |
| type        | string         | true  | none | Type        | 文件类型分类         |
| description | any            | false | none | Description | 资源详细描述（可选） |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称           | 类型 | 必选  | 约束 | 中文名         | 说明               |
| -------------- | ---- | ----- | ---- | -------------- | ------------------ |
| sync_knowledge | any  | false | none | Sync Knowledge | 是否同步到知识图谱 |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | boolean | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_ConceptNode">ConceptNode</h2>

<a id="schemaconceptnode"></a>
<a id="schema_ConceptNode"></a>
<a id="tocSconceptnode"></a>
<a id="tocsconceptnode"></a>

```json
{
  "id": "string",
  "category": "Concept",
  "name": "string",
  "description": "string",
  "depth": 0,
  "difficulty": 0,
  "importance": 0
}
```

ConceptNode

### 属性

| 名称        | 类型   | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------ | ----- | ---- | ----------- | ---- |
| id          | string | true  | none | Id          | none |
| category    | any    | true  | none | Category    | none |
| name        | string | true  | none | Name        | none |
| description | any    | false | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称       | 类型    | 必选  | 约束 | 中文名     | 说明 |
| ---------- | ------- | ----- | ---- | ---------- | ---- |
| depth      | integer | true  | none | Depth      | none |
| difficulty | any     | false | none | Difficulty | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | integer | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称       | 类型 | 必选  | 约束 | 中文名     | 说明 |
| ---------- | ---- | ----- | ---- | ---------- | ---- |
| importance | any  | false | none | Importance | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | integer | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_ConversationCreate">ConversationCreate</h2>

<a id="schemaconversationcreate"></a>
<a id="schema_ConversationCreate"></a>
<a id="tocSconversationcreate"></a>
<a id="tocsconversationcreate"></a>

```json
{
  "title": "string"
}
```

ConversationCreate

### 属性

| 名称  | 类型   | 必选 | 约束 | 中文名 | 说明 |
| ----- | ------ | ---- | ---- | ------ | ---- |
| title | string | true | none | Title  | none |

<h2 id="tocS_ConversationOut">ConversationOut</h2>

<a id="schemaconversationout"></a>
<a id="schema_ConversationOut"></a>
<a id="tocSconversationout"></a>
<a id="tocsconversationout"></a>

```json
{
  "id": "string",
  "title": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "messages": []
}
```

ConversationOut

### 属性

| 名称       | 类型                              | 必选  | 约束 | 中文名     | 说明 |
| ---------- | --------------------------------- | ----- | ---- | ---------- | ---- |
| id         | string                            | true  | none | Id         | none |
| title      | string                            | true  | none | Title      | none |
| created_at | string(date-time)                 | true  | none | Created At | none |
| messages   | [[MessageOut](#schemamessageout)] | false | none | Messages   | none |

<h2 id="tocS_ConversationSummary">ConversationSummary</h2>

<a id="schemaconversationsummary"></a>
<a id="schema_ConversationSummary"></a>
<a id="tocSconversationsummary"></a>
<a id="tocsconversationsummary"></a>

```json
{
  "id": "string",
  "title": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

ConversationSummary

### 属性

| 名称       | 类型              | 必选 | 约束 | 中文名     | 说明 |
| ---------- | ----------------- | ---- | ---- | ---------- | ---- |
| id         | string            | true | none | Id         | none |
| title      | string            | true | none | Title      | none |
| created_at | string(date-time) | true | none | Created At | none |

<h2 id="tocS_CourseNode">CourseNode</h2>

<a id="schemacoursenode"></a>
<a id="schema_CourseNode"></a>
<a id="tocScoursenode"></a>
<a id="tocscoursenode"></a>

```json
{
  "id": "string",
  "category": "Course",
  "name": "string",
  "description": "string",
  "depth": 0
}
```

CourseNode

### 属性

| 名称        | 类型   | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------ | ----- | ---- | ----------- | ---- |
| id          | string | true  | none | Id          | none |
| category    | any    | true  | none | Category    | none |
| name        | string | true  | none | Name        | none |
| description | any    | false | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称  | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ----- | ---- | ----- | ---- | ------ | ---- |
| depth | any  | false | none | Depth  | none |

<h2 id="tocS_GraphData">GraphData</h2>

<a id="schemagraphdata"></a>
<a id="schema_GraphData"></a>
<a id="tocSgraphdata"></a>
<a id="tocsgraphdata"></a>

```json
{
  "nodes": [
    {
      "id": "string",
      "category": "Course",
      "name": "string",
      "description": "string",
      "depth": 0
    }
  ],
  "edges": [
    {
      "source": "string",
      "target": "string",
      "relation": "string"
    }
  ]
}
```

GraphData

### 属性

| 名称  | 类型    | 必选 | 约束 | 中文名 | 说明 |
| ----- | ------- | ---- | ---- | ------ | ---- |
| nodes | [anyOf] | true | none | Nodes  | none |

anyOf

| 名称          | 类型                            | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------------------------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [CourseNode](#schemacoursenode) | false | none |        | none |

or

| 名称          | 类型                              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | --------------------------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [ConceptNode](#schemaconceptnode) | false | none |        | none |

or

| 名称          | 类型                                | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------------------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [ResourceNode](#schemaresourcenode) | false | none |        | none |

continued

| 名称  | 类型                            | 必选 | 约束 | 中文名 | 说明 |
| ----- | ------------------------------- | ---- | ---- | ------ | ---- |
| edges | [[GraphEdge](#schemagraphedge)] | true | none | Edges  | none |

<h2 id="tocS_GraphDataOut">GraphDataOut</h2>

<a id="schemagraphdataout"></a>
<a id="schema_GraphDataOut"></a>
<a id="tocSgraphdataout"></a>
<a id="tocsgraphdataout"></a>

```json
{
  "nodes": [
    {
      "id": "string",
      "category": "Course",
      "name": "string",
      "description": "string",
      "depth": 0
    }
  ],
  "edges": [
    {
      "source": "string",
      "target": "string",
      "relation": "string"
    }
  ],
  "resources": [
    {
      "id": "string",
      "name": "string"
    }
  ]
}
```

GraphDataOut

### 属性

| 名称  | 类型    | 必选 | 约束 | 中文名 | 说明 |
| ----- | ------- | ---- | ---- | ------ | ---- |
| nodes | [anyOf] | true | none | Nodes  | none |

anyOf

| 名称          | 类型                            | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------------------------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [CourseNode](#schemacoursenode) | false | none |        | none |

or

| 名称          | 类型                              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | --------------------------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [ConceptNode](#schemaconceptnode) | false | none |        | none |

or

| 名称          | 类型                                | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------------------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [ResourceNode](#schemaresourcenode) | false | none |        | none |

continued

| 名称      | 类型                                              | 必选 | 约束 | 中文名    | 说明 |
| --------- | ------------------------------------------------- | ---- | ---- | --------- | ---- |
| edges     | [[GraphEdge](#schemagraphedge)]                   | true | none | Edges     | none |
| resources | [[ResourceSimpleInfo](#schemaresourcesimpleinfo)] | true | none | Resources | none |

<h2 id="tocS_GraphEdge">GraphEdge</h2>

<a id="schemagraphedge"></a>
<a id="schema_GraphEdge"></a>
<a id="tocSgraphedge"></a>
<a id="tocsgraphedge"></a>

```json
{
  "source": "string",
  "target": "string",
  "relation": "string"
}
```

GraphEdge

### 属性

| 名称     | 类型   | 必选 | 约束 | 中文名   | 说明 |
| -------- | ------ | ---- | ---- | -------- | ---- |
| source   | string | true | none | Source   | none |
| target   | string | true | none | Target   | none |
| relation | string | true | none | Relation | none |

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>

<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

HTTPValidationError

### 属性

| 名称   | 类型                                        | 必选  | 约束 | 中文名 | 说明 |
| ------ | ------------------------------------------- | ----- | ---- | ------ | ---- |
| detail | [[ValidationError](#schemavalidationerror)] | false | none | Detail | none |

<h2 id="tocS_KnowledgeInfo">KnowledgeInfo</h2>

<a id="schemaknowledgeinfo"></a>
<a id="schema_KnowledgeInfo"></a>
<a id="tocSknowledgeinfo"></a>
<a id="tocsknowledgeinfo"></a>

```json
{
  "id": "string",
  "name": "string"
}
```

KnowledgeInfo

### 属性

| 名称 | 类型   | 必选 | 约束 | 中文名 | 说明 |
| ---- | ------ | ---- | ---- | ------ | ---- |
| id   | string | true | none | Id     | none |
| name | string | true | none | Name   | none |

<h2 id="tocS_LearningRecordCreate">LearningRecordCreate</h2>

<a id="schemalearningrecordcreate"></a>
<a id="schema_LearningRecordCreate"></a>
<a id="tocSlearningrecordcreate"></a>
<a id="tocslearningrecordcreate"></a>

```json
{
  "student_id": 0,
  "resource_id": "string",
  "status": 0,
  "total_time": 0,
  "page_times": [0]
}
```

LearningRecordCreate

### 属性

| 名称        | 类型    | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------- | ----- | ---- | ----------- | ---- |
| student_id  | integer | true  | none | Student Id  | none |
| resource_id | string  | true  | none | Resource Id | none |
| status      | integer | true  | none | Status      | none |
| total_time  | integer | true  | none | Total Time  | none |
| page_times  | any     | false | none | Page Times  | none |

anyOf

| 名称          | 类型      | 必选  | 约束 | 中文名 | 说明 |
| ------------- | --------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [integer] | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_MasteryListOut">MasteryListOut</h2>

<a id="schemamasterylistout"></a>
<a id="schema_MasteryListOut"></a>
<a id="tocSmasterylistout"></a>
<a id="tocsmasterylistout"></a>

```json
{
  "knowledge_id": "string",
  "student_id": 0,
  "student_name": "string",
  "mastery": 0
}
```

MasteryListOut

### 属性

| 名称         | 类型    | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ------- | ---- | ---- | ------------ | ---- |
| knowledge_id | string  | true | none | Knowledge Id | none |
| student_id   | integer | true | none | Student Id   | none |
| student_name | string  | true | none | Student Name | none |
| mastery      | number  | true | none | Mastery      | none |

<h2 id="tocS_MasteryOut">MasteryOut</h2>

<a id="schemamasteryout"></a>
<a id="schema_MasteryOut"></a>
<a id="tocSmasteryout"></a>
<a id="tocsmasteryout"></a>

```json
{
  "mastery": 0,
  "knowledge_id": "string"
}
```

MasteryOut

### 属性

| 名称         | 类型   | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ------ | ---- | ---- | ------------ | ---- |
| mastery      | number | true | none | Mastery      | none |
| knowledge_id | string | true | none | Knowledge Id | none |

<h2 id="tocS_MessageIn">MessageIn</h2>

<a id="schemamessagein"></a>
<a id="schema_MessageIn"></a>
<a id="tocSmessagein"></a>
<a id="tocsmessagein"></a>

```json
{
  "user_input": "string"
}
```

MessageIn

### 属性

| 名称       | 类型   | 必选 | 约束 | 中文名     | 说明 |
| ---------- | ------ | ---- | ---- | ---------- | ---- |
| user_input | string | true | none | User Input | none |

<h2 id="tocS_MessageOut">MessageOut</h2>

<a id="schemamessageout"></a>
<a id="schema_MessageOut"></a>
<a id="tocSmessageout"></a>
<a id="tocsmessageout"></a>

```json
{
  "id": 0,
  "role": "string",
  "content": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "rag_docs": [{}]
}
```

MessageOut

### 属性

| 名称       | 类型              | 必选  | 约束 | 中文名     | 说明 |
| ---------- | ----------------- | ----- | ---- | ---------- | ---- |
| id         | integer           | true  | none | Id         | none |
| role       | string            | true  | none | Role       | none |
| content    | string            | true  | none | Content    | none |
| created_at | string(date-time) | true  | none | Created At | none |
| rag_docs   | any               | false | none | Rag Docs   | none |

anyOf

| 名称          | 类型     | 必选  | 约束 | 中文名 | 说明 |
| ------------- | -------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [object] | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_NodeDetail">NodeDetail</h2>

<a id="schemanodedetail"></a>
<a id="schema_NodeDetail"></a>
<a id="tocSnodedetail"></a>
<a id="tocsnodedetail"></a>

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "total_time": 0,
  "average_time": 0,
  "resources": [
    {
      "id": "string",
      "name": "string",
      "type": "string",
      "download_url": "string",
      "is_child": false
    }
  ],
  "prerequisites": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "successors": [
    {
      "id": "string",
      "name": "string"
    }
  ]
}
```

NodeDetail

### 属性

| 名称        | 类型   | 必选 | 约束 | 中文名      | 说明 |
| ----------- | ------ | ---- | ---- | ----------- | ---- |
| id          | string | true | none | Id          | none |
| name        | string | true | none | Name        | none |
| description | any    | true | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称          | 类型                                  | 必选 | 约束 | 中文名        | 说明 |
| ------------- | ------------------------------------- | ---- | ---- | ------------- | ---- |
| total_time    | integer                               | true | none | Total Time    | none |
| average_time  | integer                               | true | none | Average Time  | none |
| resources     | [[ResourceInfo](#schemaresourceinfo)] | true | none | Resources     | none |
| prerequisites | [[NodeRef](#schemanoderef)]           | true | none | Prerequisites | none |
| successors    | [[NodeRef](#schemanoderef)]           | true | none | Successors    | none |

<h2 id="tocS_NodeRef">NodeRef</h2>

<a id="schemanoderef"></a>
<a id="schema_NodeRef"></a>
<a id="tocSnoderef"></a>
<a id="tocsnoderef"></a>

```json
{
  "id": "string",
  "name": "string"
}
```

NodeRef

### 属性

| 名称 | 类型   | 必选 | 约束 | 中文名 | 说明 |
| ---- | ------ | ---- | ---- | ------ | ---- |
| id   | string | true | none | Id     | none |
| name | string | true | none | Name   | none |

<h2 id="tocS_PermissionResponse">PermissionResponse</h2>

<a id="schemapermissionresponse"></a>
<a id="schema_PermissionResponse"></a>
<a id="tocSpermissionresponse"></a>
<a id="tocspermissionresponse"></a>

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "resource": "string"
}
```

PermissionResponse

### 属性

| 名称        | 类型    | 必选 | 约束 | 中文名      | 说明 |
| ----------- | ------- | ---- | ---- | ----------- | ---- |
| id          | integer | true | none | Id          | none |
| name        | string  | true | none | Name        | none |
| description | any     | true | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称     | 类型 | 必选 | 约束 | 中文名   | 说明 |
| -------- | ---- | ---- | ---- | -------- | ---- |
| resource | any  | true | none | Resource | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_ProgressListOut">ProgressListOut</h2>

<a id="schemaprogresslistout"></a>
<a id="schema_ProgressListOut"></a>
<a id="tocSprogresslistout"></a>
<a id="tocsprogresslistout"></a>

```json
{
  "knowledge_id": "string",
  "student_id": 0,
  "student_name": "string",
  "progress": 0
}
```

ProgressListOut

### 属性

| 名称         | 类型    | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ------- | ---- | ---- | ------------ | ---- |
| knowledge_id | string  | true | none | Knowledge Id | none |
| student_id   | integer | true | none | Student Id   | none |
| student_name | string  | true | none | Student Name | none |
| progress     | number  | true | none | Progress     | none |

<h2 id="tocS_ProgressOut">ProgressOut</h2>

<a id="schemaprogressout"></a>
<a id="schema_ProgressOut"></a>
<a id="tocSprogressout"></a>
<a id="tocsprogressout"></a>

```json
{
  "knowledge_id": "string",
  "progress": 0
}
```

ProgressOut

### 属性

| 名称         | 类型   | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ------ | ---- | ---- | ------------ | ---- |
| knowledge_id | string | true | none | Knowledge Id | none |
| progress     | number | true | none | Progress     | none |

<h2 id="tocS_ReplyBase">ReplyBase</h2>

<a id="schemareplybase"></a>
<a id="schema_ReplyBase"></a>
<a id="tocSreplybase"></a>
<a id="tocsreplybase"></a>

```json
{
  "content": "string"
}
```

ReplyBase

### 属性

| 名称    | 类型   | 必选 | 约束 | 中文名  | 说明 |
| ------- | ------ | ---- | ---- | ------- | ---- |
| content | string | true | none | Content | none |

<h2 id="tocS_ReplyCreate">ReplyCreate</h2>

<a id="schemareplycreate"></a>
<a id="schema_ReplyCreate"></a>
<a id="tocSreplycreate"></a>
<a id="tocsreplycreate"></a>

```json
{
  "content": "string"
}
```

ReplyCreate

### 属性

| 名称    | 类型   | 必选 | 约束 | 中文名  | 说明 |
| ------- | ------ | ---- | ---- | ------- | ---- |
| content | string | true | none | Content | none |

<h2 id="tocS_ReplyResponse">ReplyResponse</h2>

<a id="schemareplyresponse"></a>
<a id="schema_ReplyResponse"></a>
<a id="tocSreplyresponse"></a>
<a id="tocsreplyresponse"></a>

```json
{
  "content": "string",
  "id": 0,
  "topic_id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "created_by_name": "string"
}
```

ReplyResponse

### 属性

| 名称          | 类型              | 必选  | 约束 | 中文名        | 说明 |
| ------------- | ----------------- | ----- | ---- | ------------- | ---- |
| content       | string            | true  | none | Content       | none |
| id            | integer           | true  | none | Id            | none |
| topic_id      | integer           | true  | none | Topic Id      | none |
| created_by_id | integer           | true  | none | Created By Id | none |
| created_at    | string(date-time) | true  | none | Created At    | none |
| updated_at    | any               | false | none | Updated At    | none |

anyOf

| 名称          | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | string(date-time) | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称            | 类型 | 必选  | 约束 | 中文名          | 说明 |
| --------------- | ---- | ----- | ---- | --------------- | ---- |
| created_by_name | any  | false | none | Created By Name | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_ResourceInfo">ResourceInfo</h2>

<a id="schemaresourceinfo"></a>
<a id="schema_ResourceInfo"></a>
<a id="tocSresourceinfo"></a>
<a id="tocsresourceinfo"></a>

```json
{
  "id": "string",
  "name": "string",
  "type": "string",
  "download_url": "string",
  "is_child": false
}
```

ResourceInfo

### 属性

| 名称         | 类型    | 必选  | 约束 | 中文名       | 说明 |
| ------------ | ------- | ----- | ---- | ------------ | ---- |
| id           | string  | true  | none | Id           | none |
| name         | string  | true  | none | Name         | none |
| type         | string  | true  | none | Type         | none |
| download_url | string  | true  | none | Download Url | none |
| is_child     | boolean | false | none | Is Child     | none |

<h2 id="tocS_ResourceNode">ResourceNode</h2>

<a id="schemaresourcenode"></a>
<a id="schema_ResourceNode"></a>
<a id="tocSresourcenode"></a>
<a id="tocsresourcenode"></a>

```json
{
  "id": "string",
  "category": "Resource",
  "name": "string",
  "download_url": "string",
  "type": "string"
}
```

ResourceNode

### 属性

| 名称         | 类型   | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ------ | ---- | ---- | ------------ | ---- |
| id           | string | true | none | Id           | none |
| category     | any    | true | none | Category     | none |
| name         | string | true | none | Name         | none |
| download_url | string | true | none | Download Url | none |
| type         | string | true | none | Type         | none |

<h2 id="tocS_ResourceSimpleInfo">ResourceSimpleInfo</h2>

<a id="schemaresourcesimpleinfo"></a>
<a id="schema_ResourceSimpleInfo"></a>
<a id="tocSresourcesimpleinfo"></a>
<a id="tocsresourcesimpleinfo"></a>

```json
{
  "id": "string",
  "name": "string"
}
```

ResourceSimpleInfo

### 属性

| 名称 | 类型   | 必选 | 约束 | 中文名 | 说明 |
| ---- | ------ | ---- | ---- | ------ | ---- |
| id   | string | true | none | Id     | none |
| name | string | true | none | Name   | none |

<h2 id="tocS_RoleCreate">RoleCreate</h2>

<a id="schemarolecreate"></a>
<a id="schema_RoleCreate"></a>
<a id="tocSrolecreate"></a>
<a id="tocsrolecreate"></a>

```json
{
  "name": "string",
  "description": "string",
  "permission_ids": []
}
```

RoleCreate

### 属性

| 名称        | 类型   | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------ | ----- | ---- | ----------- | ---- |
| name        | string | true  | none | Name        | none |
| description | any    | false | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称           | 类型      | 必选  | 约束 | 中文名         | 说明 |
| -------------- | --------- | ----- | ---- | -------------- | ---- |
| permission_ids | [integer] | false | none | Permission Ids | none |

<h2 id="tocS_RoleResponse">RoleResponse</h2>

<a id="schemaroleresponse"></a>
<a id="schema_RoleResponse"></a>
<a id="tocSroleresponse"></a>
<a id="tocsroleresponse"></a>

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "permissions": []
}
```

RoleResponse

### 属性

| 名称        | 类型    | 必选 | 约束 | 中文名      | 说明 |
| ----------- | ------- | ---- | ---- | ----------- | ---- |
| id          | integer | true | none | Id          | none |
| name        | string  | true | none | Name        | none |
| description | any     | true | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称        | 类型                                              | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------------------------------------------------- | ----- | ---- | ----------- | ---- |
| permissions | [[PermissionResponse](#schemapermissionresponse)] | false | none | Permissions | none |

<h2 id="tocS_RoleUpdate">RoleUpdate</h2>

<a id="schemaroleupdate"></a>
<a id="schema_RoleUpdate"></a>
<a id="tocSroleupdate"></a>
<a id="tocsroleupdate"></a>

```json
{
  "name": "string",
  "description": "string",
  "permission_ids": [0]
}
```

RoleUpdate

### 属性

| 名称 | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ---- | ---- | ----- | ---- | ------ | ---- |
| name | any  | false | none | Name   | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称        | 类型 | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ---- | ----- | ---- | ----------- | ---- |
| description | any  | false | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称           | 类型 | 必选  | 约束 | 中文名         | 说明 |
| -------------- | ---- | ----- | ---- | -------------- | ---- |
| permission_ids | any  | false | none | Permission Ids | none |

anyOf

| 名称          | 类型      | 必选  | 约束 | 中文名 | 说明 |
| ------------- | --------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | [integer] | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_StudyTimeListOut">StudyTimeListOut</h2>

<a id="schemastudytimelistout"></a>
<a id="schema_StudyTimeListOut"></a>
<a id="tocSstudytimelistout"></a>
<a id="tocsstudytimelistout"></a>

```json
{
  "knowledge_id": "string",
  "study_time": 0,
  "student_id": 0,
  "student_name": "string"
}
```

StudyTimeListOut

### 属性

| 名称         | 类型    | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ------- | ---- | ---- | ------------ | ---- |
| knowledge_id | string  | true | none | Knowledge Id | none |
| study_time   | number  | true | none | Study Time   | none |
| student_id   | integer | true | none | Student Id   | none |
| student_name | string  | true | none | Student Name | none |

<h2 id="tocS_StudyTimeOut">StudyTimeOut</h2>

<a id="schemastudytimeout"></a>
<a id="schema_StudyTimeOut"></a>
<a id="tocSstudytimeout"></a>
<a id="tocsstudytimeout"></a>

```json
{
  "study_time": 0,
  "knowledge_id": "string"
}
```

StudyTimeOut

### 属性

| 名称         | 类型   | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ------ | ---- | ---- | ------------ | ---- |
| study_time   | number | true | none | Study Time   | none |
| knowledge_id | string | true | none | Knowledge Id | none |

<h2 id="tocS_SubmitRequest">SubmitRequest</h2>

<a id="schemasubmitrequest"></a>
<a id="schema_SubmitRequest"></a>
<a id="tocSsubmitrequest"></a>
<a id="tocssubmitrequest"></a>

```json
{
  "answers": [
    {
      "question_id": 0,
      "student_answer": "string"
    }
  ],
  "time_spent": 0,
  "knowledge_id": "string"
}
```

SubmitRequest

### 属性

| 名称         | 类型                              | 必选  | 约束 | 中文名       | 说明 |
| ------------ | --------------------------------- | ----- | ---- | ------------ | ---- |
| answers      | [[AnswerItem](#schemaansweritem)] | true  | none | Answers      | none |
| time_spent   | integer                           | true  | none | Time Spent   | none |
| knowledge_id | any                               | false | none | Knowledge Id | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_TaskCreate">TaskCreate</h2>

<a id="schemataskcreate"></a>
<a id="schema_TaskCreate"></a>
<a id="tocStaskcreate"></a>
<a id="tocstaskcreate"></a>

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z",
  "student_ids": [0]
}
```

TaskCreate

### 属性

| 名称        | 类型   | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------ | ----- | ---- | ----------- | ---- |
| title       | string | true  | none | Title       | none |
| description | any    | false | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称     | 类型 | 必选  | 约束 | 中文名   | 说明 |
| -------- | ---- | ----- | ---- | -------- | ---- |
| due_date | any  | false | none | Due Date | none |

anyOf

| 名称          | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | string(date-time) | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称        | 类型      | 必选 | 约束 | 中文名      | 说明 |
| ----------- | --------- | ---- | ---- | ----------- | ---- |
| student_ids | [integer] | true | none | Student Ids | none |

<h2 id="tocS_TaskResponse">TaskResponse</h2>

<a id="schemataskresponse"></a>
<a id="schema_TaskResponse"></a>
<a id="tocStaskresponse"></a>
<a id="tocstaskresponse"></a>

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z",
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "assigned_count": 0,
  "completed_count": 0
}
```

TaskResponse

### 属性

| 名称        | 类型   | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------ | ----- | ---- | ----------- | ---- |
| title       | string | true  | none | Title       | none |
| description | any    | false | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称     | 类型 | 必选  | 约束 | 中文名   | 说明 |
| -------- | ---- | ----- | ---- | -------- | ---- |
| due_date | any  | false | none | Due Date | none |

anyOf

| 名称          | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | string(date-time) | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称          | 类型              | 必选  | 约束 | 中文名        | 说明 |
| ------------- | ----------------- | ----- | ---- | ------------- | ---- |
| id            | integer           | true  | none | Id            | none |
| created_by_id | integer           | true  | none | Created By Id | none |
| created_at    | string(date-time) | true  | none | Created At    | none |
| updated_at    | any               | false | none | Updated At    | none |

anyOf

| 名称          | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | string(date-time) | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称           | 类型 | 必选  | 约束 | 中文名         | 说明 |
| -------------- | ---- | ----- | ---- | -------------- | ---- |
| assigned_count | any  | false | none | Assigned Count | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | integer | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称            | 类型 | 必选  | 约束 | 中文名          | 说明 |
| --------------- | ---- | ----- | ---- | --------------- | ---- |
| completed_count | any  | false | none | Completed Count | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | integer | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_TaskSubmissionResponse">TaskSubmissionResponse</h2>

<a id="schematasksubmissionresponse"></a>
<a id="schema_TaskSubmissionResponse"></a>
<a id="tocStasksubmissionresponse"></a>
<a id="tocstasksubmissionresponse"></a>

```json
{
  "content": "string",
  "file_path": "string",
  "id": 0,
  "task_id": 0,
  "student_id": 0,
  "submitted_at": "2019-08-24T14:15:22Z",
  "score": 0,
  "feedback": "string",
  "graded_at": "2019-08-24T14:15:22Z"
}
```

TaskSubmissionResponse

### 属性

| 名称    | 类型 | 必选  | 约束 | 中文名  | 说明 |
| ------- | ---- | ----- | ---- | ------- | ---- |
| content | any  | false | none | Content | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称      | 类型 | 必选  | 约束 | 中文名    | 说明 |
| --------- | ---- | ----- | ---- | --------- | ---- |
| file_path | any  | false | none | File Path | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称         | 类型              | 必选  | 约束 | 中文名       | 说明 |
| ------------ | ----------------- | ----- | ---- | ------------ | ---- |
| id           | integer           | true  | none | Id           | none |
| task_id      | integer           | true  | none | Task Id      | none |
| student_id   | integer           | true  | none | Student Id   | none |
| submitted_at | string(date-time) | true  | none | Submitted At | none |
| score        | any               | false | none | Score        | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | integer | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称     | 类型 | 必选  | 约束 | 中文名   | 说明 |
| -------- | ---- | ----- | ---- | -------- | ---- |
| feedback | any  | false | none | Feedback | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称      | 类型 | 必选  | 约束 | 中文名    | 说明 |
| --------- | ---- | ----- | ---- | --------- | ---- |
| graded_at | any  | false | none | Graded At | none |

anyOf

| 名称          | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | string(date-time) | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_TaskUpdate">TaskUpdate</h2>

<a id="schemataskupdate"></a>
<a id="schema_TaskUpdate"></a>
<a id="tocStaskupdate"></a>
<a id="tocstaskupdate"></a>

```json
{
  "title": "string",
  "description": "string",
  "due_date": "2019-08-24T14:15:22Z"
}
```

TaskUpdate

### 属性

| 名称        | 类型   | 必选  | 约束 | 中文名      | 说明 |
| ----------- | ------ | ----- | ---- | ----------- | ---- |
| title       | string | true  | none | Title       | none |
| description | any    | false | none | Description | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称     | 类型 | 必选  | 约束 | 中文名   | 说明 |
| -------- | ---- | ----- | ---- | -------- | ---- |
| due_date | any  | false | none | Due Date | none |

anyOf

| 名称          | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | string(date-time) | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_Token">Token</h2>

<a id="schematoken"></a>
<a id="schema_Token"></a>
<a id="tocStoken"></a>
<a id="tocstoken"></a>

```json
{
  "access_token": "string",
  "token_type": "string",
  "user": {
    "username": "string",
    "full_name": "string",
    "id": 0,
    "is_active": true,
    "created_at": "2019-08-24T14:15:22Z",
    "roles": []
  }
}
```

Token

### 属性

| 名称         | 类型                                | 必选 | 约束 | 中文名       | 说明 |
| ------------ | ----------------------------------- | ---- | ---- | ------------ | ---- |
| access_token | string                              | true | none | Access Token | none |
| token_type   | string                              | true | none | Token Type   | none |
| user         | [UserResponse](#schemauserresponse) | true | none |              | none |

<h2 id="tocS_TopicCreate">TopicCreate</h2>

<a id="schematopiccreate"></a>
<a id="schema_TopicCreate"></a>
<a id="tocStopiccreate"></a>
<a id="tocstopiccreate"></a>

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false
}
```

TopicCreate

### 属性

| 名称      | 类型   | 必选  | 约束 | 中文名    | 说明 |
| --------- | ------ | ----- | ---- | --------- | ---- |
| title     | string | true  | none | Title     | none |
| content   | string | true  | none | Content   | none |
| is_sticky | any    | false | none | Is Sticky | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | boolean | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称      | 类型 | 必选  | 约束 | 中文名    | 说明 |
| --------- | ---- | ----- | ---- | --------- | ---- |
| is_closed | any  | false | none | Is Closed | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | boolean | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_TopicResponse">TopicResponse</h2>

<a id="schematopicresponse"></a>
<a id="schema_TopicResponse"></a>
<a id="tocStopicresponse"></a>
<a id="tocstopicresponse"></a>

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false,
  "id": 0,
  "created_by_id": 0,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "created_by_name": "string",
  "replies_count": 0
}
```

TopicResponse

### 属性

| 名称      | 类型   | 必选  | 约束 | 中文名    | 说明 |
| --------- | ------ | ----- | ---- | --------- | ---- |
| title     | string | true  | none | Title     | none |
| content   | string | true  | none | Content   | none |
| is_sticky | any    | false | none | Is Sticky | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | boolean | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称      | 类型 | 必选  | 约束 | 中文名    | 说明 |
| --------- | ---- | ----- | ---- | --------- | ---- |
| is_closed | any  | false | none | Is Closed | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | boolean | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称          | 类型              | 必选  | 约束 | 中文名        | 说明 |
| ------------- | ----------------- | ----- | ---- | ------------- | ---- |
| id            | integer           | true  | none | Id            | none |
| created_by_id | integer           | true  | none | Created By Id | none |
| created_at    | string(date-time) | true  | none | Created At    | none |
| updated_at    | any               | false | none | Updated At    | none |

anyOf

| 名称          | 类型              | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ----------------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | string(date-time) | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称            | 类型 | 必选  | 约束 | 中文名          | 说明 |
| --------------- | ---- | ----- | ---- | --------------- | ---- |
| created_by_name | any  | false | none | Created By Name | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称          | 类型 | 必选  | 约束 | 中文名        | 说明 |
| ------------- | ---- | ----- | ---- | ------------- | ---- |
| replies_count | any  | false | none | Replies Count | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | integer | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_TopicUpdate">TopicUpdate</h2>

<a id="schematopicupdate"></a>
<a id="schema_TopicUpdate"></a>
<a id="tocStopicupdate"></a>
<a id="tocstopicupdate"></a>

```json
{
  "title": "string",
  "content": "string",
  "is_sticky": false,
  "is_closed": false
}
```

TopicUpdate

### 属性

| 名称  | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ----- | ---- | ----- | ---- | ------ | ---- |
| title | any  | false | none | Title  | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称    | 类型 | 必选  | 约束 | 中文名  | 说明 |
| ------- | ---- | ----- | ---- | ------- | ---- |
| content | any  | false | none | Content | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称      | 类型 | 必选  | 约束 | 中文名    | 说明 |
| --------- | ---- | ----- | ---- | --------- | ---- |
| is_sticky | any  | false | none | Is Sticky | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | boolean | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称      | 类型 | 必选  | 约束 | 中文名    | 说明 |
| --------- | ---- | ----- | ---- | --------- | ---- |
| is_closed | any  | false | none | Is Closed | none |

anyOf

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | boolean | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_UserCreate">UserCreate</h2>

<a id="schemausercreate"></a>
<a id="schema_UserCreate"></a>
<a id="tocSusercreate"></a>
<a id="tocsusercreate"></a>

```json
{
  "username": "string",
  "full_name": "string",
  "password": "string",
  "role": "student"
}
```

UserCreate

### 属性

| 名称      | 类型   | 必选  | 约束 | 中文名    | 说明 |
| --------- | ------ | ----- | ---- | --------- | ---- |
| username  | string | true  | none | Username  | none |
| full_name | any    | false | none | Full Name | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称     | 类型   | 必选  | 约束 | 中文名   | 说明 |
| -------- | ------ | ----- | ---- | -------- | ---- |
| password | string | true  | none | Password | none |
| role     | any    | false | none | Role     | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_UserResponse">UserResponse</h2>

<a id="schemauserresponse"></a>
<a id="schema_UserResponse"></a>
<a id="tocSuserresponse"></a>
<a id="tocsuserresponse"></a>

```json
{
  "username": "string",
  "full_name": "string",
  "id": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "roles": []
}
```

UserResponse

### 属性

| 名称      | 类型   | 必选  | 约束 | 中文名    | 说明 |
| --------- | ------ | ----- | ---- | --------- | ---- |
| username  | string | true  | none | Username  | none |
| full_name | any    | false | none | Full Name | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称       | 类型                                  | 必选  | 约束 | 中文名     | 说明 |
| ---------- | ------------------------------------- | ----- | ---- | ---------- | ---- |
| id         | integer                               | true  | none | Id         | none |
| is_active  | boolean                               | true  | none | Is Active  | none |
| created_at | string(date-time)                     | true  | none | Created At | none |
| roles      | [[RoleResponse](#schemaroleresponse)] | false | none | Roles      | none |

<h2 id="tocS_UserUpdate">UserUpdate</h2>

<a id="schemauserupdate"></a>
<a id="schema_UserUpdate"></a>
<a id="tocSuserupdate"></a>
<a id="tocsuserupdate"></a>

```json
{
  "full_name": "string",
  "password": "string"
}
```

UserUpdate

### 属性

| 名称      | 类型 | 必选  | 约束 | 中文名    | 说明 |
| --------- | ---- | ----- | ---- | --------- | ---- |
| full_name | any  | false | none | Full Name | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

continued

| 名称     | 类型 | 必选  | 约束 | 中文名   | 说明 |
| -------- | ---- | ----- | ---- | -------- | ---- |
| password | any  | false | none | Password | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型 | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ---- | ----- | ---- | ------ | ---- |
| » _anonymous_ | null | false | none |        | none |

<h2 id="tocS_ValidationError">ValidationError</h2>

<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": ["string"],
  "msg": "string",
  "type": "string"
}
```

ValidationError

### 属性

| 名称 | 类型    | 必选 | 约束 | 中文名   | 说明 |
| ---- | ------- | ---- | ---- | -------- | ---- |
| loc  | [anyOf] | true | none | Location | none |

anyOf

| 名称          | 类型   | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------ | ----- | ---- | ------ | ---- |
| » _anonymous_ | string | false | none |        | none |

or

| 名称          | 类型    | 必选  | 约束 | 中文名 | 说明 |
| ------------- | ------- | ----- | ---- | ------ | ---- |
| » _anonymous_ | integer | false | none |        | none |

continued

| 名称 | 类型   | 必选 | 约束 | 中文名     | 说明 |
| ---- | ------ | ---- | ---- | ---------- | ---- |
| msg  | string | true | none | Message    | none |
| type | string | true | none | Error Type | none |
