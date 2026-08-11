from sqlalchemy import Column, Integer, String
from database import Base


class APIConfig(Base):
    __tablename__ = "api_configs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    endpoint = Column(String)
    timeout = Column(Integer, default=30)
    auth_type = Column(String)
    rate_limit = Column(Integer)
