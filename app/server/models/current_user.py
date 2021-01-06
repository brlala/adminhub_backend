from pydantic import BaseModel


class CurrentUserSchema(BaseModel):
    username: str
    userId: str
    permissions: list[str]
    name: str
    email: str
    avatar: str
    is_active: bool

    class Config:
        schema_extra = {
            "username": "user@pand.ai",
            "userId": "5efdc63e74f7e093ce73db78",
            "access": "admin",
            "permissions": [
                "create_flow",
                "read_flow",
            ],
            "name": "Teh Li heng ",
            "email": "liheng@pand.ai",
            "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
            "is_active": True
        }
