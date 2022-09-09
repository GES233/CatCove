from ..entities.tables.contents.posts import UserPosts


class UserPostsService:
    def __init__(self, post: UserPosts, status: dict | None = None) -> None:
        ...
