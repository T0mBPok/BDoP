class RBSubtit:
    def __init__(self, id: int | None = None,
                 name: str | None = None,
                 category_color: int | None = None,
                 importance_color: int | None = None,
                 task_id: int | None = None):
        self.id = id
        self.name = name
        self.category_color = category_color
        self.importance_color = importance_color
        self.task_id = task_id
    
    def to_dict(self) -> dict:
        data = {"id": self.id, 
                "name":self.name, 
                "category_color": self.category_color, 
                "importance_color": self.importance_color,
                "task_id": self.task_id}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data