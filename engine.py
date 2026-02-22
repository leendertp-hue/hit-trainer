import random
import copy
from exercises import MASTER_LIBRARY

class HITEngine:
    def __init__(self, days, equipment, target_reps, beginner=False): # Added beginner=False
        self.days = days
        self.equipment = equipment
        self.target_reps = target_reps
        self.beginner = beginner # Store the flag
        
        # --- DYNAMIC VOLUME SCALING ---
        if self.days == 2:
            vol = 2
        elif self.days in [3, 4]:
            vol = 4
        elif self.days == 5:
            vol = 5
        else: 
            vol = 6
            
        self.targets = {
            "Pectorals": vol, "Upper Back": vol, "Quads": vol, 
            "Hamstrings/Glutes": vol, "Front Delts": vol, 
            "Side Delts": vol, "Rear Delts": vol, "Triceps": vol, "Biceps": vol
        }

    def generate_program(self):
        """Generates a 6-week block with unique memory objects per week."""
        pool = [ex for ex in MASTER_LIBRARY if ex['equip'] in self.equipment]
        
        # --- ERROR CHECK ---
        total_possible_units = {m: 0.0 for m in self.targets.keys()}
        for ex in pool:
            for m, val in ex['impact'].items():
                if m in total_possible_units: total_possible_units[m] += val
            for m, val in ex['secondary'].items():
                if m in total_possible_units: total_possible_units[m] += val
        
        missing_muscles = [m for m, target in self.targets.items() if total_possible_units[m] < target]
        if missing_muscles:
            return {
                "error": "Insufficient Equipment",
                "missing": missing_muscles,
                "details": f"Missing gear for: {', '.join(missing_muscles)}."
            }

        # 2. UTILITY-BASED SELECTION
        current_volume = {m: 0.0 for m in self.targets.keys()}
        selected_moves = []

        while True:
            deficits = {m: self.targets[m] - current_volume[m] for m in self.targets}
            if max(deficits.values()) <= 0:
                break
            
            best_score = 0
            candidates = []
            
            for ex in pool:
                if ex['name'] in [m['name'] for m in selected_moves]:
                    continue
                
                utility = sum(min(val, max(0, deficits.get(m, 0))) for m, val in ex['impact'].items())
                utility += sum(min(val, max(0, deficits.get(m, 0))) for m, val in ex['secondary'].items())
                
                if utility > best_score:
                    best_score = utility
                    candidates = [ex]
                elif utility == best_score and best_score > 0:
                    candidates.append(ex)
            
            if not candidates:
                break

            # --- BEGINNER LOGIC: TIERED SELECTION ---
            if self.beginner:
                gentle_candidates = [c for c in candidates if c.get('gentle') == True]
                chosen = random.choice(gentle_candidates) if gentle_candidates else random.choice(candidates)
            else:
                chosen = random.choice(candidates)
                
            selected_moves.append(chosen)
            
            for m, val in chosen['impact'].items():
                current_volume[m] += val
            for m, val in chosen['secondary'].items():
                current_volume[m] += val

        # 3. DISTRIBUTION & DEEP COPY
        random.shuffle(selected_moves)
        low, high = map(int, self.target_reps.split('-'))
        program = {"weeks": {}}

        week_template = {}
        for d in range(1, self.days + 1):
            d_key = f"Day {d}"
            moves_for_day = selected_moves[d-1::self.days]
            
            day_list = []
            for ex in moves_for_day:
                is_bw = ex.get('equip') == "Bodyweight"
                is_weighted_bw = "Weighted" in ex['name']
                p_type = "density" if (is_bw and not is_weighted_bw) else "standard"
                
                day_list.append({
                    "name": ex['name'],
                    "prog_type": p_type,
                    "target_reps": 0 if p_type == "density" else random.randint(low, high),
                    "target_weight": 0.0,
                    "e1rm": 0.0,
                    "discovery_reps": 0
                })
            week_template[d_key] = day_list

        for w in range(1, 7):
            program["weeks"][f"Week {w}"] = copy.deepcopy(week_template)
        
        return {"program": program, "volume_report": current_volume}
    
    #SWAP Engine

    def get_single_swap(self, current_name, all_week_exercise_names):
        """Finds the best alternative while strictly respecting gear and rep range."""
        
        # 1. THE STRICT POOL (Fixed to prevent Arnold Press leak)
        # Sanitizes "Dumbbell" vs "Dumbbells"
        user_gear = [g.lower().strip().rstrip('s') for g in self.equipment]
        pool = []
        for ex in MASTER_LIBRARY:
            lib_gear = ex['equip'].lower().strip().rstrip('s')
            if lib_gear in user_gear:
                pool.append(ex)
        
        # 0. Identify what we are losing
        original_ex = next((x for x in MASTER_LIBRARY if x['name'] == current_name), None)
        if not original_ex: return None
        
        # 1. Census: Current Volume
        current_block_vol = {m: 0.0 for m in self.targets.keys()}
        for name in all_week_exercise_names:
            if name == current_name: continue
            ex_data = next((x for x in MASTER_LIBRARY if x['name'] == name), None)
            if ex_data:
                for m, val in ex_data.get('impact', {}).items():
                    if m in current_block_vol: current_block_vol[m] += val
                for m, val in ex_data.get('secondary', {}).items():
                    if m in current_block_vol: current_block_vol[m] += (val * 0.5)

        # 2. Gap Analysis
        deficits = {m: self.targets[m] - current_block_vol[m] for m in self.targets}
        best_score, candidates = -999, []
        
        for ex in pool:
            if ex['name'] in all_week_exercise_names: continue
            score = 0
            combined_impact = {**ex.get('secondary', {}), **ex.get('impact', {})}
            for m, val in combined_impact.items():
                deficit = deficits.get(m, 0)
                if deficit > 0:
                    score += (min(val, deficit))
                else:
                    score -= (val) 

            if score > best_score:
                best_score, candidates = score, [ex]
            elif score == best_score:
                candidates.append(ex)

        if not candidates: return None

        # 3. Selection
        if self.beginner:
            gentle = [c for c in candidates if c.get('gentle')]
            chosen = random.choice(gentle) if gentle else random.choice(candidates)
        else:
            chosen = random.choice(candidates)

        # --- 4. THE REP RANGE FIX ---
        # We parse the string (e.g., "8-12") passed from the DB to the Engine
        try:
            low, high = map(int, self.target_reps.split('-'))
        except (ValueError, AttributeError):
            # Fallback to general hypertrophy if the string is malformed
            low, high = 8, 12

        is_bw = chosen.get('equip') == "Bodyweight"
        p_type = "density" if (is_bw and "Weighted" not in chosen['name']) else "standard"

        return {
            "name": chosen['name'],
            "prog_type": p_type,
            "target_reps": 0 if p_type == "density" else random.randint(low, high),
            "target_weight": 0.0,
            "e1rm": 0.0,
            "discovery_reps": 0
        }