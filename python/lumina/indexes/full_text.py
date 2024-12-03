import uuid
import lancedb
from pydantic import BaseModel
from typing import Type


class Document(BaseModel):

    id: str = uuid.uuid4()
    content: str

class FullTextIndexer(BaseModel):

    db_path: str = "full_text.lancedb"
    table_name: str = "documents"

    def __init__(self, **data):

        super().__init__(**data)
        self.db = lancedb.connect(self.db_path)
        self._create_table()

    def _create_table(self):

        if self.table_name not in self.db.tables:
            self.db.create_table(self.table_name, {
                "id": 
            })