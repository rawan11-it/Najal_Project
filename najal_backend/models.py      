"""
najal_backend/models.py
----------------------------
جداول قاعدة البيانات.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base   # بدون نقطة لأن الملفات بنفس المجلد


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("role IN ('citizen','farmer','municipality')", name="valid_role"),
    )

    reports = relationship("TreeReport", back_populates="citizen")
    planted_trees = relationship("PlantedTree", back_populates="user")


class Neighborhood(Base):
    __tablename__ = "neighborhoods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    avg_temperature_c = Column(Float)
    soil_type = Column(String)
    tree_priority = Column(String)


class TreeReport(Base):
    __tablename__ = "tree_reports"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    status = Column(String, default="pending", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    citizen = relationship("User", back_populates="reports")


class PlantedTree(Base):
    __tablename__ = "planted_trees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tree_type = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    points_earned = Column(Integer, default=10, nullable=False)
    planted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="planted_trees")