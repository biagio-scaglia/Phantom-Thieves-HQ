"""Main game loop and state management."""
from sqlalchemy.orm import Session
from models.user import User
from models.task import Task, TaskStatus, TaskCategory, TaskDifficulty
from models.palace import Palace
from core.stats_engine import StatsEngine
from core.palace_engine import PalaceEngine
from datetime import date, datetime
from typing import Optional


class GameState:
    """Main game state manager."""
    
    def __init__(self, db: Session):
        self.db = db
        self.current_user: Optional[User] = None
    
    def create_user(self, username: str) -> User:
        """Create a new user."""
        user = User(username=username)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Initialize stats
        StatsEngine.get_or_create_stats(self.db, user.id)
        
        self.current_user = user
        return user
    
    def load_user(self, username: str) -> Optional[User]:
        """Load an existing user."""
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            self.current_user = user
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_task(
        self,
        title: str,
        category: str,
        difficulty: str,
        description: str = "",
        deadline: Optional[date] = None
    ) -> Task:
        """Create a new task."""
        if not self.current_user:
            raise ValueError("No user loaded")
        
        task = Task(
            user_id=self.current_user.id,
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            deadline=deadline
        )
        
        task.calculate_exp_reward()
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def complete_task(self, task_id: int) -> dict:
        """Complete a task and update stats/exp."""
        if not self.current_user:
            raise ValueError("No user loaded")
        
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == self.current_user.id
        ).first()
        
        if not task:
            raise ValueError("Task not found")
        
        if task.status == TaskStatus.COMPLETED.value:
            return {"message": "Task already completed"}
        
        # Complete task
        task.complete()
        
        # Process stats
        stats_result = StatsEngine.process_task_completion(self.db, task)
        
        # Add EXP to user
        leveled_up = self.current_user.add_exp(task.exp_reward)
        
        # Update palace progress
        palaces = PalaceEngine.get_active_palaces(self.db, self.current_user.id)
        for palace in palaces:
            PalaceEngine.update_palace_progress(self.db, palace)
        
        self.db.commit()
        self.db.refresh(self.current_user)
        
        return {
            "task": task.title,
            "exp_gained": task.exp_reward,
            "stat_boost": stats_result,
            "leveled_up": leveled_up,
            "new_level": self.current_user.level if leveled_up else None
        }
    
    def create_palace(
        self,
        name: str,
        description: str = "",
        boss_name: str = "",
        deadline: Optional[date] = None
    ) -> Palace:
        """Create a new palace."""
        if not self.current_user:
            raise ValueError("No user loaded")
        
        palace = Palace(
            user_id=self.current_user.id,
            name=name,
            description=description,
            boss_name=boss_name,
            deadline=deadline
        )
        
        self.db.add(palace)
        self.db.commit()
        self.db.refresh(palace)
        
        return palace
    
    def get_pending_tasks(self) -> list[Task]:
        """Get all pending tasks for current user."""
        if not self.current_user:
            return []
        
        return self.db.query(Task).filter(
            Task.user_id == self.current_user.id,
            Task.status == TaskStatus.PENDING.value
        ).order_by(Task.deadline.asc()).all()
    
    def get_overdue_tasks(self) -> list[Task]:
        """Get all overdue tasks."""
        if not self.current_user:
            return []
        
        tasks = self.get_pending_tasks()
        return [task for task in tasks if task.is_overdue()]
    
    def get_user_stats(self):
        """Get current user stats."""
        if not self.current_user:
            return None
        
        stats = StatsEngine.get_or_create_stats(self.db, self.current_user.id)
        return StatsEngine.get_stats_summary(stats)

