# Server-sent events support

## 一些量

- 后端路由地址（在`/catcove/static/js/sse_client.js`与`/catcove/services/stream.py`中）： `/subcribe`
- 结束通信的事件标识： `"event: close"`
- 重试时间（由应用的配置所决定）：15s / 1500ms
- 确定用户的方法
  - 从Cookie/Token所获得的payload（`request.ctx.current_user`）
  - 需要的部分（`payload["id"]`）

### 关于业务的量
