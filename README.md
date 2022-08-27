# CatCove
![img](https://img.shields.io/badge/license-WTFPL-blue)

基于话题的、轻量的SNS（目前进度10%）。

## 项目背景

来由：

- 几个人或几十个人的后花园
- 小圈子生辰高质内容的站点
- 国内的备案 + 无法过审

想法：*构建一个轻便而易于部署的网页程序，可以随时跑路再建的那种*

## 安装

### 依赖项

- Python
  - ... 一堆插件（见 `requirements.txt` ）
- Pico.css
- SimpleMDE/raw-text (Optional)

### 代码

直接运行：

```bash
git clone https://github.com/GES233/CatCove.git
# Create a env before.
pip install requirements.txt
# Configure the application.
python server.py init
python server.py db
# Following constructions.
python server.py run --pro
```

采用Docker：

略

## 配置及使用

略

## 相关项目

- [GES233/MeowCavePre](https://github.com/GES233/MeowCavePre) 22年上半年整的，如果没有这个根本搞不起来后面的 ~~本地还有个用 `Quart` 重写的同名仓库，不过那时候受 `FastAPI` 影响较深在前端一窍不通的情况下只写了后端部分~~
- [jaggerwang/sanic-in-practice](https://github.com/jaggerwang/sanic-in-practice) 看了他的博客（代码仓库就是所指项目）选择了按照「干净架构」来重构应用 ~~虽然重构的也不咋地，但写起来比之前轻松多了~~
- （待补充）

## 维护者

只有，[我自己](https://github.com/GES233)。

## TODO

- [ ] 表单有「记住我」后能够设置的过期日期
- [ ] 消息机制的引入
  - [ ] APSchedule
  - [ ] 类似于 Flask 的 `flash()` （No-JS）
  - [ ] ESS 的实现（需要JS）
- [ ] 简单的API
  - [x] 基于JWE的鉴权（测试已通过）
  - [ ] 文档
    - [ ] `code` 与 `info`
  - [ ] Pydantic 错误的个性化定制
- [ ] `Markdown` 支持
  - [ ] 渲染
  - [ ] 链接渲染
- [ ] 文件上传以及下载功能
  - [ ] 多媒体内容的存取
    - [ ] Rickroll
  - [ ] 断点续传
- [ ] 个人主页
  - [ ] 头像
  - [ ] 动态（基于UserPosts）
  - [ ] 账号冻结
  - [ ] 注销导出数据
- [ ] 简单分类的话题/节点结构
  - [x] 相对应的表
  - [ ] 业务逻辑部分
- [ ] 用户日志功能（计划采用 NoSQL 数据存储）
- [ ] 管理业务
 - [ ] 后台界面
 - [ ] 管理员面板
