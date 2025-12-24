"""Example usage script for Phantom Thieves HQ."""
"""
This script demonstrates how to use the Phantom Thieves HQ system programmatically.
Run this to see the system in action without the interactive UI.
"""
from db.database import init_db, SessionLocal
from core.game_loop import GameState
from models.task import TaskCategory, TaskDifficulty
from datetime import date, timedelta
from rich.console import Console
from rich.panel import Panel

console = Console()


def example_usage():
    """Run example usage."""
    console.print(Panel(
        "[bold cyan]Phantom Thieves HQ - Example Usage[/bold cyan]\n"
        "This script demonstrates the core functionality.",
        border_style="cyan"
    ))
    
    # Initialize database
    init_db()
    db = SessionLocal()
    game_state = GameState(db)
    
    # Create a test user
    console.print("\n[bold green]1. Creating user...[/bold green]")
    user = game_state.create_user("Joker")
    console.print(f"✅ Created user: {user.username} (Level {user.level})")
    
    # Create some tasks
    console.print("\n[bold green]2. Creating tasks...[/bold green]")
    
    tasks_data = [
        {
            "title": "Learn SQLAlchemy",
            "category": TaskCategory.KNOWLEDGE.value,
            "difficulty": TaskDifficulty.MEDIUM.value,
            "description": "Study SQLAlchemy ORM",
            "deadline": date.today() + timedelta(days=7)
        },
        {
            "title": "Build Portfolio Website",
            "category": TaskCategory.PROFICIENCY.value,
            "difficulty": TaskDifficulty.HARD.value,
            "description": "Create a professional portfolio",
            "deadline": date.today() + timedelta(days=30)
        },
        {
            "title": "Network at Tech Meetup",
            "category": TaskCategory.CHARM.value,
            "difficulty": TaskDifficulty.MEDIUM.value,
            "description": "Attend local tech meetup",
            "deadline": date.today() + timedelta(days=14)
        }
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        task = game_state.create_task(**task_data)
        created_tasks.append(task)
        console.print(f"✅ Created task: {task.title} ({task.category}, {task.difficulty})")
    
    # Complete some tasks
    console.print("\n[bold green]3. Completing tasks...[/bold green]")
    for task in created_tasks[:2]:  # Complete first 2 tasks
        result = game_state.complete_task(task.id)
        console.print(f"✅ Completed: {result['task']}")
        console.print(f"   EXP Gained: {result['exp_gained']}")
        console.print(f"   Stat Boost: {result['stat_boost']['stat']} +{result['stat_boost']['amount']}")
        if result.get('leveled_up'):
            console.print(f"   🎉 LEVEL UP! Now Level {result['new_level']}!")
    
    # Create a palace
    console.print("\n[bold green]4. Creating palace...[/bold green]")
    palace = game_state.create_palace(
        name="Master Python Development",
        description="Become an expert Python developer",
        boss_name="Complete 10 Python Projects",
        deadline=date.today() + timedelta(days=180)
    )
    console.print(f"✅ Created palace: {palace.name}")
    console.print(f"   Boss: {palace.boss_name}")
    
    # Show stats
    console.print("\n[bold green]5. Current Statistics:[/bold green]")
    stats = game_state.get_user_stats()
    from core.stats_engine import StatsEngine
    stats_summary = StatsEngine.get_stats_summary(
        StatsEngine.get_or_create_stats(db, user.id)
    )
    
    for stat_name, value in stats_summary.items():
        if stat_name != "Total":
            rank = StatsEngine.get_stat_rank(value)
            console.print(f"   {stat_name}: {value} ({rank})")
    
    # Show user info
    console.print("\n[bold green]6. User Summary:[/bold green]")
    console.print(f"   Username: {user.username}")
    console.print(f"   Level: {user.level}")
    console.print(f"   Total EXP: {user.total_exp}")
    
    # Show palace progress
    from core.palace_engine import PalaceEngine
    active_palaces = PalaceEngine.get_active_palaces(db, user.id)
    if active_palaces:
        console.print("\n[bold green]7. Palace Progress:[/bold green]")
        for palace in active_palaces:
            console.print(f"   {palace.name}: {palace.infiltration_percentage:.1f}%")
    
    db.close()
    console.print("\n[bold cyan]✅ Example completed![/bold cyan]")
    console.print("[dim]Run 'python app.py' to use the interactive UI.[/dim]")


if __name__ == "__main__":
    example_usage()

