from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, List, Optional

ModelType = TypeVar('ModelType')
EntityType = TypeVar('EntityType')

class BaseRepository(Generic[ModelType, EntityType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get_all(self) -> List[EntityType]:
        models = self.db.query(self.model).all()
        return [m.to_entity() for m in models]

    def get_by_id(self, id: str) -> Optional[EntityType]:
        model = self.db.query(self.model).filter(self.model.id == id).first()
        return model.to_entity() if model else None

    def create(self, data: dict) -> EntityType:
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj.to_entity()

    def update(self, id: str, data: dict) -> Optional[EntityType]:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
            return obj.to_entity()
        return None

    def delete(self, id: str) -> bool:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
