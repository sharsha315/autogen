from sqlmodel import SQLModel, Session, create_engine, select, delete, and_
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DBManager:
    """ A class to manage database operations"""

    def __init__(self, engine_uri: str):
        self.engine = create_engine(engine_uri)
        self.session = Session(self.engine)

    def create_db_and_tables(self):
        """ Create a new database and tables """
        SQLModel.metadata.create_all(self.engine)

    def upsert(self, model: SQLModel):
        """ Create a new entity"""
        # check if the model exists, update else add
        model_class = type(model)
        current_model = self.session.exec(
            select(model_class).where(model_class.id == model.id)).first()
        if current_model:
            model.updated_at = datetime.now()
            for key, value in model.model_dump().items():
                setattr(current_model, key, value)
            self.session.add(current_model)
        else:
            self.session.add(model)
        self.session.commit()
        status_message = "Item Updated Successfully " if current_model else "Item Added Successfully"
        return status_message

    def _model_to_dict(self, model_obj):
        return {col.name: getattr(model_obj, col.name) for col in model_obj.__table__.columns}

    def get(self, model_class: SQLModel, filters: dict = None, return_json: bool = False):
        """ List all entities for a user"""
        if filters:
            conditions = [getattr(model_class, col) ==
                          value for col, value in filters.items()]
            statement = select(model_class).where(and_(*conditions))
        else:
            statement = select(model_class)
        if return_json:
            return [self._model_to_dict(row) for row in self.session.exec(statement).all()]
        else:
            return self.session.exec(statement).all()

    def delete(self, model_class: SQLModel, filters: dict = None):
        """ Delete an entity"""
        row = None
        status_message = ""
        if filters:
            conditions = [getattr(model_class, col) ==
                          value for col, value in filters.items()]
            row = self.session.exec(
                select(model_class).where(and_(*conditions))).all()
        else:
            row = self.session.exec(select(model_class)).all()
        if row:
            for row in row:
                self.session.delete(row)
            self.session.commit()
            status_message = "Deleted Successfully"
        else:
            print(f"Row with filters {filters} not found")
            logger.info("Row with filters %s not found", filters)
            status_message = "Row not found"
        return status_message