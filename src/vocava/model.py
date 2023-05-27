import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

user_language_table = Table(
    'user_language', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('language_id', Integer, ForeignKey('languages.id'), primary_key=True),
)

user_conversation_table = Table(
    'user_conversation', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column(
        'conversation_id', Integer, ForeignKey('conversations.id'), primary_key=True
    ),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship('Language')
    participants = relationship('User', secondary=user_conversation_table)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    conversation = relationship('Conversation')
