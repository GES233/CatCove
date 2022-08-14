# CatCove

基于话题的小论坛（目前进度10%）。

## Install

### 依赖项

- Python
  - Sanic
  - SQLAlchemy
  - alembic
  - Pydantic
  - PyJWT
  - ujson
  - Jinja2
  - WTForms
  - PyYAML
- Pico.css
- SimpleMDE/raw-text (Optional)

### 代码

```bash
pip install requirements.txt
python server.py
```

## TODO

- [x] 数据库
- [x] 重构——业务代码与API的解耦
  - [x] 代码优化 (能力极限)
- [x] 前端美化框架（`Pico.css`）
  - [ ] 再美化（
- [ ] 自动在安装时完成运行添加示例（基于Mako+click）
- [x] 简单的API
  - [ ] 基于JWT的鉴权
  - [ ] 添加code与response
  - [ ] 文档
- [ ] `Markdown` 支持
  - [ ] 渲染
- [ ] 个人主页
  - [ ] 头像
  - [ ] 动态（基于UserPosts）
- [ ] 简单分类的话题/节点结构
