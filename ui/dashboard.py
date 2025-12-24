"""Dashboard UI with Rich."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich.text import Text
from assets.ascii_art import SOCIAL_STATS
from typing import Optional, Dict, List
from models.user import User
from models.task import Task
from models.palace import Palace


class Dashboard:
    """Main dashboard display."""
    
    def __init__(self):
        self.console = Console()
    
    def display_welcome(self):
        """Display welcome screen."""
        from assets.ascii_art import JOKER_LOGO, WELCOME_MESSAGE
        
        self.console.print(Panel(
            JOKER_LOGO + "\n" + WELCOME_MESSAGE,
            border_style="bright_red",
            title="[bold red]PHANTOM THIEVES HQ[/bold red]"
        ))
    
    def display_user_profile(self, user: User, stats: Optional[Dict] = None):
        """Display user profile information."""
        profile_table = Table(title="👤 Profile", show_header=True, header_style="bold magenta")
        profile_table.add_column("Attribute", style="cyan")
        profile_table.add_column("Value", style="green")
        
        profile_table.add_row("Username", user.username)
        profile_table.add_row("Level", str(user.level))
        profile_table.add_row("Total EXP", str(user.total_exp))
        exp_to_next = max(0, (user.level * 100) - user.total_exp)
        profile_table.add_row("EXP to Next Level", str(exp_to_next))
        
        if stats:
            profile_table.add_row("Total Stats", str(stats.get("Total", 0)))
        
        self.console.print(profile_table)
    
    def display_stats(self, stats: Dict):
        """Display statistics with progress bars."""
        stats_table = Table(title="📊 Statistics", show_header=True, header_style="bold blue")
        stats_table.add_column("Stat", style="cyan", width=15)
        stats_table.add_column("Value", style="green", width=10)
        stats_table.add_column("Progress", width=30)
        stats_table.add_column("Rank", style="yellow", width=12)
        
        from core.stats_engine import StatsEngine
        
        for stat_name, value in stats.items():
            if stat_name == "Total":
                continue
            
            # Progress bar
            progress_bar = self._create_progress_bar(value, 100)
            
            # Rank
            rank = StatsEngine.get_stat_rank(value)
            
            # Icon
            icon = SOCIAL_STATS.get(stat_name, "📊")
            
            stats_table.add_row(
                f"{icon} {stat_name}",
                str(value),
                progress_bar,
                rank
            )
        
        self.console.print(stats_table)
    
    def _create_progress_bar(self, value: int, max_value: int) -> str:
        """Create a text progress bar."""
        percentage = (value / max_value) * 100
        bar_length = 20
        filled = int((value / max_value) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        return f"{bar} {percentage:.1f}%"
    
    def display_tasks(self, tasks: List[Task], title: str = "📋 Tasks"):
        """Display list of tasks."""
        if not tasks:
            self.console.print(f"[yellow]No {title.lower()} found.[/yellow]")
            return
        
        tasks_table = Table(title=title, show_header=True, header_style="bold green")
        tasks_table.add_column("ID", style="cyan", width=5)
        tasks_table.add_column("Title", style="white", width=30)
        tasks_table.add_column("Category", style="blue", width=12)
        tasks_table.add_column("Difficulty", style="yellow", width=10)
        tasks_table.add_column("Status", style="magenta", width=12)
        tasks_table.add_column("Deadline", style="red", width=12)
        tasks_table.add_column("EXP", style="green", width=8)
        
        for task in tasks:
            status_style = {
                "pending": "[yellow]Pending[/yellow]",
                "in_progress": "[blue]In Progress[/blue]",
                "completed": "[green]Completed[/green]",
                "cancelled": "[red]Cancelled[/red]"
            }.get(task.status, task.status)
            
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
            
            if task.is_overdue():
                deadline_str = f"[red]{deadline_str} ⚠️[/red]"
            
            tasks_table.add_row(
                str(task.id),
                task.title[:28] + "..." if len(task.title) > 28 else task.title,
                task.category,
                task.difficulty,
                status_style,
                deadline_str,
                str(task.exp_reward)
            )
        
        self.console.print(tasks_table)
    
    def display_palaces(self, palaces: List[Palace], title: str = "🏯 Palaces"):
        """Display list of palaces."""
        if not palaces:
            self.console.print(f"[yellow]No {title.lower()} found.[/yellow]")
            return
        
        palaces_table = Table(title=title, show_header=True, header_style="bold red")
        palaces_table.add_column("ID", style="cyan", width=5)
        palaces_table.add_column("Name", style="white", width=25)
        palaces_table.add_column("Infiltration", style="blue", width=15)
        palaces_table.add_column("Boss", style="yellow", width=20)
        palaces_table.add_column("Deadline", style="red", width=12)
        palaces_table.add_column("Status", style="magenta", width=12)
        
        for palace in palaces:
            infiltration_bar = self._create_progress_bar(
                int(palace.infiltration_percentage),
                100
            )
            
            deadline_str = palace.deadline.strftime("%Y-%m-%d") if palace.deadline else "No deadline"
            days_remaining = palace.days_remaining()
            
            if days_remaining is not None:
                deadline_str += f" ({days_remaining}d left)"
            
            if palace.is_overdue():
                deadline_str = f"[red]{deadline_str} ⚠️[/red]"
            
            status_style = {
                "active": "[green]Active[/green]",
                "completed": "[blue]Completed[/blue]",
                "abandoned": "[red]Abandoned[/red]"
            }.get(palace.status, palace.status)
            
            palaces_table.add_row(
                str(palace.id),
                palace.name[:23] + "..." if len(palace.name) > 23 else palace.name,
                f"{palace.infiltration_percentage:.1f}% {infiltration_bar}",
                palace.boss_name[:18] + "..." if palace.boss_name and len(palace.boss_name) > 18 else (palace.boss_name or "Unknown"),
                deadline_str,
                status_style
            )
        
        self.console.print(palaces_table)
    
    def display_completion_message(self, result: Dict):
        """Display task completion message."""
        message = f"""
[bold green]✅ Task Completed![/bold green]

Task: {result['task']}
EXP Gained: {result['exp_gained']}
Stat Boost: {result['stat_boost']['stat'].title()} +{result['stat_boost']['amount']}
New {result['stat_boost']['stat'].title()} Value: {result['stat_boost']['new_value']}
"""
        
        if result.get('leveled_up'):
            message += f"\n[bold yellow]🎉 LEVEL UP! You are now Level {result['new_level']}![/bold yellow]"
        
        self.console.print(Panel(message, border_style="green", title="[bold green]Mission Complete[/bold green]"))
    
    def display_error(self, message: str):
        """Display error message."""
        self.console.print(f"[bold red]❌ Error:[/bold red] {message}")
    
    def display_success(self, message: str):
        """Display success message."""
        self.console.print(f"[bold green]✅ {message}[/bold green]")
    
    def display_info(self, message: str):
        """Display info message."""
        self.console.print(f"[bold blue]ℹ️ {message}[/bold blue]")

