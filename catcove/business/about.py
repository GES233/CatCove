from datetime import datetime
from ..models.schemas.response import OriginData
from ..models.schemas.response.announcement import Anouncement

about_content=[
"# 关于本站",
"`CatCove` 是一个轻量且自由的论坛网站，它基于 `Sanic` 来运行并且\
仅保留了部分最基本的功能，因此其运行速度不会很慢。",
"## 请填写标题", "请填写内容"
]

def about_model():
   return OriginData(
    content_type="anouncement",
    detail=Anouncement(
        title="关于",
        author="Administrator",
        timestamp=datetime(2022, 8, 10, 6, 22, 30),
        content=about_content
    )
)