"""Menu system with Rich."""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from datetime import datetime, date
from typing import Optional
from models.task import TaskCategory, TaskDifficulty
from models.palace import PalaceStatus


class MenuSystem:
    """Menu navigation system."""
    
    def __init__(self):
        self.console = Console()
    
    def main_menu(self) -> str:
        """Display main menu and get user choice."""
        menu_table = Table(title="Main Menu", show_header=False, box=None)
        menu_table.add_column("Option", style="cyan", width=3)
        menu_table.add_column("Action", style="white")
        
        menu_table.add_row("1", "📊 View Dashboard")
        menu_table.add_row("2", "📋 Manage Tasks")
        menu_table.add_row("3", "🏯 Manage Palaces")
        menu_table.add_row("4", "📈 View Analytics")
        menu_table.add_row("5", "⚙️  Settings")
        menu_table.add_row("0", "🚪 Exit")
        
        self.console.print(menu_table)
        
        choice = Prompt.ask(
            "\n[bold cyan]Select an option[/bold cyan]",
            choices=["0", "1", "2", "3", "4", "5"],
            default="1"
        )
        
        return choice
    
    def task_menu(self) -> str:
        """Display task management menu."""
        menu_table = Table(title="Task Management", show_header=False, box=None)
        menu_table.add_column("Option", style="cyan", width=3)
        menu_table.add_column("Action", style="white")
        
        menu_table.add_row("1", "➕ Create New Task")
        menu_table.add_row("2", "✅ Complete Task")
        menu_table.add_row("3", "📋 View All Tasks")
        menu_table.add_row("4", "⚠️  View Overdue Tasks")
        menu_table.add_row("0", "🔙 Back to Main Menu")
        
        self.console.print(menu_table)
        
        choice = Prompt.ask(
            "\n[bold cyan]Select an option[/bold cyan]",
            choices=["0", "1", "2", "3", "4"],
            default="1"
        )
        
        return choice
    
    def palace_menu(self) -> str:
        """Display palace management menu."""
        menu_table = Table(title="Palace Management", show_header=False, box=None)
        menu_table.add_column("Option", style="cyan", width=3)
        menu_table.add_column("Action", style="white")
        
        menu_table.add_row("1", "➕ Create New Palace")
        menu_table.add_row("2", "📋 View Active Palaces")
        menu_table.add_row("3", "🏆 View Completed Palaces")
        menu_table.add_row("0", "🔙 Back to Main Menu")
        
        self.console.print(menu_table)
        
        choice = Prompt.ask(
            "\n[bold cyan]Select an option[/bold cyan]",
            choices=["0", "1", "2", "3"],
            default="1"
        )
        
        return choice
    
    def get_task_input(self) -> dict:
        """Get task input from user."""
        self.console.print("\n[bold cyan]Create New Task[/bold cyan]")
        
        title = Prompt.ask("Task Title")
        description = Prompt.ask("Description (optional)", default="")
        
        # Category selection
        categories = [cat.value for cat in TaskCategory]
        category_table = Table(show_header=False, box=None)
        for i, cat in enumerate(categories, 1):
            category_table.add_row(str(i), cat)
        self.console.print(category_table)
        
        cat_choice = Prompt.ask(
            "Select Category",
            choices=[str(i) for i in range(1, len(categories) + 1)],
            default="1"
        )
        category = categories[int(cat_choice) - 1]
        
        # Difficulty selection
        difficulties = [diff.value for diff in TaskDifficulty]
        diff_table = Table(show_header=False, box=None)
        for i, diff in enumerate(difficulties, 1):
            diff_table.add_row(str(i), diff)
        self.console.print(diff_table)
        
        diff_choice = Prompt.ask(
            "Select Difficulty",
            choices=[str(i) for i in range(1, len(difficulties) + 1)],
            default="1"
        )
        difficulty = difficulties[int(diff_choice) - 1]
        
        # Deadline
        deadline_str = Prompt.ask(
            "Deadline (YYYY-MM-DD, optional)",
            default=""
        )
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                self.console.print("[red]Invalid date format. Skipping deadline.[/red]")
        
        return {
            "title": title,
            "description": description,
            "category": category,
            "difficulty": difficulty,
            "deadline": deadline
        }
    
    def get_palace_input(self) -> dict:
        """Get palace input from user."""
        self.console.print("\n[bold cyan]Create New Palace[/bold cyan]")
        
        name = Prompt.ask("Palace Name")
        description = Prompt.ask("Description (optional)", default="")
        boss_name = Prompt.ask("Boss Name / Final Milestone (optional)", default="")
        
        # Deadline
        deadline_str = Prompt.ask(
            "Deadline (YYYY-MM-DD, optional)",
            default=""
        )
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                self.console.print("[red]Invalid date format. Skipping deadline.[/red]")
        
        return {
            "name": name,
            "description": description,
            "boss_name": boss_name,
            "deadline": deadline
        }
    
    def get_task_id(self, prompt_text: str = "Enter Task ID") -> Optional[int]:
        """Get task ID from user."""
        try:
            task_id = int(Prompt.ask(f"[cyan]{prompt_text}[/cyan]"))
            return task_id
        except ValueError:
            self.console.print("[red]Invalid task ID.[/red]")
            return None
    
    def confirm_action(self, message: str) -> bool:
        """Get confirmation from user."""
        return Confirm.ask(f"[yellow]{message}[/yellow]")
    
    def get_username(self) -> str:
        """Get username from user."""
        return Prompt.ask("[bold cyan]Enter your username[/bold cyan]")

