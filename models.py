import uuid
from enum import Enum
from db import Base
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Integer,
    Text,
    Time,
    ForeignKey,
    DateTime,
    Date,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    """Пользователи"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = Column(BigInteger, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    pin_code = Column(String, unique=True, nullable=False)
    admin_rule = Column(Boolean, nullable=False, default=False)


class CompanyInfo(Base):
    """Информация о компании"""

    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text)
    file_path = Column(Text)
    image_path = Column(Text)


class FAQ(Base):
    """Вопросы и ответы"""

    __tablename__ = "faq"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(Text, nullable=True)

    keywords = relationship(
        "FAQKeyWords", back_populates="faq", cascade="all, delete-orphan"
    )


class FAQKeyWords(Base):
    """Ключевые слова к вопросу"""

    __tablename__ = "faq_keywords"

    id = Column(Integer, primary_key=True)
    faq_id = Column(Integer, ForeignKey("faq.id"), nullable=False)
    word = Column(Text, nullable=False)

    faq = relationship("FAQ", back_populates="keywords")


class Feedback(Base):
    """Отзывы о боте"""

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    text = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)

    attachments = relationship(
        "FeedbackAttachments", back_populates="feedback", cascade="all, delete-orphan"
    )


class FeedbackAttachments(Base):
    """Вложения к отзыву о боте"""

    __tablename__ = "feedback_attachments"

    id = Column(Integer, primary_key=True)
    feedback_id = Column(
        Integer,
        ForeignKey("feedback.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_id = Column(Text)

    feedback = relationship(
        "Feedback", back_populates="attachments", passive_deletes=True
    )


class RegistrationRequest(Base):
    __tablename__ = "registration_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)


class VirtualExcursion(Base):
    __tablename__ = "virtual_excursions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    materials = relationship(
        "ExcursionMaterial", back_populates="excursion", cascade="all, delete-orphan"
    )


class ExcursionMaterial(Base):
    __tablename__ = "excursion_materials"

    id = Column(Integer, primary_key=True)
    excursion_id = Column(
        Integer, ForeignKey("virtual_excursions.id", ondelete="CASCADE"), nullable=False
    )
    telegram_file_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=True)

    excursion = relationship("VirtualExcursion", back_populates="materials")


class OrganizationalStructure(Base):
    """Организационная структура компании"""

    __tablename__ = "organizational_structure"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text)
    file_id = Column(Text)


class Canteen(Base):
    """Информация о столовой"""

    __tablename__ = "canteen"
    id = Column(Integer, primary_key=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    description = Column(Text, nullable=True)


class CanteenMenu(Base):
    """Меню столовой"""

    __tablename__ = "canteen_menu"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    file_id = Column(String)
    file_type = Column(String)
    menu = Column(Text)


class CanteenMenuFileType(str, Enum):
    PHOTO = "PHOTO"
    FILE = "FILE"


class Guide(Base):
    """Руководство по оформлению документов"""

    __tablename__ = "guides"

    id = Column(Integer, primary_key=True)
    document = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    text = Column(Text)
    file_id = Column(Text)
