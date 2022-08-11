# CatCove

基于话题的小论坛（目前进度5%）。

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

### 代码

```bash
pip install requirements.txt
python server.py
```

## TODO

- [x] 数据库
- [x] 重构——业务代码与API的解耦
  -[ ] 代码优化
- [x] 前端美化框架（`Pico.css`）
  - [ ] 再美化（
- [ ] 自动在安装时完成运行添加示例（基于Mako+click）
- [x] 简单的API
  - [ ] 基于JWT的鉴权
  - [ ] 添加code与response
  - [ ] 文档
- [ ] `Markdown` 支持
