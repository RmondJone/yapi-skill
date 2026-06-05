# Yapi Skill

<div align="center">

![Claude](https://img.shields.io/badge/Claude-AI%20Assistant-blueviolet?style=for-the-badge&logo=anthropic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=license&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge&logo=github&logoColor=white)

**🚀 Yapi 接口定义自动获取工具 | 一键拉取接口文档交给 LLM**

*基于 Claude Code Skills 打造的 Yapi 集成工具，专注接口定义数据获取与回传*

</div>

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔌 **零配置启动** | 自动从 `.env` 加载 Yapi 连接信息，无需手动传参 |
| 🐍 **脚本化调用** | 内置 Python 脚本直接对接 Yapi 开放接口，不依赖任何 MCP 工具 |
| 📦 **开箱即用** | 一行命令安装，Claude 自动识别并激活 |
| 🎯 **精准定位** | 支持按 path、ID、关键词多种方式定位接口 |
| 📋 **原始 JSON 回传** | 透传 Yapi 原始响应结构，方便 LLM 直接解析 |
| 🛡️ **Cloudflare 兼容** | 已处理 Python urllib 的 UA 拦截问题 |

---

## 🚀 快速开始

### 安装

```bash
npx skills add RmondJone/yapi-skill@yapi-skill -g -y
```

或者将 `.claude/skills/yapi-skill/` 目录复制到任意工程的 `.claude/skills/` 下。

### .env 配置

在工程根目录创建 `.env` 文件，写入以下三项：

```bash
# API 配置
YAPI_URL=https://yapi.guohanlin.com/
YAPI_TOKEN=你的项目token
YAPI_PROJECT_ID=你的项目ID
```

> 💡 Token 在 Yapi 平台「项目设置 → 接口设置」中生成。`.env` 不存在时 SKILL 会从当前目录向上自动查找。

### 触发词

在 Claude Code 中描述以下场景时，技能将自动激活：

| 触发词 | 说明 |
|--------|------|
| `调 yapi-skill` | 显式调用本技能 |
| `拉取 yapi 接口定义` | 主动拉取接口文档 |
| `查看 yapi 接口` / `查询 yapi 接口` | 查询接口元信息 |
| `实现 xx 接口` | 间接触发（实现前需要接口定义） |
| `调用 /auth/login/password` | 提到具体接口路径时 |

---

## 📦 技能详情

### yapi-skill

<div align="left">

**Yapi 接口定义自动获取工具 v1.0**

通过内置 Python 脚本对接 Yapi 开放接口，自动加载 `.env` 配置，把接口定义以原始 JSON 形式回传给 LLM。

```bash
npx skills add RmondJone/yapi-skill@yapi-skill -g -y
```

</div>

#### 触发词

> `调 yapi-skill` · `拉取 yapi 接口定义` · `查看 yapi 接口` · `查询 yapi 接口字段` · `我需要 xx 接口的定义` · `拿一下 yapi 上的 xx 接口`

#### 工作流程

```
1. 加载 .env 配置（用户指定路径 / 从 CWD 向上查找）
2. 列出"要查询的接口集合"（根据用户描述推断）
3. 用 Bash 执行 scripts/yapi_fetch.py
4. 合并所有接口的 detail JSON 数组
5. 透传给 LLM 用于后续代码生成
```

#### 核心能力

| 模块 | 说明 |
|------|------|
| **自动 .env 加载** | 支持用户显式传参 + 自动向上查找两种方式 |
| **7 种 action** | 覆盖 Yapi 官方开放接口全集 |
| **Cloudflare 兼容** | 自动注入浏览器 UA，绕过 CDN 拦截 |
| **SSL 证书处理** | 使用 certifi 解决 macOS Python 证书问题 |
| **原始 JSON 透传** | 不重组结构、不丢字段，保留 Yapi 原生字段名 |
| **批量并发查询** | 多个接口支持并行调用（单次最多 5 个） |

#### 支持的 action

| action | 对应 Yapi 接口 | 用途 |
|--------|---------------|------|
| `project_info` | `GET /api/project/get` | 获取项目基本信息 |
| `cat_menu` | `GET /api/interface/getCatMenu` | 获取项目分类菜单 |
| `interface_menu` | `GET /api/interface/list_menu` | 获取完整菜单树（分类+接口） |
| `category_interfaces` | `GET /api/interface/list_cat` | 获取某个分类下的接口列表 |
| `interface_detail` | `GET /api/interface/get` | 按 ID 拿完整详情 |
| `interface_by_path` | `GET /api/interface/get` | 按 path 精确查找接口 |
| `search` | 本地按关键词过滤 | 按关键词模糊搜索接口 |

#### 项目结构

```
yapi-skill/
├── README.md                          # 本文件
├── YAPI-OPENAPI.md                    # Yapi 开放接口定义文档（参考）
├── .env.example                       # .env 配置示例
└── .claude/
    └── skills/
        └── yapi-skill/
            ├── SKILL.md               # SKILL 工作流定义（给 LLM 看）
            └── scripts/
                └── yapi_fetch.py      # Yapi 开放接口调用脚本
```

#### 脚本调用示例

```bash
# 获取项目信息
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --action project_info

# 按路径精确查找接口
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --action interface_by_path \
  --path "/auth/login/password" \
  --method POST

# 按关键词搜索
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --action search \
  --keyword "登录"

# 按 ID 拿完整接口定义
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --action interface_detail \
  --id 4921

# 指定 .env 路径
python3 .claude/skills/yapi-skill/scripts/yapi_fetch.py \
  --env /path/to/project/.env \
  --action cat_menu
```

#### 依赖

| 依赖 | 用途 | 必填 |
|------|------|------|
| Python 3.7+ | 运行调用脚本 | 是 |
| `certifi` | macOS 上 SSL 证书支持 | 推荐 |
| `.env` 文件 | Yapi 连接配置 | 是 |

#### 环境要求

- Python 3.7 或更高版本
- macOS / Linux / Windows 均可
- 仅使用 Python 标准库 + `certifi`（可选）

---

## 🎯 使用示例

### 示例 1：拉取单个接口定义

```
用户: 帮我拿一下 /auth/login/password 这个接口的定义
Claude: (自动激活 yapi-skill)
→ 加载 .env 配置
→ 执行 interface_by_path 拿到接口 ID
→ 执行 interface_detail 拿到完整定义
→ 回传 Yapi 原始 JSON
```

### 示例 2：实现某个接口功能

```
用户: 用 yapi-skill 拿一下登录接口定义，然后实现 Flutter 登录页
Claude: (自动激活 yapi-skill)
→ 加载 .env 配置
→ 拉取 /auth/login/password、/auth/login/code、/auth/login/captcha 等接口
→ 按 Flutter 网络规范生成 LoginParams、LoginResponse、NetWorkController
→ 实现 LoginPage
```

### 示例 3：批量查询多个接口

```
用户: 调 yapi-skill，帮我看看用户模块都有哪些接口
Claude: (自动激活 yapi-skill)
→ 加载 .env 配置
→ 执行 interface_menu 拿到全量菜单
→ 过滤"用户接口"分类
→ 列出所有接口的 path、method、title
```

### 示例 4：搜索特定功能接口

```
用户: yapi-skill 找一下所有跟"作品"相关的接口
Claude: (自动激活 yapi-skill)
→ 加载 .env 配置
→ 执行 search --keyword "作品"
→ 命中 4 个分类下共 20+ 个接口
→ 列出所有匹配结果
```

---

## 📊 技术栈

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Yapi](https://img.shields.io/badge/Yapi-Open%20API-25A162?style=for-the-badge&logo=swagger&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-Skills-blueviolet?style=for-the-badge&logo=anthropic&logoColor=white)

---

## 📄 许可证

本项目基于 [MIT License](LICENSE) 许可证开源。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

<div align="center">

**Made with ❤️ by RmondJone**

</div>
