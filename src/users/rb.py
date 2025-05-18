from pydantic import EmailStr
class RBUser:
    def __init__(self, id: int | None = None,
                 username: str | None = None,
                 email: EmailStr | None = None):
        self.id = id
        self.username = username
        self.email = email
        
    def to_dict(self) -> dict:
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        filtered_date = {key: value for key, value in data.items() if value is not None}
        return filtered_date