from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BIGINT
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PersonRepository(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    nameFirst = Column(String(100))
    nameLast = Column(String(100))
    nameMiddle = Column(String(100))
    nameExt = Column(String(100))
    contactTel = Column(String(100))
    contactMobile = Column(String(100))
    contactEmail = Column(String(100))
    # audit
    updatedAt = Column(BIGINT)
    updatedBy = Column(String(100))
    deletedAt = Column(BIGINT)
    deletedBy = Column(String(100))


# Create Tables
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
