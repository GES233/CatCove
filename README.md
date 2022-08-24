# CatCove

基于话题的小~~论坛~~SNS（目前进度12%）。

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

- [ ] 完善的测试代码
- [ ] 消息机制的引入
  - [ ] APSchedule
  - [ ] 类似于 Flask 的 `flash()` （No-JS）
  - [ ] ESS 的实现（需要JS）
- [ ] HTML模板的调整
- [x] 前端美化框架（`Pico.css`）
  - [ ] 再美化（CSS reliable）
- [x] 简单的API
  - [ ] 基于JWE的鉴权
  - [x] 添加code与response（`Tiny`）
  - [ ] 文档
- [ ] `Markdown` 支持
  - [ ] 渲染
- [ ] 个人主页
  - [ ] 头像
  - [ ] 动态（基于UserPosts）
  - [ ] 账号冻结
  - [ ] 注销导出数据
- [ ] 简单分类的话题/节点结构
  - [ ] 相对应的表
  - [ ] 业务逻辑部分
