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
- [x] API
- [x] 重构——业务代码与API的解耦
- [x] 前端美化框架（`Pico.css`）
- [ ] 自动在安装时完成运行添加示例（基于Mako+click）
- [ ] 添加code与response
- [ ] 文档
