"""Palace engine for managing major goals."""
from models.palace import Palace, PalaceStatus
from models.task import Task, TaskStatus
from sqlalchemy.orm import Session
from sqlalchemy import func


class PalaceEngine:
    """Engine for managing Palace progression."""
    
    @staticmethod
    def calculate_infiltration(db: Session, palace: Palace) -> float:
        """Calculate infiltration percentage based on related tasks."""
        # Get all tasks for the user
        user_tasks = db.query(Task).filter(
            Task.user_id == palace.user_id,
            Task.status == TaskStatus.COMPLETED.value
        ).all()
        
        # Simple calculation: each completed task adds a small percentage
        # This can be customized based on task difficulty or category
        base_infiltration = len(user_tasks) * 0.5  # 0.5% per completed task
        
        # Cap at 100%
        infiltration = min(100.0, base_infiltration)
        
        return infiltration
    
    @staticmethod
    def update_palace_progress(db: Session, palace: Palace):
        """Update palace infiltration percentage."""
        infiltration = PalaceEngine.calculate_infiltration(db, palace)
        palace.update_infiltration(infiltration)
        db.commit()
        db.refresh(palace)
    
    @staticmethod
    def get_palace_status(palace: Palace) -> dict:
        """Get formatted palace status."""
        days_remaining = palace.days_remaining()
        
        status_info = {
            "name": palace.name,
            "infiltration": f"{palace.infiltration_percentage:.1f}%",
            "status": palace.status,
            "deadline": palace.deadline.strftime("%Y-%m-%d") if palace.deadline else "No deadline",
            "days_remaining": days_remaining if days_remaining is not None else "N/A",
            "boss": palace.boss_name or "Unknown"
        }
        
        if palace.is_overdue():
            status_info["warning"] = "⚠️ OVERDUE"
        
        return status_info
    
    @staticmethod
    def get_active_palaces(db: Session, user_id: int) -> list[Palace]:
        """Get all active palaces for a user."""
        return db.query(Palace).filter(
            Palace.user_id == user_id,
            Palace.status == PalaceStatus.ACTIVE
        ).all()
    
    @staticmethod
    def get_completed_palaces(db: Session, user_id: int) -> list[Palace]:
        """Get all completed palaces for a user."""
        return db.query(Palace).filter(
            Palace.user_id == user_id,
            Palace.status == PalaceStatus.COMPLETED
        ).all()

