![](https://i.loli.net/2019/07/29/5d3e8e11b82d621126.png)

# 🔑 AIP (Anonymous Identify Provider)

![](https://img.shields.io/badge/team-SecureCats-blue?logo=data:image/svg+xml;base64,PHN2ZyBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGZpbGwtcnVsZT0iZXZlbm9kZCIgc3Ryb2tlLWxpbmVq%0D%0Ab2luPSJyb3VuZCIgc3Ryb2tlLW1pdGVybGltaXQ9IjIiIHZpZXdCb3g9IjAgMCAyOSAyOSIgeG1s%0D%0AbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cGF0aCBkPSJtMCA3LjI2MWMxLjUw%0D%0ANCAxMi42MDYgNi4zOTIgMTguMzkgMTQuMjE0IDIxLjYwNHYtMjguODY1Yy0yLjkzMiA1LjcyNC04%0D%0ALjE0MyA4LjExNC0xNC4yMTQgNy4yNjF6IiBmaWxsPSIjZmZmIiAvPgogIDxwYXRoIGQ9Im0yOC40%0D%0AMjkgNy4yNjFjLTEuNTA1IDEyLjYwNi02LjM5MiAxOC4zOS0xNC4yMTUgMjEuNjA0di0yOC44NjVj%0D%0AMi45MzMgNS43MjQgOC4xNDQgOC4xMTQgMTQuMjE1IDcuMjYxeiIgZmlsbD0iI2ViZWJlYiIgLz4K%0D%0APC9zdmc+Cg==&style=flat-square)
![](https://img.shields.io/circleci/build/github/SecureCats/AIP_BackEnd?label=circleci&logo=circleci&style=flat-square)

> FATES: The Fully Anonymous Teaching Evaluation System

## 📦 架构

### 整体架构

- Client 客户端：学生用户
  - AIP 前端：<https://aip.fates.felinae98.cn>
  - TES 前端：<https://pes.fates.felinae98.cn>
- AIP 匿名身份提供服务端
- TES 课程评价服务端

![](https://i.loli.net/2019/07/29/5d3e7be69760d29835.png)

### 目录结构

仓库主要包含 AIP 服务端内容。其中 `frontend/` 路径为 `submodule`，链接至 AIP 前端项目：[SecureCats/AIP_FrontEnd](https://github.com/SecureCats/AIP_FrontEnd)

```
.
├── AIP_BackEnd // AIP 服务端
├── frontend // AIP 前端（以 submodule 形式链接）
│   ├── ...
│   └── src // AIP 前端（工程源代码）
├── ...
└── aipsite // AIP 服务端（工程源代码）
    └── ...
```

### 项目技术

- 服务端：[Django](https://www.djangoproject.com/) / Python
- 前端：[Vue.js](https://vuejs.org) / [Vuetify](https://vuetifyjs.com/en/)

## 🗂 部署

由于项目包含有前后端全部内容，因此克隆项目至本地时需要将 `submodule` 也进行克隆。具体方法为：

```shell
git clone --recursive https://github.com/SecureCats/AIP_BackEnd.git
```

更多有关 submodule 的使用请参考：[Working with submodules.](https://github.blog/2016-02-01-working-with-submodules/)

由于前后端需要同时部署，**因此需要先 build 前端项目，再运行后端项目**。具体操作如下：

### 前端环境部署

1. 配置环境

- 安装 Node.js：[Installing Node.js via package manager](https://nodejs.org/en/download/package-manager/)
- 安装包管理 `yarn`：[yarn | Installation](https://yarnpkg.com/lang/en/docs/install)

2. 安装依赖

```shell
yarn install
```

3. 编译静态文件

```shell
yarn build
```

### 服务端环境部署

1. 配置环境

- 安装 Python：[Python 3 Installation & Setup Guide](https://realpython.com/installing-python/)
- 安装 `pipenv`：[Installing Pipenv](https://docs.pipenv.org/en/latest/install/#installing-pipenv)

2. 安装依赖

```shell
pipenv install
```

3. 进入 Python 虚拟环境

```shell
pipenv shell
```

4. 初始化 Django 框架和数据库

```shell
# Migrate 数据库
python manage.py migrate

# 创建管理员账户
python manage.py createsuperuser
```

5. 启动服务器

```shell
python manage.py runserver
```

登录页面位于：`https://localhost:8000/`

管理页面位于：`http://localhost:8000/admin`

## 🎁 API

### 公钥查询

查询 Public Key：`/api/v1/pubkey/{classno}`

返回数据：

```json
{
  "n": "{n}",
  "a": "{a}",
  "b": "{b}",
  "c": "{c}",
  "g": "{g}",
  "h": "{h}"
}
```

---

**🔑 AIP ©SecureCats.** Released under the MIT License.

Authored and maintained by [Team SecureCats](https://github.com/SecureCats).

© 2019 Made with 🖤 from BIT.

