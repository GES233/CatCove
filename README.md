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
  - click
- Pico.css
- SimpleMDE/raw-text (Optional)

### 代码

```bash
pip install requirements.txt
python server.py
```

## TODO

### 原始内容

暂略。

### 何时与 `master` 合并？

直到完成如下内容：

- [ ] 完整的注册/登录流程
  - [x] 页面渲染（网页段）
  - [ ] 数据库提交流程
  - [ ] 表单提交以及前端的检查（`WTForms`）
  - [ ] 后端的检查（`Pydantic`）
  - [ ] Cookie 以及 Token 的加密解密
    - [ ] Base64
    - [ ] 非对称加密
- [ ] API端按照协议渲染自定义错误
  - `{"code": code, "info": info, "org": {...}}`
- [ ] 网页渲染端能够根据 Cookie 的内容返回用户信息
- [ ] 进一步的完成「干净化」