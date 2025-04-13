class RBProject:
    def __init__(self, id: int | None = None,
                 name: str | None = None,
                 category_color: str | None = None):
        self.id = id
        self.name = name
        self.category_color = category_color
    
    def to_dict(self) -> dict:
        data = {"id": self.id, "name":self.name, "category_color": self.category_color}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data