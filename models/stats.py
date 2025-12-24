"""Stats model."""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base


class Stats(Base):
    """Stats model representing user statistics."""
    
    __tablename__ = "stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    knowledge = Column(Integer, default=0)
    guts = Column(Integer, default=0)
    proficiency = Column(Integer, default=0)
    kindness = Column(Integer, default=0)
    charm = Column(Integer, default=0)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="stats")
    
    STAT_NAMES = ["knowledge", "guts", "proficiency", "kindness", "charm"]
    MAX_STAT = 100  # Max value for each stat
    
    def __repr__(self):
        return f"<Stats(user_id={self.user_id}, K={self.knowledge}, G={self.guts}, P={self.proficiency}, Ki={self.kindness}, C={self.charm})>"
    
    def get_stat(self, stat_name: str) -> int:
        """Get stat value by name."""
        return getattr(self, stat_name.lower(), 0)
    
    def increase_stat(self, stat_name: str, amount: int = 1) -> bool:
        """Increase a stat by amount. Returns True if stat was increased."""
        stat_name = stat_name.lower()
        if stat_name not in self.STAT_NAMES:
            return False
        
        current_value = getattr(self, stat_name, 0)
        new_value = min(self.MAX_STAT, current_value + amount)
        setattr(self, stat_name, new_value)
        return new_value > current_value
    
    def get_total_stats(self) -> int:
        """Get sum of all stats."""
        return sum([
            self.knowledge,
            self.guts,
            self.proficiency,
            self.kindness,
            self.charm
        ])
    
    def get_stat_percentage(self, stat_name: str) -> float:
        """Get stat as percentage of max."""
        value = self.get_stat(stat_name)
        return (value / self.MAX_STAT) * 100

