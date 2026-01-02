import sys
sys.path.insert(0, 'src')

from core.simulation import Simulation
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime
from collections import defaultdict

class GprahRunner:
    # graph for doing multiple sim runs and collecting stats
    # maybe add config file support later?
    
    def __init__(self, num_runs=20):
        self.num_runs = num_runs
        self.results = []
        self.honour_progression = defaultdict(list)  # track honour progression over time for graphs
    
    def run_experiment(self, config_name, **sim_params):
        #run a bunch of simulations with the given params and collect stats
        print(f"Running experiment: {config_name}")
        print(f"Parameters: {sim_params}")
        print(f"Number of runs: {self.num_runs}")

        
        run_results = []
        
        for run_num in range(self.num_runs):
            print(f"Run {run_num + 1}/{self.num_runs}...", end=' ', flush=True)
            
            sim = Simulation(**sim_params)
            
            try:
                #suppress print output during run
                import io
                import contextlib
                
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    sim.run(display_every=0, max_turns=100)
                
                turns_survived = sim.turn 
                
            except Exception as e:
                print(f"Error in run {run_num + 1}: {e}")  
                continue
            
            dek = next((p for p in sim.predators if p.isDek), None)
            boss = next((m for m in sim.monsters if m.is_boss), None)
            
            if dek:
                dek_honour = dek.honour
                dek_health = dek.health
                dek_kills = dek.kills
                dek_stamina = dek.stamina
                dek_max_honour = max(dek.honour, 50 + dek.kills * 10)  #rough estimate starting at 50
                
                honour_timeline = []
                for turn in range(0, min(turns_survived + 1, 100), 10):
                    estimated_honour = min(100, 50 + (dek.kills * 10 * turn / max(turns_survived, 1)))
                    honour_timeline.append({
                        'turn': turn,
                        'honour': estimated_honour if turn < turns_survived else dek.honour,
                        'health': dek.health if turn == turns_survived else 100,
                        'kills': int(dek.kills * turn / max(turns_survived, 1)),
                        'stamina': dek.stamina if turn == turns_survived else 100
                    })
            else:
                
                dek_honour = 0
                dek_health = 0
                dek_kills = 0
                dek_stamina = 0
                dek_max_honour = 0
                honour_timeline = []
            
            result = {
                'run': run_num + 1,
                'config': config_name,
                'turns_survived': turns_survived,
                'max_turns': sim.max_turns,
                'dek_survived': dek.alive if dek else False,
                'boss_defeated': not (boss.alive if boss else False),
                'boss_alive': boss.alive if boss else False,
                'total_kills': sim.stats['kills'],
                'total_deaths': sim.stats['deaths'],
                'total_combats': sim.stats['combats'],
                'resources_collected': sim.stats.get('resources_collected', 0),
                'dek_honour': dek_honour,
                'dek_health': dek_health,
                'dek_kills': dek_kills,
                'dek_stamina': dek_stamina,
                'dek_max_honour': dek_max_honour,
                'honour_timeline': honour_timeline
            }
            
            run_results.append(result)
            print("good run")
        
        self.results.extend(run_results)
        
        #save honour data for plots
        for result in run_results:
            if result['honour_timeline']:
                self.honour_progression[config_name].extend(result['honour_timeline'])
        
        return run_results
    
    def generate_statistics(self):
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
            median_turns = np.median([r['turns_survived'] for r in config_results])
            
            avg_honour = np.mean([r['dek_honour'] for r in config_results])
            std_honour = np.std([r['dek_honour'] for r in config_results])
            max_honour_achieved = max([r['dek_max_honour'] for r in config_results], default=0)
            
            avg_kills = np.mean([r['dek_kills'] for r in config_results])
            avg_combats = np.mean([r['total_combats'] for r in config_results])
            avg_resources = np.mean([r['resources_collected'] for r in config_results])
            
            survived_turns = [r['turns_survived'] for r in config_results if r['dek_survived']]
            died_turns = [r['turns_survived'] for r in config_results if not r['dek_survived']]
            
            stats_by_config[config] = {
                'total_runs': total_runs,
                'survival_rate': survival_rate,
                'boss_defeat_rate': boss_defeat_rate,
                'avg_turns': avg_turns,
                'std_turns': std_turns,
                'median_turns': median_turns,
                'avg_honour': avg_honour,
                'std_honour': std_honour,
                'max_honour_achieved': max_honour_achieved,
                'avg_kills': avg_kills,
                'avg_combats': avg_combats,
                'avg_resources': avg_resources,
                'survived_turns': survived_turns,
                'died_turns': died_turns
            }
        
     
        print("statistical analysis results:")
        for config, stats in stats_by_config.items():
            print(f"Configuration: {config}")
            print(f"Total runs: {stats['total_runs']}")
            print(f"Dek survival rate: {stats['survival_rate']:.1f}%")
            print(f"Boss defeat rate: {stats['boss_defeat_rate']:.1f}%")
            print(f"Average survival time: {stats['avg_turns']:.1f} ± {stats['std_turns']:.1f} turns")
            print(f"Median survival time: {stats['median_turns']:.1f} turns")
            print(f"Average final honour: {stats['avg_honour']:.1f} ± {stats['std_honour']:.1f}")
            print(f"Maximum honour achieved: {stats['max_honour_achieved']:.1f}")
            print(f"Average kills: {stats['avg_kills']:.1f}")
            print(f"Average combats: {stats['avg_combats']:.1f}")
            print(f"Average resources collected: {stats['avg_resources']:.1f}")
            if stats['survived_turns']:
                print(f"  Survived runs - avg turns: {np.mean(stats['survived_turns']):.1f}")
            if stats['died_turns']:
                print(f"  Died runs - avg turns: {np.mean(stats['died_turns']):.1f}")
            print()
        
        return stats_by_config
    
    def plot_results(self, output_file='experiment_results.png'):
        if not self.results:
            return
        
        fig = plt.figure(figsize=(16, 12))
        
        configs = sorted(set(r['config'] for r in self.results))
        
        ax1 = plt.subplot(3, 3, 1)
        survival_rates = []
        for config in configs:
            config_results = [r for r in self.results if r['config'] == config]
            rate = sum(1 for r in config_results if r['dek_survived']) / len(config_results) * 100
            survival_rates.append(rate)
        
        ax1.bar(configs, survival_rates, color='blue')
        ax1.set_title('Dek Survival Rate by Configuration', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Survival Rate (%)')
        ax1.set_ylim(0, 100)
        for i, v in enumerate(survival_rates):
            ax1.text(i, v + 2, f'{v:.1f}%', ha='center')
        
        ax2 = plt.subplot(3, 3, 2)
        honours = [r['dek_honour'] for r in self.results]
        ax2.hist(honours, bins=20, color='gold', edgecolor='black')
        ax2.set_title('Final Honour Score Distribution', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Final Honour')
        ax2.set_ylabel('Frequency')
        ax2.axvline(np.mean(honours), color='red', linestyle='--', label=f'Mean: {np.mean(honours):.1f}')
        ax2.legend()
        
        ax3 = plt.subplot(3, 3, 3)
        turns = [r['turns_survived'] for r in self.results]
        ax3.hist(turns, bins=20, color='lightcoral', edgecolor='black')
        ax3.set_title('Survival Time Distribution', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Turns Survived')
        ax3.set_ylabel('Frequency')
        ax3.axvline(np.mean(turns), color='blue', linestyle='--', label=f'Mean: {np.mean(turns):.1f}')
        ax3.legend()
        
        ax4 = plt.subplot(3, 3, 4)
        for config in configs:
            if config in self.honour_progression:
                timeline = self.honour_progression[config]
                if timeline:
                    turns = [t['turn'] for t in timeline]
                    honours = [t['honour'] for t in timeline]
                    sampled_turns = turns[::5]  #downsample to reduce clutter
                    sampled_honours = honours[::5]
                    ax4.plot(sampled_turns, sampled_honours, alpha=0.3, label=config)
        
        if self.honour_progression:
            all_turns = sorted(set(t['turn'] for timeline in self.honour_progression.values() for t in timeline))
            avg_honours = []
            for turn in all_turns[:100]:
                honours_at_turn = [t['honour'] for timeline in self.honour_progression.values() 
                                 for t in timeline if t['turn'] == turn]
                if honours_at_turn:
                    avg_honours.append(np.mean(honours_at_turn))
                else:
                    avg_honours.append(avg_honours[-1] if avg_honours else 50)
            
            ax4.plot(all_turns[:len(avg_honours)], avg_honours, 'r-', linewidth=2, 
                    label='Average', alpha=0.8)
        
        ax4.set_title('Honour Progression Over Time', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Turn')
        ax4.set_ylabel('Honour')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        ax5 = plt.subplot(3, 3, 5)
        survived = [r['turns_survived'] for r in self.results if r['dek_survived']]
        died = [r['turns_survived'] for r in self.results if not r['dek_survived']]
        if survived and died:
            ax5.boxplot([survived, died], labels=['Survived', 'Died'])
            ax5.set_title('Survival Time: Survived vs Died', fontsize=12, fontweight='bold')
            ax5.set_ylabel('Turns')
        
        ax6 = plt.subplot(3, 3, 6)
        boss_rates = []
        for config in configs:
            config_results = [r for r in self.results if r['config'] == config]
            rate = sum(1 for r in config_results if r['boss_defeated']) / len(config_results) * 100
            boss_rates.append(rate)
        
        ax6.bar(configs, boss_rates, color='darkred')
        ax6.set_title('Boss Defeat Rate by Configuration', fontsize=12, fontweight='bold')
        ax6.set_ylabel('Defeat Rate (%)')
        ax6.set_ylim(0, 100)
        for i, v in enumerate(boss_rates):
            ax6.text(i, v + 2, f'{v:.1f}%', ha='center')
        
        ax7 = plt.subplot(3, 3, 7)
        kills = [r['dek_kills'] for r in self.results]
        ax7.hist(kills, bins=15, color='purple', edgecolor='black')
        ax7.set_title('Kills Distribution', fontsize=12, fontweight='bold')
        ax7.set_xlabel('Number of Kills')
        ax7.set_ylabel('Frequency')
        
        ax8 = plt.subplot(3, 3, 8)
        resources_by_config = {}
        for config in configs:
            config_results = [r for r in self.results if r['config'] == config]
            resources_by_config[config] = [r['resources_collected'] for r in config_results]
        
        ax8.boxplot([resources_by_config.get(c, []) for c in configs], labels=configs)
        ax8.set_title('Resources Collected by Configuration', fontsize=12, fontweight='bold')
        ax8.set_ylabel('Resources Collected')
        
        ax9 = plt.subplot(3, 3, 9)
        survived_honour = [r['dek_honour'] for r in self.results if r['dek_survived']]
        died_honour = [r['dek_honour'] for r in self.results if not r['dek_survived']]
        
        if survived_honour and died_honour:
            ax9.scatter([1]*len(survived_honour), survived_honour, alpha=0.5, label='Survived', color='green')
            ax9.scatter([2]*len(died_honour), died_honour, alpha=0.5, label='Died', color='red')
            ax9.set_xticks([1, 2])
            ax9.set_xticklabels(['Survived', 'Died'])
            ax9.set_title('Final Honour: Survived vs Died', fontsize=12, fontweight='bold')
            ax9.set_ylabel('Final Honour')
            ax9.legend()
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plots saved to {output_file}")
        plt.close()
    
    def save_results(self, filename='experiment_results.json'):
        serialisable_results = []
        for r in self.results:
            sr = r.copy()
            serialisable_results.append(sr)
        
        with open(filename, 'w') as f:
            json.dump(serialisable_results, f, indent=2)
        print(f"💾 Results saved to {filename}")
    
    def print_evaluation(self):
        print("CRITICAL EVALUATION OF EMERGENT BEHAVIOURS")
   
        
        if not self.results:
            print("No results to evaluate")
            return
        
        survival_rate = sum(1 for r in self.results if r['dek_survived']) / len(self.results) * 100
        avg_honour = np.mean([r['dek_honour'] for r in self.results])
        avg_kills = np.mean([r['dek_kills'] for r in self.results])
        
        print("1. SURVIVAL PATTERNS:")
        print(f"   - Overall survival rate: {survival_rate:.1f}%")
        print(f"   - Average honour score of {avg_honour:.1f} suggests some adaptive behavior")
        print(f"   - Avg {avg_kills:.1f} kills per run shows active threat engagement\n")
          
        

if __name__ == "__main__":
    runner = ExperimentRunner(num_runs=20)
    
    runner.run_experiment("baseline", width=20, height=20, 
                         num_predators=3, num_monsters=5)
    
    runner.run_experiment("high_difficulty", width=20, height=20,
                         num_predators=3, num_monsters=8)
    
    stats = runner.generate_statistics()
    runner.plot_results()
    runner.save_results()
    runner.print_evaluation()