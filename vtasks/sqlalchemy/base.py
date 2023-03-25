from sqlalchemy.orm import registry
from sqlalchemy import MetaData


metadata = MetaData()
mapper_registry = registry(metadata=metadata)
