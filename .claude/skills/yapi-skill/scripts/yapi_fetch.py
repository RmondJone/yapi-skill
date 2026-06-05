#!/usr/bin/env python3
# 注释：Yapi 开放接口调用脚本
# 时间：2026/6/5
# 作者：郭翰林

"""Yapi 开放接口调用脚本。

按 YAPI-OPENAPI.md 文档实现 Yapi 平台开放 API 的 HTTP 调用。
不依赖任何 MCP 工具，直接通过 HTTP 调 Yapi 服务。

支持的 action:
  project_info         获取项目基本信息
  cat_menu             获取项目分类菜单
  interface_menu       获取项目接口菜单树（含分类及接口）
  category_interfaces  获取某个分类下的接口列表
  interface_detail     根据接口 ID 获取完整详情
  interface_by_path    根据接口路径精确查找接口详情
  search               按关键词模糊搜索接口（基于 interface_menu 过滤）

环境变量（从 .env 加载）:
  YAPI_URL         Yapi 服务地址（带末尾 /）
  YAPI_TOKEN       项目 token
  YAPI_PROJECT_ID  项目 ID
"""

import argparse
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def load_env(env_path: str) -> dict:
    """加载 .env 文件。

    兼容 KEY=VALUE、KEY="VALUE"、KEY='VALUE'、带 # 注释、空行。
    """
    env: dict = {}
    path = Path(env_path)
    if not path.exists():
        raise FileNotFoundError(f".env 文件不存在: {env_path}")

    with path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            # 去掉包裹的引号
            if len(value) >= 2 and (
                (value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")
            ):
                value = value[1:-1]
            env[key] = value

    required = ["YAPI_URL", "YAPI_TOKEN", "YAPI_PROJECT_ID"]
    missing = [k for k in required if not env.get(k)]
    if missing:
        raise ValueError(
            f".env 缺少必要配置: {', '.join(missing)}。请在 .env 中配置 YAPI_URL / YAPI_TOKEN / YAPI_PROJECT_ID"
        )
    return env


def find_env(start_dir: str) -> str:
    """从 start_dir 开始向上查找 .env 文件，找到第一个就返回。"""
    current = Path(start_dir).resolve()
    for parent in [current, *current.parents]:
        candidate = parent / ".env"
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(
        f"从 {start_dir} 向上未找到 .env 文件。请在工程根目录创建 .env 并配置 YAPI_URL / YAPI_TOKEN / YAPI_PROJECT_ID"
    )


def _build_ssl_context() -> ssl.SSLContext:
    """构造 SSL context，优先使用 certifi 的 CA 证书。

    macOS 系统 Python 的 urllib 默认不信任系统 CA，会触发
    CERTIFICATE_VERIFY_FAILED。这里用 certifi 注入证书。
    如果 certifi 不可用，回退到未验证模式（仅用于内网 Yapi 调试）。
    """
    try:
        import certifi

        ctx = ssl.create_default_context(cafile=certifi.where())
        return ctx
    except ImportError:
        # 内网 Yapi 没有公网证书链时，允许跳过校验
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx


def yapi_get(env: dict, api_path: str, params: dict) -> dict:
    """调用 Yapi 开放接口（GET 请求）。

    自动把 token 拼到 query 里。
    返回 Yapi 原始 JSON。
    """
    params = {k: v for k, v in params.items() if v is not None}
    params["token"] = env["YAPI_TOKEN"]

    base = env["YAPI_URL"].rstrip("/")
    url = f"{base}{api_path}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url, method="GET")
    req.add_header("Content-Type", "application/json")
    # Cloudflare 1003/1010：默认的 Python-urllib UA 会被 CDN 拦截为爬虫
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )

    ssl_ctx = _build_ssl_context()
    try:
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        return {
            "errcode": e.code,
            "errmsg": f"HTTP {e.code}: {e.reason}",
            "data": None,
        }
    except Exception as e:
        return {
            "errcode": -1,
            "errmsg": f"请求失败: {type(e).__name__}: {e}",
            "data": None,
        }


# ============== Yapi 开放接口封装 ==============

def get_project_info(env: dict) -> dict:
    """GET /api/project/get"""
    return yapi_get(env, "/api/project/get", {})


def get_cat_menu(env: dict) -> dict:
    """GET /api/interface/getCatMenu"""
    return yapi_get(env, "/api/interface/getCatMenu", {"project_id": env["YAPI_PROJECT_ID"]})


def get_interface_menu(env: dict) -> dict:
    """GET /api/interface/list_menu"""
    return yapi_get(
        env,
        "/api/interface/list_menu",
        {"project_id": env["YAPI_PROJECT_ID"]},
    )


def get_category_interfaces(env: dict, catid: int, page: int = 1, limit: int = 100) -> dict:
    """GET /api/interface/list_cat"""
    return yapi_get(
        env,
        "/api/interface/list_cat",
        {"catid": catid, "page": page, "limit": limit},
    )


