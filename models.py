from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)


class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('nodes.id'), nullable=True)
    is_approved = Column(Boolean, default=False)
    children = relationship('Node')
    audits = relationship('Audit', back_populates='node')


class Audit(Base):
    __tablename__ = "audits"
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer, ForeignKey('nodes.id'))
    action = Column(String)
    node = relationship('Node', back_populates='audits')
