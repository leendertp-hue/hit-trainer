import random
from exercises import MASTER_LIBRARY

class HITEngine:
    def __init__(self, days, equipment, target_reps):
        self.days = days
        self.equipment = equipment
        self.target_reps = target_reps
        
        # --- DYNAMIC VOLUME SCALING ---
        # 2 days = 2 units. 3-4 days = 4 units. 5 days = 5 units. 6-7 days = 6 units.
        if self.days == 2:
            vol = 2
        elif self.days in [3, 4]:
            vol = 4
        elif self.days == 5:
            vol = 5
        else: # 6 or 7 days
            vol = 6
            
        # Major muscle groups to track (Lats merged into Upper Back)
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
        """Generates a 6-week block based on global utility scoring."""
        # 1. Gear Filter
        pool = [ex for ex in MASTER_LIBRARY if ex['equip'] in self.equipment]
        current_volume = {m: 0.0 for m in self.targets.keys()}
        selected_moves = []

 # --- NEW ERROR CHECK ---
        # Calculate the maximum possible stimulus units available with this gear
        total_possible_units = {m: 0.0 for m in self.targets.keys()}
        for ex in pool:
            for m, val in ex['impact'].items():
                if m in total_possible_units: total_possible_units[m] += val
            for m, val in ex['secondary'].items():
                if m in total_possible_units: total_possible_units[m] += val
        
        # Find which muscles can't be hit
        missing_muscles = [m for m, target in self.targets.items() if total_possible_units[m] < target]
        
        if missing_muscles:
            return {
                "error": "Insufficient Equipment",
                "missing": missing_muscles,
                "details": f"Your current equipment selection cannot provide enough volume for: {', '.join(missing_muscles)}."
            }
        # --- END ERROR CHECK ---       



        # 2. UTILITY-BASED SELECTION LOOP
        while True:
            deficits = {m: self.targets[m] - current_volume[m] for m in self.targets}
            
            if max(deficits.values()) <= 0:
                break
            
            best_score = 0
            best_candidates = []
            
            for ex in pool:
                # Don't pick the same exercise twice in one week
                if ex['name'] in [m['name'] for m in selected_moves]:
                    continue
                
                # Calculate Utility: (Impact * Needed)
                current_utility = 0
                for muscle, val in ex['impact'].items():
                    current_utility += min(val, max(0, deficits.get(muscle, 0)))
                
                for muscle, val in ex['secondary'].items():
                    current_utility += min(val, max(0, deficits.get(muscle, 0)))
                
                if current_utility > best_score:
                    best_score = current_utility
                    best_candidates = [ex]
                elif current_utility == best_score and best_score > 0:
                    best_candidates.append(ex)
            
            if not best_candidates:
                break
                
            chosen = random.choice(best_candidates)
            selected_moves.append(chosen)
            
            # Update volume tracker
            for m, val in chosen['impact'].items():
                if m in current_volume: current_volume[m] += val
            for m, val in chosen['secondary'].items():
                if m in current_volume: current_volume[m] += val

        # 3. DISTRIBUTION INTO 6-WEEK BLOCK
        random.shuffle(selected_moves)
        low, high = map(int, self.target_reps.split('-'))
        program = {"weeks": {}}

        for w in range(1, 7):
            wk_key = f"Week {w}"
            program["weeks"][wk_key] = {}
            for d in range(1, self.days + 1):
                d_key = f"Day {d}"
                # Distribute moves using slicing
                moves_for_day = selected_moves[d-1::self.days]
                
                program["weeks"][wk_key][d_key] = [
                    {
                        "name": ex['name'],
                        "target_reps": random.randint(low, high),
                        "target_weight": 0.0,
                        "e1rm": 0.0
                    } for ex in moves_for_day
                ]
        
        return {
            "program": program,
            "volume_report": current_volume 
        }

    def get_single_swap(self, current_name, all_week_exercise_names):
        """Utility-driven surgical swap: finds the best filler for the week's deficit."""
        pool = [ex for ex in MASTER_LIBRARY if ex['equip'] in self.equipment]
        
        # 1. Calculate current volume for the week MINUS the exercise being swapped
        current_vol = {m: 0.0 for m in self.targets.keys()}
        for name in all_week_exercise_names:
            if name == current_name:
                continue
            
            ex_data = next((x for x in MASTER_LIBRARY if x['name'] == name), None)
            if ex_data:
                for m, val in ex_data.get('impact', {}).items():
                    if m in current_vol: current_vol[m] += val
                for m, val in ex_data.get('secondary', {}).items():
                    if m in current_vol: current_vol[m] += val

        # 2. Identify the Deficits
        deficits = {m: self.targets[m] - current_vol[m] for m in self.targets}
        
        # 3. Score candidates based on utility
        best_score = -1
        best_candidates = []
        
        for ex in pool:
            if ex['name'] in all_week_exercise_names:
                continue
                
            score = 0
            for muscle, val in ex.get('impact', {}).items():
                score += min(val, max(0, deficits.get(muscle, 0)))
            for muscle, val in ex.get('secondary', {}).items():
                score += min(val, max(0, deficits.get(muscle, 0)))
                
            if score > best_score:
                best_score = score
                best_candidates = [ex]
            elif score == best_score and score >= 0:
                best_candidates.append(ex)
        
        if not best_candidates:
            return None
            
        chosen = random.choice(best_candidates)
        low, high = map(int, self.target_reps.split('-'))
        
        return {
            "name": chosen['name'],
            "target_reps": random.randint(low, high),
            "target_weight": 0.0,
            "e1rm": 0.0
        }

    def calculate_volume_report(self, workout_names):
        """Calculates total weekly stimulus units from a list of exercise names."""
        report = {m: 0.0 for m in self.targets.keys()}
        
        for name in workout_names:
            ex_data = next((x for x in MASTER_LIBRARY if x['name'] == name), None)
            if ex_data:
                for muscle, val in ex_data.get('impact', {}).items():
                    if muscle in report: 
                        report[muscle] += val
                for muscle, val in ex_data.get('secondary', {}).items():
                    if muscle in report: 
                        report[muscle] += val
                        
        return report