def get_interface_detail(env: dict, interface_id: int) -> dict:
    """GET /api/interface/get"""
    return yapi_get(env, "/api/interface/get", {"id": interface_id})


def get_interface_by_path(env: dict, path: str, method: str = "") -> dict:
    """GET /api/interface/get （按 path 精确匹配）"""
    return yapi_get(
        env,
        "/api/interface/get",
        {"path": path, "method": method.upper() if method else None},
    )


def search_interface(env: dict, keyword: str) -> dict:
    """按关键词搜索接口。

    Yapi 官方没有专门的 search 接口，这里通过 list_menu 拿到全量
    菜单树，然后在本地按 title / path / method 模糊匹配。
    """
    menu = get_interface_menu(env)
    if menu.get("errcode") != 0:
        return menu

    keyword_lower = keyword.lower()
    matched_cats: list = []
    for cat in menu.get("data", []) or []:
        hits = []
        for iface in cat.get("list", []) or []:
            title = (iface.get("title") or "").lower()
            path = (iface.get("path") or "").lower()
            method = (iface.get("method") or "").lower()
            if (
                keyword_lower in title
                or keyword_lower in path
                or keyword_lower in method
            ):
                hits.append(iface)
        if hits:
            matched_cats.append(
                {
                    "_id": cat.get("_id"),
                    "name": cat.get("name"),
                    "project_id": cat.get("project_id"),
                    "desc": cat.get("desc", ""),
                    "list": hits,
                }
            )

    return {
        "errcode": 0,
        "errmsg": "成功",
        "data": matched_cats,
        "_meta": {"keyword": keyword, "total_matched": sum(len(c["list"]) for c in matched_cats)},
    }


# ============== 批量拉取（拿到完整 detail） ==============

def fetch_interfaces_full(env: dict, items: list) -> list:
    """对每个 {path, method} 或 {id} 调用 get_interface 拿完整 detail。

    items 支持两种元素：
      {"path": "/api/xxx", "method": "GET"}   按路径查
      {"id": 4396}                            按 ID 查

    返回 list[dict]，每个 dict 是 Yapi /api/interface/get 的完整 data。
    """
    results: list = []
    for item in items:
        if "id" in item:
            resp = get_interface_detail(env, int(item["id"]))
        else:
            resp = get_interface_by_path(env, item["path"], item.get("method", ""))
        results.append(resp)
    return results


# ============== CLI 入口 ==============

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Yapi 开放接口调用工具（参考 YAPI-OPENAPI.md）"
    )
    parser.add_argument("--env", help=".env 文件绝对路径；不传则从 CWD 向上查找")
    parser.add_argument(
        "--action",
        required=True,
        choices=[
            "project_info",
            "cat_menu",
            "interface_menu",
            "category_interfaces",
            "interface_detail",
            "interface_by_path",
            "search",
        ],
    )
    parser.add_argument("--id", type=int, help="接口 ID（interface_detail 用）")
    parser.add_argument("--catid", type=int, help="分类 ID（category_interfaces 用）")
    parser.add_argument("--path", help="接口路径（interface_by_path 用）")
    parser.add_argument("--method", help="接口方法 GET/POST/PUT/DELETE（interface_by_path 用）")
    parser.add_argument("--keyword", help="搜索关键词（search 用）")
    args = parser.parse_args()

    try:
        env_path = args.env if args.env else find_env(os.getcwd())
        env = load_env(env_path)
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"errcode": -1, "errmsg": str(e), "data": None}, ensure_ascii=False))
        return 1

    if args.action == "project_info":
        result = get_project_info(env)
    elif args.action == "cat_menu":
        result = get_cat_menu(env)
    elif args.action == "interface_menu":
        result = get_interface_menu(env)
    elif args.action == "category_interfaces":
        if not args.catid:
            print(json.dumps({"errcode": -1, "errmsg": "缺少 --catid", "data": None}, ensure_ascii=False))
            return 1
        result = get_category_interfaces(env, args.catid)
    elif args.action == "interface_detail":
        if not args.id:
            print(json.dumps({"errcode": -1, "errmsg": "缺少 --id", "data": None}, ensure_ascii=False))
            return 1
        result = get_interface_detail(env, args.id)
    elif args.action == "interface_by_path":
        if not args.path:
            print(json.dumps({"errcode": -1, "errmsg": "缺少 --path", "data": None}, ensure_ascii=False))
            return 1
        result = get_interface_by_path(env, args.path, args.method)
    elif args.action == "search":
        if not args.keyword:
            print(json.dumps({"errcode": -1, "errmsg": "缺少 --keyword", "data": None}, ensure_ascii=False))
            return 1
        result = search_interface(env, args.keyword)
    else:
        result = {"errcode": -1, "errmsg": f"未知 action: {args.action}", "data": None}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("errcode") == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
