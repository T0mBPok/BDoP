class RBImage:
    def __init__(self, id: int | None = None):
        self.id = id
        
    def to_dict(self) -> dict:
        data = {"id": self.id}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data