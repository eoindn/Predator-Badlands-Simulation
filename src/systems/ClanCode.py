
from entities.agent import Agent
from entities.predator import Predator
from entities.monster import Monster
from entities.synthetics import Synthetic


class ClanCode:
 
    

    HONOR_BOSS_KILL = 20
    HONOR_WORTHY_KILL = 10
    HONOR_WOUNDED_ATTACK = 10
    HONOR_SYNTHETIC_ATTACK = -5
    HONOR_COWARDICE = -15
    
    @staticmethod
    def is_worthy_prey(predator: Predator, target: Agent) -> tuple[bool, str]:
        #Do not harm the unworthy as synthetics are not living prey
        if isinstance(target, Synthetic):
            return False, "not_alive"
        
        # Rule no 2 do not harm the sick and injured
        if hasattr(target, 'health') and hasattr(target, 'max_health'):
            health_percent = target.health / target.max_health
            if health_percent < 0.5:
                return False, "wounded_prey"
        
        
        if isinstance(target, Monster) and target.is_boss:
            return True, "ultimate_adversary"
        
        #full health enemies are worthy opponents
        if hasattr(target, 'health') and hasattr(target, 'max_health'):
            if target.health == target.max_health:
                return True, "healthy_prey"
            
        # default acceptable prey
        return True, "standard_prey"
    
    @staticmethod
    def calculate_honor_change(predator: Predator, target: Agent, action: str) -> tuple[int, str]:
    
        if action == "kill":
            if isinstance(target, Monster) and target.is_boss:
                return ClanCode.HONOR_BOSS_KILL, f"{predator.name} gains great honor for slaying the Ultimate Adversary!"
            
          
            is_worthy, reason = ClanCode.is_worthy_prey(predator, target)
            if is_worthy:
                return ClanCode.HONOR_WORTHY_KILL, f"{predator.name} gains honor for a successful hunt"
            
            
            
            
            
            
            if reason == "wounded_prey":
                return ClanCode.HONOR_WOUNDED_ATTACK, f"{predator.name} dishonorably killed wounded prey!"
            elif reason == "not_alive":
                return ClanCode.HONOR_SYNTHETIC_ATTACK, f"{predator.name} attacked non-living prey!"
        
        elif action == "attack":
          
            is_worthy, reason = ClanCode.is_worthy_prey(predator, target)
            if not is_worthy:
                if reason == "not_alive":
                    return ClanCode.HONOR_SYNTHETIC_ATTACK, f" {predator.name} attacks nonliving prey  dishonorable!"
                elif reason == "wounded_prey":
                    return ClanCode.HONOR_WOUNDED_ATTACK, f"{predator.name} attacks wounded prey  shameful!"
        
        elif action == "flee":
            return ClanCode.HONOR_COWARDICE, f"⚠️ {predator.name} fled from combat  cowardice!"
        
        return 0, ""
    
    @staticmethod
    def should_allow_action(predator: Predator, target: Agent, action: str) -> bool:
     
        if action in ["attack", "kill"]:
            is_worthy, reason = ClanCode.is_worthy_prey(predator, target)
            
        
            if reason == "not_alive" and predator.isDek:
                #dek hqs to follow the code more strictly
                print(f" {predator.name} refuses to attack {target.name}  not worthy prey!")
                return False
        
        return True