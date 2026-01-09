
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  
project_root = os.path.dirname(parent_dir) 
sys.path.insert(0, parent_dir)
sys.path.insert(0, project_root)
from core.simulation import Simulation
from matplotlib import *
import matplotlib.pyplot as plt
import json
import numpy as np
from collections import defaultdict

class ExperimentRunner:
    """
    Runs multiple simulations and collects REAL statistical data
    """
    
    def __init__(self, num_runs=20):
        self.num_runs = num_runs
        self.results = []
        self.honour_timelines = defaultdict(list)  # stores actual honour progression
    
    def run_experiment(self, config_name, **sim_params):
        """
        Run multiple simulations with given parameters and collect real stats
        """
        print(f"\n{'='*60}")
        print(f"Running experiment: {config_name}")
        print(f"Parameters: {sim_params}")
        print(f"Number of runs: {self.num_runs}")
        print(f"{'='*60}\n")
        
        run_results = []
        
        for run_num in range(self.num_runs):
            print(f"Run {run_num + 1}/{self.num_runs}... ", end='', flush=True)
            
            # Create simulation with custom tracking
            sim = Simulation(**sim_params)
            
            # Add tracking hooks to Dek
            dek = next((p for p in sim.predators if p.isDek), None)
            if dek:
                dek.honour_history = []  # Track honour over time
                dek.health_history = []  # Track health over time
                dek.stamina_history = []
                dek.kill_history = []
            
            try:
                # Run simulation with suppressed output
                import io
                import contextlib
                
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    # Modified run to track metrics each turn
                    self._run_with_tracking(sim, max_turns=100)
                
                turns_survived = sim.turn
                
            except Exception as e:
                print(f"ERROR: {e}")
                import traceback
                traceback.print_exc()
                continue
            
            # Collect final results
            boss = next((m for m in sim.monsters if m.is_boss), None)
            
            if dek and hasattr(dek, 'honour_history'):
                result = {
                    'run': run_num + 1,
                    'config': config_name,
                    'turns_survived': turns_survived,
                    'max_turns': sim.max_turns,
                    'dek_survived': dek.alive,
                    'boss_defeated': not (boss.alive if boss else False),
                    'total_kills': sim.stats['kills'],
                    'total_deaths': sim.stats['deaths'],
                    'total_combats': sim.stats['combats'],
                    'resources_collected': sim.stats.get('resources_collected', 0),
                    'dek_honour': dek.honour,
                    'dek_health': dek.health,
                    'dek_kills': dek.kills,
                    'dek_stamina': dek.stamina,
                    'honour_timeline': list(dek.honour_history),
                    'health_timeline': list(dek.health_history),
                    'stamina_timeline': list(dek.stamina_history),
                    'kill_timeline': list(dek.kill_history),
                }
            else:
                result = {
                    'run': run_num + 1,
                    'config': config_name,
                    'turns_survived': turns_survived,
                    'max_turns': sim.max_turns,
                    'dek_survived': False,
                    'boss_defeated': False,
                    'total_kills': sim.stats['kills'],
                    'total_deaths': sim.stats['deaths'],
                    'total_combats': sim.stats['combats'],
                    'resources_collected': sim.stats.get('resources_collected', 0),
                    'dek_honour': 0,
                    'dek_health': 0,
                    'dek_kills': 0,
                    'dek_stamina': 0,
                    'honour_timeline': [],
                    'health_timeline': [],
                    'stamina_timeline': [],
                    'kill_timeline': [],
                }
            
            run_results.append(result)
            print(f"✓ Completed (survived={result['dek_survived']}, kills={result['dek_kills']})")
        
        self.results.extend(run_results)
        
        # Store timelines for plotting
        for result in run_results:
            if result['honour_timeline']:
                self.honour_timelines[config_name].append(result['honour_timeline'])
        
        return run_results
    
    def _run_with_tracking(self, sim, max_turns=100):
        """
        Run simulation while tracking metrics each turn
        """
        sim.max_turns = max_turns
        
        # Find Dek
        dek = next((p for p in sim.predators if p.isDek), None)
        
        # Main simulation loop with tracking
        for turn in range(1, max_turns + 1):
            sim.turn = turn
            sim.stats['turns'] = turn
            
            # Track Dek's stats THIS turn
            if dek and hasattr(dek, 'honour_history'):
                dek.honour_history.append(dek.honour)
                dek.health_history.append(dek.health)
                dek.stamina_history.append(dek.stamina)
                dek.kill_history.append(dek.kills)
            
            # Update agents
            sim._update_agents()
            
            # Check if hazard_generation exists before calling
            if hasattr(sim, 'hazard_generation'):
                sim.hazard_generation.update(turn)
            
            # Check if weather_update exists before calling
            if hasattr(sim, 'weather_update'):
                sim.weather_update()
            
            # Check win conditions
            if sim._check_win_conditions():
                break
            
            # Check if simulation should continue
            if len([p for p in sim.predators if p.alive]) == 0:
                break
            if len([m for m in sim.monsters if m.alive]) == 0:
                break
    
    def generate_statistics(self):
        """Generate comprehensive statistics from all runs"""
        if not self.results:
            print("No results to analyse!")
            return None
        
        stats_by_config = {}
        
        for config in set(r['config'] for r in self.results):
            config_results = [r for r in self.results if r['config'] == config]
            total_runs = len(config_results)
            
            if total_runs == 0:
                continue
            
            survival_rate = sum(1 for r in config_results if r['dek_survived']) / total_runs * 100
            boss_defeat_rate = sum(1 for r in config_results if r['boss_defeated']) / total_runs * 100
            
            avg_turns = np.mean([r['turns_survived'] for r in config_results])
            std_turns = np.std([r['turns_survived'] for r in config_results])
            
            avg_honour = np.mean([r['dek_honour'] for r in config_results])
            std_honour = np.std([r['dek_honour'] for r in config_results])
            
            avg_kills = np.mean([r['dek_kills'] for r in config_results])
            avg_combats = np.mean([r['total_combats'] for r in config_results])
            avg_resources = np.mean([r['resources_collected'] for r in config_results])
            
            stats_by_config[config] = {
                'total_runs': total_runs,
                'survival_rate': survival_rate,
                'boss_defeat_rate': boss_defeat_rate,
                'avg_turns': avg_turns,
                'std_turns': std_turns,
                'avg_honour': avg_honour,
                'std_honour': std_honour,
                'avg_kills': avg_kills,
                'avg_combats': avg_combats,
                'avg_resources': avg_resources,
            }
        
        # Print statistics
        print("\n" + "="*60)
        print("STATISTICAL ANALYSIS")
        print("="*60)
        for config, stats in stats_by_config.items():
            print(f"\n📊 Configuration: {config}")
            print(f"  • Total runs: {stats['total_runs']}")
            print(f"  • Survival rate: {stats['survival_rate']:.1f}%")
            print(f"  • Boss defeat rate: {stats['boss_defeat_rate']:.1f}%")
            print(f"  • Average survival: {stats['avg_turns']:.1f} ± {stats['std_turns']:.1f} turns")
            print(f"  • Average honour: {stats['avg_honour']:.1f} ± {stats['std_honour']:.1f}")
            print(f"  • Average kills: {stats['avg_kills']:.1f}")
            print(f"  • Average combats: {stats['avg_combats']:.1f}")
            print(f"  • Resources collected: {stats['avg_resources']:.1f}")
        print("="*60)
        
        return stats_by_config
    
    def plot_results(self, output_file='experiment_results.png'):
        """Generate comprehensive matplotlib visualizations"""
        if not self.results:
            print("No results to plot!")
            return
        
        print(f"\nGenerating plots...")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('Predator: Badlands - Multi-Agent Simulation Analysis', 
                     fontsize=16, fontweight='bold')
        
        configs = sorted(set(r['config'] for r in self.results))
        
        # 1. Survival Rate by Configuration
        ax1 = plt.subplot(3, 3, 1)
        survival_rates = []
        for config in configs:
            config_results = [r for r in self.results if r['config'] == config]
            rate = sum(1 for r in config_results if r['dek_survived']) / len(config_results) * 100
            survival_rates.append(rate)
        
        colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6']
        bars = ax1.bar(configs, survival_rates, color=colors[:len(configs)])
        ax1.set_title('Dek Survival Rate by Configuration', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Survival Rate (%)')
        ax1.set_ylim(0, 100)
        for i, v in enumerate(survival_rates):
            ax1.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
        
        # 2. Final Honour Distribution
        ax2 = plt.subplot(3, 3, 2)
        honours = [r['dek_honour'] for r in self.results if r['dek_survived']]
        if honours:
            ax2.hist(honours, bins=15, color='gold', edgecolor='black', alpha=0.7)
            ax2.set_title('Final Honour Score Distribution (Survivors)', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Final Honour')
            ax2.set_ylabel('Frequency')
            ax2.axvline(np.mean(honours), color='red', linestyle='--', linewidth=2,
                       label=f'Mean: {np.mean(honours):.1f}')
            ax2.legend()
        
        # 3. Survival Time Distribution
        ax3 = plt.subplot(3, 3, 3)
        turns = [r['turns_survived'] for r in self.results]
        ax3.hist(turns, bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
        ax3.set_title('Survival Time Distribution', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Turns Survived')
        ax3.set_ylabel('Frequency')
        ax3.axvline(np.mean(turns), color='blue', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(turns):.1f}')
        ax3.legend()
        
        # 4. Honour Progression Over Time (REAL DATA)
        ax4 = plt.subplot(3, 3, 4)
        for config in configs:
            if config in self.honour_timelines:
                timelines = self.honour_timelines[config]
                if timelines:
                    # Plot individual runs (faded)
                    for timeline in timelines[:5]:  # Show first 5 runs
                        turns_range = range(len(timeline))
                        ax4.plot(turns_range, timeline, alpha=0.2, color='gray')
                    
                    # Calculate and plot average
                    max_len = max(len(t) for t in timelines)
                    avg_timeline = []
                    for turn in range(max_len):
                        values = [t[turn] for t in timelines if len(t) > turn]
                        if values:
                            avg_timeline.append(np.mean(values))
                    
                    ax4.plot(range(len(avg_timeline)), avg_timeline, linewidth=2.5,
                            label=config, marker='o', markersize=3)
        
        ax4.set_title('Honour Progression Over Time (Real Data)', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Turn')
        ax4.set_ylabel('Honour Score')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Boss Defeat Rate
        ax5 = plt.subplot(3, 3, 5)
        boss_rates = []
        for config in configs:
            config_results = [r for r in self.results if r['config'] == config]
            rate = sum(1 for r in config_results if r['boss_defeated']) / len(config_results) * 100
            boss_rates.append(rate)
        
        ax5.bar(configs, boss_rates, color='darkred', alpha=0.7)
        ax5.set_title('Boss Defeat Rate by Configuration', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Defeat Rate (%)')
        ax5.set_ylim(0, 100)
        for i, v in enumerate(boss_rates):
            ax5.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
        
        # 6. Kills Distribution
        ax6 = plt.subplot(3, 3, 6)
        kills = [r['dek_kills'] for r in self.results]
        if kills and max(kills) > 0:
            ax6.hist(kills, bins=range(max(kills)+2), color='purple', edgecolor='black', alpha=0.7)
            ax6.set_title('Kills Distribution', fontsize=12, fontweight='bold')
            ax6.set_xlabel('Number of Kills')
            ax6.set_ylabel('Frequency')
            ax6.axvline(np.mean(kills), color='red', linestyle='--', linewidth=2,
                       label=f'Mean: {np.mean(kills):.1f}')
            ax6.legend()
        
        # 7. Survival vs Death Comparison
        ax7 = plt.subplot(3, 3, 7)
        survived_turns = [r['turns_survived'] for r in self.results if r['dek_survived']]
        died_turns = [r['turns_survived'] for r in self.results if not r['dek_survived']]
        
        if survived_turns and died_turns:
            box_data = [survived_turns, died_turns]
            bp = ax7.boxplot(box_data, tick_labels=['Survived', 'Died'], patch_artist=True)
            bp['boxes'][0].set_facecolor('green')
            bp['boxes'][0].set_alpha(0.5)
            bp['boxes'][1].set_facecolor('red')
            bp['boxes'][1].set_alpha(0.5)
            ax7.set_title('Survival Time: Survived vs Died', fontsize=12, fontweight='bold')
            ax7.set_ylabel('Turns')
        
        # 8. Resources Collected
        ax8 = plt.subplot(3, 3, 8)
        resources = [r['resources_collected'] for r in self.results]
        if resources and max(resources) > 0:
            ax8.hist(resources, bins=range(max(resources)+2), color='orange', edgecolor='black', alpha=0.7)
            ax8.set_title('Resources Collected Distribution', fontsize=12, fontweight='bold')
            ax8.set_xlabel('Resources Collected')
            ax8.set_ylabel('Frequency')
        
        # 9. Honour vs Survival Scatter
        ax9 = plt.subplot(3, 3, 9)
        survived_honour = [r['dek_honour'] for r in self.results if r['dek_survived']]
        survived_turns_scatter = [r['turns_survived'] for r in self.results if r['dek_survived']]
        died_honour = [r['dek_honour'] for r in self.results if not r['dek_survived']]
        died_turns_scatter = [r['turns_survived'] for r in self.results if not r['dek_survived']]
        
        if survived_honour:
            ax9.scatter(survived_turns_scatter, survived_honour, alpha=0.6, s=50, 
                       label='Survived', color='green', edgecolors='black')
        if died_honour:
            ax9.scatter(died_turns_scatter, died_honour, alpha=0.6, s=50,
                       label='Died', color='red', edgecolors='black')
        ax9.set_title('Honour vs Survival Time', fontsize=12, fontweight='bold')
        ax9.set_xlabel('Turns Survived')
        ax9.set_ylabel('Final Honour')
        ax9.legend()
        ax9.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Plots saved to {output_file}")
        plt.close()
    
    def save_results(self, filename='experiment_results.json'):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✓ Results saved to {filename}")


if __name__ == "__main__":
    print("="*60)
    print("PREDATOR: BADLANDS - EXPERIMENT RUNNER")
    print("="*60)
    print(f"\nProject structure detected:")
    print(f"  Script location: {__file__}")
    print(f"  Python path: {sys.path[:3]}")
    print()
    
    runner = ExperimentRunner(num_runs=10)
    
    # Run baseline experiment
    runner.run_experiment("baseline", 
                         width=20, height=20,
                         num_predators=3, num_monsters=5, num_synthetics=2)
    
    # Run high difficulty experiment
    runner.run_experiment("high_difficulty",
                         width=20, height=20,
                         num_predators=3, num_monsters=8, num_synthetics=2)
    
    # Generate statistics and plots
    stats = runner.generate_statistics()
    runner.plot_results('predator_badlands_analysis.png')
    runner.save_results('experiment_data.json')
    
    print("\n✓ Experiment complete!")
    print(f"  Check: predator_badlands_analysis.png")
    print(f"  Check: experiment_data.json")