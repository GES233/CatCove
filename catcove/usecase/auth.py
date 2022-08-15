from Crypto.PublicKey import ECC


class AuthService:
    def __init__(
        self,
        token: str | None = None,
        cookie: str | None = None,
        status: dict | None = None
    ) -> None:
        if token:
            self.token = token
            self.cookie = None
        elif cookie:
            self.token = None
            self.cookie = cookie
        else: self.token = self.cookie = None

        if status:
            self.service_status = status
        else:
            self.service_status = {
                "config": {},
                "errors": []
            }
        
        self.raw: str = ""
        self.payload: dict = {}
    
    def encrypt(self) -> bool:
        if self.token:
            self.raw = self.token
        elif self.cookie:
            self.raw = self.cookie
        return True
    
    def decrypt(self) -> bool:
        if not self.raw: return False
        self.token = ...
        self.cookie = ...
        return True
    
    def str_to_dict(self) -> bool:
        if not self.raw:
            # Not encrypted.
            ...
            return False
        
        _dict = eval(self.raw)

        if not isinstance(_dict, dict):
            # Not a dict.
            ...
            return False

        self.payload = _dict
        return True
    
    def dict_to_str(self) -> bool:
        if not self.payload: return False
        self.raw = self.payload.__str__()
        return True
