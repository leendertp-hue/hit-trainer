import random
import copy
from exercises import MASTER_LIBRARY

class HITEngine:
    def __init__(self, days, equipment, target_reps):
        self.days = days
        self.equipment = equipment
        self.target_reps = target_reps
        
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
            "Pectorals": vol, 
            "Upper Back": vol, 
            "Quads": vol, 
            "Hamstrings/Glutes": vol, 
            "Front Delts": vol, 
            "Side Delts": vol, 
            "Rear Delts": vol, 
            "Triceps": vol, 
            "Biceps": vol
        }

    def generate_program(self):
        """Generates a 6-week block with unique memory objects per week."""
        # 1. Gear Filter
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
            best_candidates = []
            
            for ex in pool:
                if ex['name'] in [m['name'] for m in selected_moves]:
                    continue
                
                utility = 0
                for muscle, val in ex['impact'].items():
                    utility += min(val, max(0, deficits.get(muscle, 0)))
                for muscle, val in ex['secondary'].items():
                    utility += min(val, max(0, deficits.get(muscle, 0)))
                
                if utility > best_score:
                    best_score = utility
                    best_candidates = [ex]
                elif utility == best_score and best_score > 0:
                    best_candidates.append(ex)
            
            if not best_candidates:
                break
                
            chosen = random.choice(best_candidates)
            selected_moves.append(chosen)
            
            for m, val in chosen['impact'].items():
                current_volume[m] += val
            for m, val in chosen['secondary'].items():
                current_volume[m] += val

        # 3. DISTRIBUTION & DEEP COPY (The Critical Fix)
        random.shuffle(selected_moves)
        low, high = map(int, self.target_reps.split('-'))
        program = {"weeks": {}}

        # Create a TEMPLATE for Day structures
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

        # Assign deep copies to every week
        for w in range(1, 7):
            program["weeks"][f"Week {w}"] = copy.deepcopy(week_template)
        
        return {"program": program, "volume_report": current_volume}

    def get_single_swap(self, current_name, all_week_exercise_names):
        """Finds the best alternative based on current weekly deficits."""
        pool = [ex for ex in MASTER_LIBRARY if ex['equip'] in self.equipment]
        current_vol = {m: 0.0 for m in self.targets.keys()}
        
        for name in all_week_exercise_names:
            if name == current_name: continue
            ex_data = next((x for x in MASTER_LIBRARY if x['name'] == name), None)
            if ex_data:
                for m, val in ex_data.get('impact', {}).items():
                    current_vol[m] += val
                for m, val in ex_data.get('secondary', {}).items():
                    current_vol[m] += val

        deficits = {m: self.targets[m] - current_vol[m] for m in self.targets}
        best_score, best_candidates = -1, []
        
        for ex in pool:
            if ex['name'] in all_week_exercise_names: continue
            score = 0
            for muscle, val in ex.get('impact', {}).items():
                score += min(val, max(0, deficits.get(muscle, 0)))
            for muscle, val in ex.get('secondary', {}).items():
                score += min(val, max(0, deficits.get(muscle, 0)))
                
            if score > best_score:
                best_score, best_candidates = score, [ex]
            elif score == best_score and score >= 0:
                best_candidates.append(ex)
        
        if not best_candidates: return None
        chosen = random.choice(best_candidates)
        low, high = map(int, self.target_reps.split('-'))
        
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

    def calculate_volume_report(self, workout_names):
        report = {m: 0.0 for m in self.targets.keys()}
        for name in workout_names:
            ex_data = next((x for x in MASTER_LIBRARY if x['name'] == name), None)
            if ex_data:
                for muscle, val in ex_data.get('impact', {}).items():
                    report[muscle] += val
                for muscle, val in ex_data.get('secondary', {}).items():
                    report[muscle] += val
        return report