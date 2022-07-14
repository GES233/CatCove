# CatCove

[![img](https://img.shields.io/badge/Cat-Cove-blueviolet.svg?style=flat-square)](https://github.com/GES233/CatCove)

采用 Sanic 搭建的一个轻量论坛 ~~（只有一部分的后端）~~ 。

## 由来

### 猫湾

> 想搭建这个论坛的第一个契机是，就想整个不用备案的后花园，让大家放开了聊那些带点颜色带点敏感而又不那么极端的话题。

> 第二个契机是，我想搭建一个社交网站，把各种分布式啊什么的buff加进去，也没啥特别的目的，想观察人类，哈哈哈。当时想法的名字叫做 `CatCove` （猫湾），再加个灯塔的 icon，就喜欢这种感到指引的感觉。

以上内容来自 `MeowCaveProject` 文档下的「想法.md」。

### Sanic

在我在终端键入 `pip install sanic[ext]` 前，正好看央视六台在演刺猬索尼克，可能这就是所谓缘分吧。

## 安装

### 环境与依赖项

项目采用 Sanic 框架编写，同时部分内容也需要以下的库：

* SQLAlchemy, ORM
* alembic, 数据库迁移
* Pydantic, 接口的检查
* pyyaml, 加载位于项目根目录的 `instance.yaml` 作为实例的配置
* python-jose, 令牌的生成

### 下载

略

## 使用说明

开发中，固略

### 配置

`CatCove` 允许通过多种方式来配置应用。

### 运行

```shell
export ENV = "pro" # In production mode.
python run.py
```

## TODOList

- [x] 连接数据库
- [ ] 基本的用户注册功能（后端部分）
  - [x] 如果数据无误能够向数据库内填充数据
  - [x] 如果密码重复能够通过Responce报错
  - [ ] 注册部分与鉴权相连接，自动跳转到令牌领取处
    - [ ] Context 相关
  - [ ] 邀请码相关机制
- [ ] 内容
  - [ ] UserPost
  - [ ] 与用户绑定（ORM端）
  - [ ] ...
- [ ] 前端的模板
 - [ ] Jinja2 + Bootstrap
- [ ] 完整的鉴权功能
  - [ ] cookie、custom header双重选择
  - [ ] 基于 Redis 的令牌黑名单


## 维护者

[@GES233](https://github.com/GES233)


