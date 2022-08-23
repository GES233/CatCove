# CatCove

基于话题的小~~论坛~~SNS（目前进度10%）。

## Install

### 依赖项

- Python
  - Sanic
  - SQLAlchemy
  - alembic
  - Pydantic
  - BCrypt
  - PyJWT
  - ujson
  - Jinja2
  - WTForms
  - PyYAML
  - click
  - email_validator
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

### ROADMAP

#### 何时与 `master` 合并？

直到完成如下内容：

- [ ] 完整的注册/登录流程
  - [x] 页面渲染（网页段）
  - [x] 数据库提交流程
  - [x] 表单提交以及前端的检查（`WTForms`）
  - [ ] 后端的检查（`Pydantic`）并且能够在 API 端返回错误
  - [ ] Cookie 以及 Token 的加密解密
    - [ ] Base64
    - [ ] 非对称加密
- [x] API端按照协议渲染自定义错误
  - `{"code": code, "info": info, "org": {...}}`
- [ ] 网页渲染端能够根据 Cookie 的内容返回用户信息
  - [ ] Cookie/Token 的自动更新

完成了以上内容，算完成了25%。

#### 之后的计划

- [ ] 完善的测试代码
- [ ] 消息机制的引入
  - [ ] APSchedule
  - [ ] 类似于 Flask 的 `flash()` （No-JS）
  - [ ] ESS 的实现（需要JS）
