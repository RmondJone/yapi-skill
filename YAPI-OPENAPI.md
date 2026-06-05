# YApi OpenAPI 接口文档

> 基于 YApi 官方开放 API 整理的接口定义文档

## 目录

- [认证方式](#认证方式)
- [项目接口](#项目接口)
  - [获取项目基本信息](#获取项目基本信息)
- [分类接口](#分类接口)
  - [新增接口分类](#新增接口分类)
  - [获取菜单列表](#获取菜单列表)
  - [获取某个分类下接口列表](#获取某个分类下接口列表)
  - [获取接口菜单列表](#获取接口菜单列表)
- [接口接口](#接口接口)
  - [获取接口数据](#获取接口数据)
  - [新增接口](#新增接口)
  - [新增或更新接口](#新增或更新接口)
  - [获取接口列表数据](#获取接口列表数据)
  - [更新接口](#更新接口)
- [数据导入接口](#数据导入接口)
  - [服务端数据导入](#服务端数据导入)

---

## 认证方式

所有接口通过项目 Token 进行认证，Token 在项目设置中获取。

| 参数名称 | 位置 | 类型 | 必填 | 说明 |
|---------|------|------|------|------|
| token | Query/Body | string | 是 | 项目 Token |

---

## 项目接口

### 获取项目基本信息

获取项目的详细信息。

**请求**

```
GET /api/project/get
```

**Query 参数**

| 参数名称 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| token | string | 是 | 项目 Token |

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "_id": 299,
    "name": "项目名称",
    "basepath": "",
    "project_type": "public"
  }
}
```

---

## 分类接口

### 新增接口分类

在项目中新增接口分类（分类/文件夹）。

**请求**

```
POST /api/interface/add_cat
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/x-www-form-urlencoded | 是 |

**Body 参数**

| 参数名称 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| token | text | 是 | 项目 Token |
| project_id | text | 是 | 项目 ID |
| name | text | 是 | 分类名称 |
| desc | text | 否 | 分类描述 |

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "_id": 1376,
    "name": "新分类",
    "project_id": 299
  }
}
```

---

### 获取菜单列表

获取项目中的分类菜单列表。

**请求**

```
GET /api/interface/getCatMenu
```

**Query 参数**

| 参数名称 | 必填 | 说明 |
|---------|------|------|
| token | 是 | 项目 Token |
| project_id | 是 | 项目 ID |

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": [
    {
      "_id": 1376,
      "name": "公共分类",
      "project_id": 299
    }
  ]
}
```

---

### 获取某个分类下接口列表

获取指定分类下的所有接口列表。

**请求**

```
GET /api/interface/list_cat
```

**Query 参数**

| 参数名称 | 必填 | 说明 |
|---------|------|------|
| token | 是 | 项目 Token |
| catid | 是 | 分类 ID |
| page | 否 | 当前页面，默认 1 |
| limit | 否 | 每页数量，默认 10 |

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": [
    {
      "_id": 4396,
      "project_id": 299,
      "catid": 1376,
      "title": "/api/user/info",
      "path": "/api/user/info",
      "method": "GET",
      "status": "done",
      "add_time": 1511431245,
      "up_time": 1511431245
    }
  ]
}
```

---

### 获取接口菜单列表

获取项目接口的完整菜单树（包含分类及其下的接口）。

**请求**

```
GET /api/interface/list_menu
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/json | 是 |

**Query 参数**

| 参数名称 | 必填 | 说明 |
|---------|------|------|
| project_id | 是 | 项目 ID |
| token | 是 | 项目 Token |

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": [
    {
      "_id": 1376,
      "name": "公共分类",
      "project_id": 299,
      "desc": "公共分类",
      "list": [
        {
          "_id": 4396,
          "title": "/api/user/info",
          "path": "/api/user/info",
          "method": "GET",
          "res_body_type": "json",
          "status": "done",
          "req_body_form": [],
          "req_params": [],
          "req_headers": [],
          "req_query": []
        }
      ]
    }
  ]
}
```

---

## 接口接口

### 获取接口数据

获取某个接口的完整详细信息。

**请求**

```
GET /api/interface/get
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/json | 是 |

**Query 参数**

| 参数名称 | 必填 | 说明 |
|---------|------|------|
| id | 是 | 接口 ID |
| token | 是 | 项目 Token |

**响应 data 字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| _id | number | 接口 ID |
| project_id | number | 项目 ID |
| catid | number | 分类 ID |
| title | string | 接口标题 |
| path | string | 请求路径 |
| method | string | 请求方法 (GET/POST/PUT/DELETE 等) |
| req_body_type | string | 请求数据类型 (raw/form/json) |
| res_body | string | 返回数据内容 |
| res_body_type | string | 返回数据类型 (json/raw) |
| req_body_form | array | 请求 form 参数列表 |
| req_params | array | 请求路径参数列表 |
| req_headers | array | 请求头列表 |
| req_query | array | Query 参数列表 |
| status | string | 接口状态 (done/undone) |
| res_body_is_json_schema | boolean | 返回数据是否为 json-schema |

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "_id": 4396,
    "project_id": 299,
    "catid": 1376,
    "title": "/api/user/info",
    "path": "/api/user/info",
    "method": "GET",
    "req_body_type": "json",
    "res_body": "{\"errcode\":0,\"errmsg\":\"成功\",\"data\":{}}",
    "res_body_type": "json",
    "req_body_form": [
      {
        "name": "username",
        "type": "text",
        "example": "admin",
        "desc": "用户名",
        "required": "1"
      }
    ],
    "req_params": [
      {
        "name": "id",
        "example": "1",
        "desc": "用户ID"
      }
    ],
    "req_headers": [
      {
        "name": "Content-Type",
        "type": "text",
        "example": "application/json",
        "desc": "",
        "required": "1"
      }
    ],
    "req_query": [
      {
        "name": "page",
        "type": "number",
        "example": "1",
        "desc": "页码",
        "required": "1"
      }
    ],
    "status": "done"
  }
}
```

---

### 新增接口

在指定分类下新增一个接口。

**请求**

```
POST /api/interface/add
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/json | 是 |

**Body 参数**

| 参数名称 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| token | string | 是 | 项目 Token |
| title | string | 是 | 接口标题 |
| catid | string | 是 | 分类 ID |
| path | string | 是 | 请求路径 |
| method | string | 是 | 请求方法 |
| status | string | 否 | 接口状态 (done/undone)，默认 undone |
| req_body_type | string | 否 | 请求数据类型 (raw/form/json) |
| res_body_type | string | 否 | 返回数据类型 (json/raw) |
| res_body | string | 否 | 返回数据内容 |
| req_body_form | array | 否 | 请求 form 参数列表 |
| req_params | array | 否 | 请求路径参数列表 |
| req_headers | array | 否 | 请求头列表 |
| req_query | array | 否 | Query 参数列表 |
| desc | string | 否 | 接口描述 |
| switch_notice | boolean | 否 | 是否开启消息通知 |
| message | string | 否 | 通知消息内容 |

**请求示例**

```json
{
  "token": "xxx",
  "title": "/api/user/list",
  "catid": "1376",
  "path": "/api/user/list",
  "method": "GET",
  "status": "undone",
  "res_body_type": "json",
  "res_body": "{\"errcode\":0,\"errmsg\":\"成功\",\"data\":[]}",
  "req_query": [],
  "req_headers": [],
  "req_body_form": [],
  "req_params": []
}
```

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "ok": 1,
    "nModified": 1,
    "n": 1
  }
}
```

---

### 新增或更新接口

新增接口，如果接口已存在则更新（根据 id 判断）。

**请求**

```
POST /api/interface/save
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/json | 是 |

**Body 参数**

与新增接口相同，多了一个 `id` 字段：

| 参数名称 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| id | string | 否 | 接口 ID，存在则更新，不存在则新增 |

**请求示例**

```json
{
  "token": "xxx",
  "id": "4396",
  "title": "/api/user/list",
  "catid": "1376",
  "path": "/api/user/list",
  "method": "GET",
  "status": "done",
  "res_body_type": "json",
  "res_body": "{\"errcode\":0,\"errmsg\":\"成功\",\"data\":[]}"
}
```

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "ok": 1,
    "nModified": 1,
    "n": 1
  }
}
```

---

### 获取接口列表数据

获取项目下的接口列表（简单信息，不包含详细定义）。

**请求**

```
GET /api/interface/list
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/json | 是 |

**Query 参数**

| 参数名称 | 必填 | 说明 |
|---------|------|------|
| project_id | 是 | 项目 ID |
| token | 是 | 项目 Token |
| page | 是 | 当前页数 |
| limit | 是 | 每页数量 |

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": [
    {
      "_id": 4444,
      "project_id": 299,
      "catid": 1376,
      "title": "/api/user/del",
      "path": "/api/user/del",
      "method": "POST",
      "status": "undone",
      "add_time": 1511431246,
      "up_time": 1511751531
    }
  ]
}
```

---

### 更新接口

更新指定接口的信息。

**请求**

```
POST /api/interface/up
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/json | 是 |

