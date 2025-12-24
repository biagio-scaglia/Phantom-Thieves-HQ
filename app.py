"""Phantom Thieves HQ - Main Application."""
import sys
from rich.console import Console
from rich.panel import Panel
from db.database import init_db, SessionLocal
from core.game_loop import GameState
from ui.dashboard import Dashboard
from ui.menus import MenuSystem
from analytics.charts import ChartGenerator
from sqlalchemy.orm import Session


class PhantomThievesApp:
    """Main application class."""
    
    def __init__(self):
        self.console = Console()
        self.dashboard = Dashboard()
        self.menu = MenuSystem()
        self.chart_gen = ChartGenerator()
        self.db: Session = SessionLocal()
        self.game_state = GameState(self.db)
        self.running = True
    
    def initialize(self):
        """Initialize database and display welcome."""
        try:
            init_db()
            self.dashboard.display_welcome()
        except Exception as e:
            self.console.print(f"[bold red]Error initializing: {e}[/bold red]")
            sys.exit(1)
    
    def login_or_create_user(self):
        """Handle user login or creation."""
        username = self.menu.get_username()
        
        user = self.game_state.load_user(username)
        if not user:
            if self.menu.confirm_action(f"User '{username}' not found. Create new user?"):
                user = self.game_state.create_user(username)
                self.dashboard.display_success(f"Welcome, {username}! Your journey begins now! 🃏")
            else:
                self.console.print("[yellow]Exiting...[/yellow]")
                sys.exit(0)
        else:
            self.dashboard.display_success(f"Welcome back, {username}! 🃏")
        
        return user
    
    def show_dashboard(self):
        """Display main dashboard."""
        self.console.clear()
        
        user = self.game_state.current_user
        stats = self.game_state.get_user_stats()
        
        self.dashboard.display_user_profile(user, stats)
        self.console.print()
        
        if stats:
            self.dashboard.display_stats(stats)
            self.console.print()
        
        # Show pending tasks
        pending_tasks = self.game_state.get_pending_tasks()
        if pending_tasks:
            self.dashboard.display_tasks(pending_tasks[:5], "📋 Recent Pending Tasks")
            self.console.print()
        
        # Show active palaces
        from core.palace_engine import PalaceEngine
        active_palaces = PalaceEngine.get_active_palaces(self.db, user.id)
        if active_palaces:
            self.dashboard.display_palaces(active_palaces, "🏯 Active Palaces")
    
    def handle_tasks(self):
        """Handle task management."""
        while True:
            self.console.clear()
            choice = self.menu.task_menu()
            
            if choice == "0":
                break
            elif choice == "1":
                self.create_task()
            elif choice == "2":
                self.complete_task()
            elif choice == "3":
                self.view_all_tasks()
            elif choice == "4":
                self.view_overdue_tasks()
    
    def create_task(self):
        """Create a new task."""
        try:
            task_input = self.menu.get_task_input()
            task = self.game_state.create_task(
                title=task_input["title"],
                category=task_input["category"],
                difficulty=task_input["difficulty"],
                description=task_input["description"],
                deadline=task_input["deadline"]
            )
            self.dashboard.display_success(f"Task '{task.title}' created successfully!")
            self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
        except Exception as e:
            self.dashboard.display_error(str(e))
            self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def complete_task(self):
        """Complete a task."""
        pending_tasks = self.game_state.get_pending_tasks()
        if not pending_tasks:
            self.dashboard.display_info("No pending tasks available.")
            self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
            return
        
        self.dashboard.display_tasks(pending_tasks, "📋 Select Task to Complete")
        task_id = self.menu.get_task_id()
        
        if task_id:
            try:
                result = self.game_state.complete_task(task_id)
                self.dashboard.display_completion_message(result)
                self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
            except Exception as e:
                self.dashboard.display_error(str(e))
                self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def view_all_tasks(self):
        """View all tasks."""
        from models.task import Task, TaskStatus
        all_tasks = self.db.query(Task).filter(
            Task.user_id == self.game_state.current_user.id
        ).order_by(Task.created_at.desc()).all()
        
        self.dashboard.display_tasks(all_tasks, "📋 All Tasks")
        self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def view_overdue_tasks(self):
        """View overdue tasks."""
        overdue_tasks = self.game_state.get_overdue_tasks()
        if overdue_tasks:
            self.dashboard.display_tasks(overdue_tasks, "⚠️ Overdue Tasks")
        else:
            self.dashboard.display_success("No overdue tasks! Great job! 🎉")
        self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def handle_palaces(self):
        """Handle palace management."""
        while True:
            self.console.clear()
            choice = self.menu.palace_menu()
            
            if choice == "0":
                break
            elif choice == "1":
                self.create_palace()
            elif choice == "2":
                self.view_active_palaces()
            elif choice == "3":
                self.view_completed_palaces()
    
    def create_palace(self):
        """Create a new palace."""
        try:
            palace_input = self.menu.get_palace_input()
            palace = self.game_state.create_palace(
                name=palace_input["name"],
                description=palace_input["description"],
                boss_name=palace_input["boss_name"],
                deadline=palace_input["deadline"]
            )
            self.dashboard.display_success(f"Palace '{palace.name}' created successfully!")
            self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
        except Exception as e:
            self.dashboard.display_error(str(e))
            self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def view_active_palaces(self):
        """View active palaces."""
        from core.palace_engine import PalaceEngine
        active_palaces = PalaceEngine.get_active_palaces(self.db, self.game_state.current_user.id)
        self.dashboard.display_palaces(active_palaces, "🏯 Active Palaces")
        self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def view_completed_palaces(self):
        """View completed palaces."""
        from core.palace_engine import PalaceEngine
        completed_palaces = PalaceEngine.get_completed_palaces(self.db, self.game_state.current_user.id)
        self.dashboard.display_palaces(completed_palaces, "🏆 Completed Palaces")
        self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def show_analytics(self):
        """Show analytics and charts."""
        self.console.clear()
        user = self.game_state.current_user
        stats = self.game_state.get_user_stats()
        
        if not stats:
            self.dashboard.display_info("No statistics available yet.")
            self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
            return
        
        self.console.print(Panel(
            "[bold cyan]Generating Analytics Charts...[/bold cyan]",
            border_style="cyan"
        ))
        
        try:
            # Generate stats radar chart
            radar_path = self.chart_gen.plot_stats_radar(stats, user.username)
            self.dashboard.display_success(f"Radar chart saved: {radar_path}")
            
            # Generate stats bar chart
            bar_path = self.chart_gen.plot_stats_bar(stats, user.username)
            self.dashboard.display_success(f"Bar chart saved: {bar_path}")
            
            # Generate palace progress chart
            from core.palace_engine import PalaceEngine
            active_palaces = PalaceEngine.get_active_palaces(self.db, user.id)
            if active_palaces:
                palace_data = [{
                    "name": p.name,
                    "infiltration": p.infiltration_percentage
                } for p in active_palaces]
                palace_path = self.chart_gen.plot_palace_progress(palace_data, user.username)
                self.dashboard.display_success(f"Palace chart saved: {palace_path}")
            
            self.console.print("\n[bold green]✅ All charts generated successfully![/bold green]")
            self.console.print("[dim]Check the 'charts' directory for saved images.[/dim]")
            
        except Exception as e:
            self.dashboard.display_error(f"Error generating charts: {e}")
        
        self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
    
    def run(self):
        """Run the main application loop."""
        self.initialize()
        user = self.login_or_create_user()
        
        while self.running:
            try:
                self.console.clear()
                choice = self.menu.main_menu()
                
                if choice == "0":
                    self.console.print("\n[bold yellow]Take Your Heart! 🃏[/bold yellow]")
                    break
                elif choice == "1":
                    self.show_dashboard()
                    self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
                elif choice == "2":
                    self.handle_tasks()
                elif choice == "3":
                    self.handle_palaces()
                elif choice == "4":
                    self.show_analytics()
                elif choice == "5":
                    self.dashboard.display_info("Settings feature coming soon!")
                    self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
            
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Exiting...[/yellow]")
                break
            except Exception as e:
                self.dashboard.display_error(f"Unexpected error: {e}")
                self.menu.console.input("\n[dim]Press Enter to continue...[/dim]")
        
        self.db.close()
    
    def __del__(self):
        """Cleanup."""
        if hasattr(self, 'db'):
            self.db.close()


def main():
    """Main entry point."""
    app = PhantomThievesApp()
    app.run()


if __name__ == "__main__":
    main()

