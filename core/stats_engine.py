"""Stats engine for managing user statistics."""
from models.stats import Stats
from models.task import Task, TaskCategory
from sqlalchemy.orm import Session


class StatsEngine:
    """Engine for managing and calculating statistics."""
    
    STAT_BOOST_MAP = {
        TaskCategory.KNOWLEDGE.value: "knowledge",
        TaskCategory.GUTS.value: "guts",
        TaskCategory.PROFICIENCY.value: "proficiency",
        TaskCategory.KINDNESS.value: "kindness",
        TaskCategory.CHARM.value: "charm"
    }
    
    @staticmethod
    def get_or_create_stats(db: Session, user_id: int) -> Stats:
        """Get or create stats for a user."""
        stats = db.query(Stats).filter(Stats.user_id == user_id).first()
        if not stats:
            stats = Stats(user_id=user_id)
            db.add(stats)
            db.commit()
            db.refresh(stats)
        return stats
    
    @staticmethod
    def process_task_completion(db: Session, task: Task) -> dict:
        """Process task completion and update stats."""
        stats = StatsEngine.get_or_create_stats(db, task.user_id)
        
        # Determine which stat to boost
        stat_to_boost = StatsEngine.STAT_BOOST_MAP.get(task.category, "knowledge")
        
        # Calculate boost amount based on difficulty
        boost_amount = {
            "Easy": 1,
            "Medium": 2,
            "Hard": 3,
            "Extreme": 5
        }.get(task.difficulty, 1)
        
        # Increase stat
        increased = stats.increase_stat(stat_to_boost, boost_amount)
        
        # Update task stat_boost field
        task.stat_boost = stat_to_boost
        
        db.commit()
        db.refresh(stats)
        
        return {
            "stat": stat_to_boost,
            "amount": boost_amount,
            "new_value": stats.get_stat(stat_to_boost),
            "increased": increased
        }
    
    @staticmethod
    def get_stats_summary(stats: Stats) -> dict:
        """Get formatted stats summary."""
        return {
            "Knowledge": stats.knowledge,
            "Guts": stats.guts,
            "Proficiency": stats.proficiency,
            "Kindness": stats.kindness,
            "Charm": stats.charm,
            "Total": stats.get_total_stats()
        }
    
    @staticmethod
    def get_stat_rank(value: int) -> str:
        """Get rank name for stat value."""
        if value >= 90:
            return "MAX"
        elif value >= 70:
            return "Expert"
        elif value >= 50:
            return "Advanced"
        elif value >= 30:
            return "Intermediate"
        elif value >= 10:
            return "Beginner"
        else:
            return "Novice"

