"""Palace model."""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import date
from enum import Enum


class PalaceStatus(str, Enum):
    """Palace status enum."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Palace(Base):
    """Palace model representing a major goal."""
    
    __tablename__ = "palaces"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    infiltration_percentage = Column(Float, default=0.0)
    boss_name = Column(String)  # Final milestone name
    deadline = Column(Date)
    status = Column(String, default=PalaceStatus.ACTIVE)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="palaces")
    
    def __repr__(self):
        return f"<Palace(id={self.id}, name='{self.name}', infiltration={self.infiltration_percentage}%)>"
    
    def update_infiltration(self, percentage: float):
        """Update infiltration percentage (0-100)."""
        self.infiltration_percentage = min(100.0, max(0.0, percentage))
        if self.infiltration_percentage >= 100.0:
            self.complete()
    
    def complete(self):
        """Mark palace as completed."""
        from datetime import datetime
        self.status = PalaceStatus.COMPLETED
        self.infiltration_percentage = 100.0
        self.completed_at = datetime.now()
    
    def days_remaining(self) -> int:
        """Calculate days remaining until deadline."""
        if self.deadline:
            delta = self.deadline - date.today()
            return max(0, delta.days)
        return None
    
    def is_overdue(self) -> bool:
        """Check if palace deadline has passed."""
        if self.deadline and self.status == PalaceStatus.ACTIVE:
            return date.today() > self.deadline
        return False

