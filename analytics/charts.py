"""Chart generation with matplotlib."""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, date
from typing import List, Dict, Optional
import os


class ChartGenerator:
    """Generate charts for analytics."""
    
    def __init__(self, output_dir: str = "charts"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        plt.style.use('dark_background')
    
    def plot_stats_radar(self, stats: Dict[str, int], username: str, save_path: Optional[str] = None):
        """Create a radar chart for stats."""
        import numpy as np
        
        stat_names = ["Knowledge", "Guts", "Proficiency", "Kindness", "Charm"]
        values = [stats.get(name, 0) for name in stat_names]
        
        # Number of variables
        N = len(stat_names)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        # Add values
        values += values[:1]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values, 'o-', linewidth=2, color='#FF6B6B', label='Stats')
        ax.fill(angles, values, alpha=0.25, color='#FF6B6B')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(stat_names, fontsize=12)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
        ax.grid(True)
        ax.set_title(f'{username}\'s Stats Profile', size=16, fontweight='bold', pad=20, color='white')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        else:
            save_path = os.path.join(self.output_dir, f"{username}_stats_radar.png")
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        
        plt.close()
        return save_path
    
    def plot_stats_bar(self, stats: Dict[str, int], username: str, save_path: Optional[str] = None):
        """Create a bar chart for stats."""
        stat_names = ["Knowledge", "Guts", "Proficiency", "Kindness", "Charm"]
        values = [stats.get(name, 0) for name in stat_names]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(stat_names, values, color=colors, edgecolor='white', linewidth=2)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold', color='white')
        
        ax.set_ylim(0, 100)
        ax.set_ylabel('Value', fontsize=12, color='white')
        ax.set_title(f'{username}\'s Statistics', fontsize=16, fontweight='bold', color='white', pad=20)
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        else:
            save_path = os.path.join(self.output_dir, f"{username}_stats_bar.png")
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        
        plt.close()
        return save_path
    
    def plot_exp_progress(self, exp_history: List[Dict], username: str, save_path: Optional[str] = None):
        """Plot EXP progress over time."""
        if not exp_history:
            return None
        
        dates = [datetime.fromisoformat(item['date']) for item in exp_history]
        exp_values = [item['exp'] for item in exp_history]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, exp_values, marker='o', linewidth=2, color='#FF6B6B', markersize=8)
        ax.fill_between(dates, exp_values, alpha=0.3, color='#FF6B6B')
        
        ax.set_xlabel('Date', fontsize=12, color='white')
        ax.set_ylabel('Total EXP', fontsize=12, color='white')
        ax.set_title(f'{username}\'s EXP Progress', fontsize=16, fontweight='bold', color='white', pad=20)
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        else:
            save_path = os.path.join(self.output_dir, f"{username}_exp_progress.png")
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        
        plt.close()
        return save_path
    
    def plot_palace_progress(self, palaces: List[Dict], username: str, save_path: Optional[str] = None):
        """Plot palace infiltration progress."""
        if not palaces:
            return None
        
        names = [p['name'][:15] + "..." if len(p['name']) > 15 else p['name'] for p in palaces]
        percentages = [p['infiltration'] for p in palaces]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ['#FF6B6B' if p < 50 else '#4ECDC4' if p < 100 else '#45B7D1' for p in percentages]
        bars = ax.barh(names, percentages, color=colors, edgecolor='white', linewidth=2)
        
        # Add percentage labels
        for bar, percentage in zip(bars, percentages):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{percentage:.1f}%',
                   ha='left' if width < 50 else 'right', va='center', 
                   fontsize=11, fontweight='bold', color='white')
        
        ax.set_xlim(0, 100)
        ax.set_xlabel('Infiltration %', fontsize=12, color='white')
        ax.set_title(f'{username}\'s Palace Progress', fontsize=16, fontweight='bold', color='white', pad=20)
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        else:
            save_path = os.path.join(self.output_dir, f"{username}_palaces.png")
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='black')
        
        plt.close()
        return save_path

