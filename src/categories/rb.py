class RBCategory:
    def __init__(self, id: int | None = None,
                 name: str | None = None,
                 color: int | None = None):
        self.id = id
        self.name = name
        self.color = color
    
    def to_dict(self) -> dict:
        data = {"id": self.id, "name":self.name, "color": self.color}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data