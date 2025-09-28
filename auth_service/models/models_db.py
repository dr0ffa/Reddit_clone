import uuid
from auth_service.models.database import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Mfa(Base):
    __tablename__ = "mfa"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)     
    secret = Column(String, nullable=True)      
    enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="mfa")

Base.metadata.create_all(bind=engine)