**Body 参数**

与新增接口相同，必须包含 `id` 字段：

| 参数名称 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| id | string | 是 | 接口 ID |
| token | string | 是 | 项目 Token |
| title | string | 是 | 接口标题 |
| catid | string | 是 | 分类 ID |
| path | string | 是 | 请求路径 |
| method | string | 是 | 请求方法 |
| status | string | 否 | 接口状态 |
| req_body_type | string | 否 | 请求数据类型 |
| res_body_type | string | 否 | 返回数据类型 |
| res_body | string | 否 | 返回数据内容 |
| req_body_form | array | 否 | 请求 form 参数 |
| req_params | array | 否 | 请求路径参数 |
| req_headers | array | 否 | 请求头列表 |
| req_query | array | 否 | Query 参数列表 |
| desc | string | 否 | 接口描述 |

**请求示例**

```json
{
  "token": "xxx",
  "id": "4396",
  "title": "/api/user/list",
  "catid": "1376",
  "path": "/api/user/list",
  "method": "GET",
  "status": "done",
  "res_body_type": "json",
  "res_body": "{\"errcode\":0,\"errmsg\":\"成功\",\"data\":[]}"
}
```

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "ok": 1,
    "nModified": 1,
    "n": 1
  }
}
```

---

## 数据导入接口

### 服务端数据导入

从 URL 或 JSON 导入接口数据到项目中。

**请求**

```
POST /api/open/import_data
```

**Headers**

| 参数名称 | 参数值 | 必填 |
|---------|--------|------|
| Content-Type | application/x-www-form-urlencoded | 是 |

**Body 参数**

| 参数名称 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| token | text | 是 | 项目 Token |
| type | text | 是 | 导入方式，如 swagger、postman、har 等 |
| merge | text | 是 | 数据同步方式：normal(普通模式)、good(智能合并)、merge(完全覆盖) |
| json | text | 否 | JSON 数据，类型为序列化后的字符串 |
| url | text | 否 | 导入数据 URL，如果存在该参数，将会通过 URL 方式获取数据 |

**请求示例**

```
type=swagger&merge=normal&token=xxx&url=https://example.com/swagger.json
```

**响应示例**

```json
{
  "errcode": 0,
  "errmsg": "成功！",
  "data": {
    "success": true,
    "data": {
      "num": 10
    }
  }
}
```

---

## 接口响应统一格式

所有接口返回统一格式如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | number | 错误码，0 表示成功 |
| errmsg | string | 错误信息 |
| data | object/array | 响应数据 |

---

## 通用字段说明

### 请求参数字段

| 字段 | 说明 |
|------|------|
| name | 参数名称 |
| type | 参数类型 (text/number/integer/boolean 等) |
| example | 示例值 |
| desc | 参数描述 |
| required | 是否必填 (1=必填，0=可选) |

### 接口状态

| 状态 | 说明 |
|------|------|
| done | 已完成 |
| undone | 未完成 |

### 请求数据类型

| 类型 | 说明 |
|------|------|
| json | JSON 格式 |
| form | Form 表单 |
| raw | 原始数据 |

### 返回数据类型

| 类型 | 说明 |
|------|------|
| json | JSON 格式 |
| raw | 原始文本 |