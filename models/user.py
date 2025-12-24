"""User model."""
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    """User model representing a Phantom Thief."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    total_exp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    palaces = relationship("Palace", back_populates="user", cascade="all, delete-orphan")
    stats = relationship("Stats", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', level={self.level})>"
    
    def add_exp(self, amount: int):
        """Add experience points and level up if needed."""
        self.total_exp += amount
        # Level up every 100 EXP
        new_level = (self.total_exp // 100) + 1
        if new_level > self.level:
            self.level = new_level
            return True  # Leveled up
        return False

