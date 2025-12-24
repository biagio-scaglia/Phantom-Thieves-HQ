"""Task model."""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import date
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enum."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskCategory(str, Enum):
    """Task category enum."""
    KNOWLEDGE = "Knowledge"
    GUTS = "Guts"
    PROFICIENCY = "Proficiency"
    KINDNESS = "Kindness"
    CHARM = "Charm"


class TaskDifficulty(str, Enum):
    """Task difficulty enum."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXTREME = "Extreme"


class Task(Base):
    """Task model representing a mission."""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    status = Column(String, default=TaskStatus.PENDING.value)
    exp_reward = Column(Integer, default=0)
    stat_boost = Column(String)  # Which stat this task boosts
    deadline = Column(Date)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    def calculate_exp_reward(self):
        """Calculate EXP reward based on difficulty."""
        exp_map = {
            TaskDifficulty.EASY.value: 10,
            TaskDifficulty.MEDIUM.value: 25,
            TaskDifficulty.HARD.value: 50,
            TaskDifficulty.EXTREME.value: 100
        }
        self.exp_reward = exp_map.get(self.difficulty, 10)
        return self.exp_reward
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.deadline and self.status != TaskStatus.COMPLETED.value:
            return date.today() > self.deadline
        return False
    
    def complete(self):
        """Mark task as completed."""
        from datetime import datetime
        self.status = TaskStatus.COMPLETED.value
        self.completed_at = datetime.now()
        if not self.exp_reward:
            self.calculate_exp_reward()

