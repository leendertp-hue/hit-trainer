
        # ==========================================
    # 대퇴사두근 (QUADS)
    # ==========================================
MASTER_LIBRARY = [
    # --- SELECTORIZED ---
    {"name": "Leg Extension", "impact": {"Quads": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},
    {"name": "Seated Leg Press (Horizontal)", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.4}, "equip": "Selectorized", "gentle": True},
    {"name": "Sissy Squat Machine", "impact": {"Quads": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},

    # --- PLATE-LOADED / SLED ---
    {"name": "Leg Press (45-Degree Sled)", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.4, "Calves": 0.4}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Hack Squat Machine", "impact": {"Quads": 1.2}, "secondary": {"Hamstrings/Glutes": 0.4}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Pendulum Squat", "impact": {"Quads": 1.3}, "secondary": {"Hamstrings/Glutes": 0.3}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "V-Squat Machine", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.6}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Belt Squat", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.5}, "equip": "Plate-Loaded", "gentle": True},

    # --- BARBELL ---
    {"name": "Barbell Back Squat", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.6, "Upper Back": 0.4}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Front Squat", "impact": {"Quads": 1.1}, "secondary": {"Upper Back": 0.7, "Hamstrings/Glutes": 0.3}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Walking Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.8}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Stationary Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.6}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Box Squat", "impact": {"Quads": 0.9}, "secondary": {"Hamstrings/Glutes": 0.8}, "equip": "Barbell", "gentle": False},

    # --- SMITH MACHINE ---
    {"name": "Smith Machine Squat", "impact": {"Quads": 1.1}, "secondary": {"Hamstrings/Glutes": 0.4}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Bulgarian Split Squat", "impact": {"Quads": 1.1}, "secondary": {"Hamstrings/Glutes": 0.6}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Walking Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.8}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Stationary Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.6}, "equip": "Smith Machine", "gentle": True},

    # --- DUMBBELLS ---
    {"name": "Dumbbell Goblet Squat", "impact": {"Quads": 1.0}, "secondary": {"Upper Back": 0.4}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Bulgarian Split Squat", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.7}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Walking Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.8}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Stationary Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.6}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Step-Ups", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.6}, "equip": "Dumbbells", "gentle": False},

# --- BODYWEIGHT (Density & Discovery) ---
    {"name": "Air Squats", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.4}, "equip": "Bodyweight", "gentle": True},
    {"name": "Cyclist Squats (Heels Elevated)", "impact": {"Quads": 1.2}, "secondary": {}, "equip": "Bodyweight", "gentle": True},
    {"name": "Sissy Squat (Bodyweight)", "impact": {"Quads": 1.3}, "secondary": {}, "equip": "Bodyweight", "gentle": False},
    
    # Lunge Variations
    {"name": "Bodyweight Reverse Lunges", "impact": {"Quads": 0.9}, "secondary": {"Hamstrings/Glutes": 0.7}, "equip": "Bodyweight", "gentle": True},
    {"name": "Bodyweight Forward Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.6}, "equip": "Bodyweight", "gentle": True},
    {"name": "Bodyweight Walking Lunges", "impact": {"Quads": 1.0}, "secondary": {"Hamstrings/Glutes": 0.8}, "equip": "Bodyweight", "gentle": True},
    {"name": "Bodyweight Side Lunges", "impact": {"Quads": 0.8}, "secondary": {"Adductors": 0.6, "Hamstrings/Glutes": 0.4}, "equip": "Bodyweight", "gentle": True},
    
    # Step-Up Variations
    {"name": "Step-Ups (Low Box)", "impact": {"Quads": 0.9}, "secondary": {"Hamstrings/Glutes": 0.5}, "equip": "Bodyweight", "gentle": True},
    {"name": "Step-Ups (High Box)", "impact": {"Quads": 1.1}, "secondary": {"Hamstrings/Glutes": 0.8}, "equip": "Bodyweight", "gentle": False},
    {"name": "Lateral Step-Ups", "impact": {"Quads": 1.0}, "secondary": {"Glute Medius": 0.6}, "equip": "Bodyweight", "gentle": True},
    # ==========================================
    # 햄스트링 & 둔근 (HAMS & GLUTES)
    # ==========================================

    # --- SELECTORIZED (Knee Flexion) ---
    {"name": "Seated Leg Curl", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},
    {"name": "Lying Leg Curl", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},
    {"name": "Standing Leg Curl", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},
    {"name": "Glute Kickback Machine", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},

    # --- PLATE-LOADED / SLED ---
    {"name": "Machine Hip Thrust", "impact": {"Hamstrings/Glutes": 1.2}, "secondary": {"Quads": 0.3}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Plate-Loaded Glute Driver", "impact": {"Hamstrings/Glutes": 1.1}, "secondary": {"Quads": 0.2}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "45-Degree Hyperextension (Weighted)", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {"Upper Back": 0.4}, "equip": "Plate-Loaded", "gentle": True},

    # --- BARBELL (The Heavy Hinges) ---
    {"name": "Barbell Romanian Deadlift (RDL)", "impact": {"Hamstrings/Glutes": 1.2}, "secondary": {"Upper Back": 0.5, "Forearms": 0.4}, "equip": "Barbell", "gentle": False},
    {"name": "Stiff-Leg Deadlift", "impact": {"Hamstrings/Glutes": 1.3}, "secondary": {"Upper Back": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Good Mornings", "impact": {"Hamstrings/Glutes": 1.1}, "secondary": {"Upper Back": 0.6}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Hip Thrust", "impact": {"Hamstrings/Glutes": 1.2}, "secondary": {"Quads": 0.3}, "equip": "Barbell", "gentle": False},

    # --- SMITH MACHINE ---
    {"name": "Smith Machine RDL", "impact": {"Hamstrings/Glutes": 1.1}, "secondary": {"Upper Back": 0.3}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Good Mornings", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {"Upper Back": 0.5}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Hip Thrust", "impact": {"Hamstrings/Glutes": 1.1}, "secondary": {"Quads": 0.2}, "equip": "Smith Machine", "gentle": True},

    # --- DUMBBELLS ---
    {"name": "Dumbbell RDL", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {"Forearms": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Single-Leg Dumbbell RDL", "impact": {"Hamstrings/Glutes": 1.0}, "secondary": {"Abs": 0.4}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Glute Bridge", "impact": {"Hamstrings/Glutes": 0.9}, "secondary": {}, "equip": "Dumbbells", "gentle": True},
    
    # --- BODYWEIGHT (Density) ---
    {"name": "Glute Ham Raise (GHR)", "impact": {"Hamstrings/Glutes": 1.3}, "secondary": {}, "equip": "Bodyweight", "gentle": False},
    {"name": "Nordic Hamstring Curl", "impact": {"Hamstrings/Glutes": 1.4}, "secondary": {}, "equip": "Bodyweight", "gentle": False},
    {"name": "Bodyweight Hyperextension", "impact": {"Hamstrings/Glutes": 0.8}, "secondary": {"Upper Back": 0.3}, "equip": "Bodyweight", "gentle": True},
    {"name": "Single-Leg Glute Bridge", "impact": {"Hamstrings/Glutes": 0.9}, "secondary": {}, "equip": "Bodyweight", "gentle": True},

    # ==========================================
    # 어깨 (FRONT, SIDE, & REAR DELTS)
    # ==========================================

    # --- THE ALL-ROUNDERS (High Versatility) ---
    {"name": "Barbell Upright Row", "impact": {"Side Delts": 1.0, "Front Delts": 1.0}, "secondary": {"Rear Delts": 0.4, "Biceps": 0.4}, "equip": "Barbell", "gentle": False},
    {"name": "Dumbbell Arnold Press", "impact": {"Front Delts": 1.0, "Side Delts": 1.0}, "secondary": {"Triceps": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Smith Machine Behind-the-Neck Press", "impact": {"Side Delts": 1.0, "Front Delts": 1.0}, "secondary": {"Triceps": 0.5}, "equip": "Smith Machine", "gentle": False},
    {"name": "Cable Face Pulls", "impact": {"Rear Delts": 1.0, "Side Delts": 0.8}, "secondary": {"Upper Back": 0.6}, "equip": "Cables", "gentle": True},

    # --- SELECTORIZED ---
    {"name": "Machine Shoulder Press", "impact": {"Front Delts": 1.0}, "secondary": {"Side Delts": 0.4, "Triceps": 0.5}, "equip": "Selectorized", "gentle": True},
    {"name": "Machine Lateral Raise", "impact": {"Side Delts": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},
    {"name": "Rear Delt Fly (Pec Deck Machine)", "impact": {"Rear Delts": 1.0}, "secondary": {"Upper Back": 0.4}, "equip": "Selectorized", "gentle": True},

    # --- PLATE-LOADED ---
    {"name": "Plate-Loaded Shoulder Press", "impact": {"Front Delts": 1.1}, "secondary": {"Side Delts": 0.4, "Triceps": 0.5}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Plate-Loaded Lateral Raise", "impact": {"Side Delts": 1.0}, "secondary": {}, "equip": "Plate-Loaded", "gentle": True},

    # --- BARBELL ---
    {"name": "Barbell Overhead Press (Standing)", "impact": {"Front Delts": 1.0}, "secondary": {"Side Delts": 0.5, "Triceps": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Overhead Press (Seated)", "impact": {"Front Delts": 1.0}, "secondary": {"Side Delts": 0.5, "Triceps": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Rear Delt Row", "impact": {"Rear Delts": 1.1}, "secondary": {"Upper Back": 0.6}, "equip": "Barbell", "gentle": False},

    # --- SMITH MACHINE ---
    {"name": "Smith Machine Shoulder Press", "impact": {"Front Delts": 1.1}, "secondary": {"Side Delts": 0.4, "Triceps": 0.4}, "equip": "Smith Machine", "gentle": True},

    # --- DUMBBELLS ---
    {"name": "Dumbbell Shoulder Press", "impact": {"Front Delts": 1.0}, "secondary": {"Side Delts": 0.4, "Triceps": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Lateral Raise", "impact": {"Side Delts": 1.0}, "secondary": {"Front Delts": 0.2}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Rear Delt Fly", "impact": {"Rear Delts": 1.0}, "secondary": {"Upper Back": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Front Raise", "impact": {"Front Delts": 1.0}, "secondary": {"Pectorals": 0.2}, "equip": "Dumbbells", "gentle": False},

    # --- CABLES ---
    {"name": "Cable Lateral Raise", "impact": {"Side Delts": 1.2}, "secondary": {}, "equip": "Cables", "gentle": True},
    {"name": "Cable Front Raise", "impact": {"Front Delts": 1.0}, "secondary": {}, "equip": "Cables", "gentle": True},

    # --- BODYWEIGHT ---
    {"name": "Pike Push-Ups", "impact": {"Front Delts": 1.0}, "secondary": {"Triceps": 0.5}, "equip": "Bodyweight", "gentle": False},
    {"name": "Handstand Push-Ups", "impact": {"Front Delts": 1.2}, "secondary": {"Triceps": 0.6, "Side Delts": 0.5}, "equip": "Bodyweight", "gentle": False},

    # ==========================================
    # 흉근 (PECTORALS)
    # ==========================================

    # --- SELECTORIZED ---
    {"name": "Machine Chest Press (Seated)", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Selectorized", "gentle": True},
    {"name": "Machine Chest Press (Flat)", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Selectorized", "gentle": True},
    {"name": "Machine Incline Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Selectorized", "gentle": True},
    {"name": "Machine Chest Fly", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.3}, "equip": "Selectorized", "gentle": True},
    {"name": "Pec Deck (Old School)", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.3}, "equip": "Selectorized", "gentle": True},
    {"name": "Triceps Dip Machine (Seated)", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.3}, "equip": "Selectorized", "gentle": True},

    # --- PLATE-LOADED ---
    {"name": "Plate-Loaded Seated Chest Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Plate-Loaded Flat Bench Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Plate-Loaded Incline Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Plate-Loaded Weighted Dip", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.5}, "equip": "Plate-Loaded", "gentle": True},

    # --- BARBELL ---
    {"name": "Barbell Bench Press (Standard Grip)", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Bench Press (Narrow Grip)", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Incline Press (Standard Grip)", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Incline Press (Narrow Grip)", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Bench Press (Inverted Grip)", "impact": {"Pectorals": 1.0}, "secondary": {"Triceps": 0.6, "Front Delts": 0.3}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Decline Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Barbell", "gentle": False},

    # --- SMITH MACHINE ---
    {"name": "Smith Machine Flat Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.4, "Triceps": 0.4}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Flat Press (Narrow Grip)", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.4}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Incline Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.4}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Incline Press (Narrow Grip)", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.5}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Decline Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.3, "Triceps": 0.4}, "equip": "Smith Machine", "gentle": True},

    # --- DUMBBELLS ---
    {"name": "Dumbbell Flat Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Incline Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Decline Press", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.5, "Triceps": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Flat Flyes", "impact": {"Pectorals": 1.0}, "secondary": {}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Incline Flyes", "impact": {"Pectorals": 1.0}, "secondary": {}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Decline Flyes", "impact": {"Pectorals": 1.0}, "secondary": {}, "equip": "Dumbbells", "gentle": False},
    {"name": "Weighted Dips (DB)", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.5}, "equip": "Dumbbells", "gentle": False},

    # --- CABLES ---
    {"name": "Cable Crossover (High-to-Low)", "impact": {"Pectorals": 1.0}, "secondary": {}, "equip": "Cables", "gentle": True},
    {"name": "Cable Crossover (Low-to-High)", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.4}, "equip": "Cables", "gentle": True},

    # --- BODYWEIGHT ---
    {"name": "Push-Ups (Standard)", "impact": {"Pectorals": 1.0}, "secondary": {"Triceps": 0.5, "Front Delts": 0.5}, "equip": "Bodyweight", "gentle": True},
    {"name": "Dips (Bodyweight Chest focus)", "impact": {"Pectorals": 1.0, "Triceps": 1.0}, "secondary": {"Front Delts": 0.5}, "equip": "Bodyweight", "gentle": False},
    {"name": "Push-Ups (Wide Grip)", "impact": {"Pectorals": 1.1}, "secondary": {"Front Delts": 0.6}, "equip": "Bodyweight", "gentle": False},
    {"name": "Push-Ups (Diamond)", "impact": {"Triceps": 1.0}, "secondary": {"Pectorals": 0.6, "Front Delts": 0.5}, "equip": "Bodyweight", "gentle": True},
    {"name": "Push-Ups (Decline - Feet Elevated)", "impact": {"Pectorals": 1.0}, "secondary": {"Front Delts": 0.6, "Triceps": 0.5}, "equip": "Bodyweight", "gentle": False},
    {"name": "Push-Ups (Incline - Hands Elevated)", "impact": {"Pectorals": 0.8}, "secondary": {"Triceps": 0.4}, "equip": "Bodyweight", "gentle": True},
    {"name": "Push-Ups (Deficit)", "impact": {"Pectorals": 1.2}, "secondary": {"Front Delts": 0.6, "Triceps": 0.5}, "equip": "Bodyweight", "gentle": False},
    {"name": "Archer Push-Ups", "impact": {"Pectorals": 1.2}, "secondary": {"Triceps": 0.6, "Front Delts": 0.6}, "equip": "Bodyweight", "gentle": False},

    # ==========================================
    # 삼두근 (TRICEPS - Isolation Focus)
    # ==========================================

    # --- SELECTORIZED ---
    {"name": "Triceps Pushdown (Cable Machine)", "impact": {"Triceps": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},
    {"name": "Overhead Triceps Extension (Machine)", "impact": {"Triceps": 1.1}, "secondary": {}, "equip": "Selectorized", "gentle": True},

    # --- BARBELL ---
    {"name": "Barbell Skull Crushers (Flat)", "impact": {"Triceps": 1.1}, "secondary": {"Forearms": 0.3}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Skull Crushers (Incline)", "impact": {"Triceps": 1.1}, "secondary": {"Forearms": 0.3}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell JM Press", "impact": {"Triceps": 1.2}, "secondary": {"Pectorals": 0.3, "Front Delts": 0.3}, "equip": "Barbell", "gentle": False},

    # --- SMITH MACHINE ---
    {"name": "Smith Machine JM Press", "impact": {"Triceps": 1.2}, "secondary": {"Front Delts": 0.3}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Skull Crushers", "impact": {"Triceps": 1.0}, "secondary": {}, "equip": "Smith Machine", "gentle": True},

    # --- DUMBBELLS ---
    {"name": "Dumbbell Overhead Extension (Seated)", "impact": {"Triceps": 1.1}, "secondary": {}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Skull Crushers", "impact": {"Triceps": 1.0}, "secondary": {}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Tate Press", "impact": {"Triceps": 1.0}, "secondary": {}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Kickbacks", "impact": {"Triceps": 0.8}, "secondary": {}, "equip": "Dumbbells", "gentle": True},

    # --- CABLES ---
    {"name": "Cable Rope Pushdown", "impact": {"Triceps": 1.0}, "secondary": {"Forearms": 0.3}, "equip": "Cables", "gentle": True},
    {"name": "Cable Overhead Extension (Rope)", "impact": {"Triceps": 1.2}, "secondary": {}, "equip": "Cables", "gentle": True},
    {"name": "Cable Straight Bar Pushdown", "impact": {"Triceps": 1.0}, "secondary": {}, "equip": "Cables", "gentle": True},
    {"name": "Single Arm Cable Extension (Lateral Head)", "impact": {"Triceps": 1.0}, "secondary": {}, "equip": "Cables", "gentle": True},

    # --- BODYWEIGHT ---
    {"name": "Bench Dips", "impact": {"Triceps": 1.0}, "secondary": {"Front Delts": 0.4}, "equip": "Bodyweight", "gentle": True},
    {"name": "Bodyweight Skull Crushers (on bar)", "impact": {"Triceps": 1.1}, "secondary": {"Abs": 0.3}, "equip": "Bodyweight", "gentle": False},

    # ==========================================
    # 등 (UPPER BACK & LATS)
    # ==========================================

    # --- SELECTORIZED ---
    {"name": "Seated Machine Row (Overhand Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.6, "Biceps": 0.4}, "equip": "Selectorized", "gentle": True},
    {"name": "Seated Machine Row (Neutral/Close Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.6, "Rear Delts": 0.4}, "equip": "Selectorized", "gentle": True},
    {"name": "Seated Machine Row (Underhand Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.8, "Rear Delts": 0.3}, "equip": "Selectorized", "gentle": True},
    {"name": "Lat Pulldown (Wide Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.5, "Biceps": 0.5}, "equip": "Selectorized", "gentle": True},
    {"name": "Lat Pulldown (Neutral/V-Bar)", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.7, "Rear Delts": 0.4}, "equip": "Selectorized", "gentle": True},
    {"name": "Lat Pulldown (Underhand)", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.8}, "equip": "Selectorized", "gentle": True},

    # --- PLATE-LOADED ---
    {"name": "Plate-Loaded Lat Pulldown", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.4, "Biceps": 0.5}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Plate-Loaded Seated Row", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.5, "Biceps": 0.5}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "Plate-Loaded High Row", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.6, "Biceps": 0.4}, "equip": "Plate-Loaded", "gentle": True},
    {"name": "T-Bar Row (Chest Supported)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.5, "Biceps": 0.5}, "equip": "Plate-Loaded", "gentle": True},

    # --- BARBELL & LANDMINE ---
    {"name": "Barbell Row (Overhand Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.6, "Biceps": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Row (Underhand Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.8, "Rear Delts": 0.4}, "equip": "Barbell", "gentle": False},
    {"name": "Meadows Row (Landmine)", "impact": {"Upper Back": 1.1}, "secondary": {"Rear Delts": 0.6, "Forearms": 0.5}, "equip": "Barbell", "gentle": False},
    {"name": "Pendlay Row", "impact": {"Upper Back": 1.2}, "secondary": {"Hamstrings/Glutes": 0.4}, "equip": "Barbell", "gentle": False},
    {"name": "T-Bar Row (Landmine/Old School)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.5, "Biceps": 0.5}, "equip": "Barbell", "gentle": False},

    # --- SMITH MACHINE ---
    {"name": "Smith Machine Row (Overhand Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.6, "Biceps": 0.4}, "equip": "Smith Machine", "gentle": True},
    {"name": "Smith Machine Row (Underhand Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.8, "Rear Delts": 0.4}, "equip": "Smith Machine", "gentle": True},

    # --- DUMBBELLS ---
    {"name": "One-Arm Dumbbell Row", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.5, "Biceps": 0.5, "Forearms": 0.5}, "equip": "Dumbbells", "gentle": False},
    {"name": "Incline Dumbbell Row", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.6, "Biceps": 0.5}, "equip": "Dumbbells", "gentle": True},
    {"name": "Dumbbell Pullover (Lat focus)", "impact": {"Upper Back": 1.0}, "secondary": {"Triceps": 0.3, "Pectorals": 0.2}, "equip": "Dumbbells", "gentle": True},

    # --- CABLES ---
    {"name": "Single Arm Cable Row (Bottom Pulley)", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.5, "Forearms": 0.3}, "equip": "Cables", "gentle": True},
    {"name": "Straight Arm Cable Pulldown (Top Pulley)", "impact": {"Upper Back": 1.0}, "secondary": {"Triceps": 0.4}, "equip": "Cables", "gentle": True},
    {"name": "Cable Pullover (Lying on bench)", "impact": {"Upper Back": 1.0}, "secondary": {"Triceps": 0.3}, "equip": "Cables", "gentle": True},

    # --- BODYWEIGHT ---
    {"name": "Pull-Ups (Wide Grip)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.5, "Biceps": 0.5}, "equip": "Bodyweight", "gentle": False},
    {"name": "Chin-Ups (Underhand)", "impact": {"Upper Back": 1.0, "Biceps": 1.0}, "secondary": {"Rear Delts": 0.3}, "equip": "Bodyweight", "gentle": False},
    {"name": "Neutral Grip Pull-Ups", "impact": {"Upper Back": 1.0}, "secondary": {"Biceps": 0.7, "Rear Delts": 0.5}, "equip": "Bodyweight", "gentle": False},
    {"name": "Inverted Row (Aussie Pull-ups)", "impact": {"Upper Back": 1.0}, "secondary": {"Rear Delts": 0.6, "Biceps": 0.5}, "equip": "Bodyweight", "gentle": True},

    # ==========================================
    # 이두근 (BICEPS & FOREARMS)
    # ==========================================

    # --- SELECTORIZED ---
    {"name": "Machine Bicep Curl", "impact": {"Biceps": 1.0}, "secondary": {}, "equip": "Selectorized", "gentle": True},
    {"name": "Machine Preacher Curl", "impact": {"Biceps": 1.1}, "secondary": {}, "equip": "Selectorized", "gentle": True},

    # --- BARBELL ---
    {"name": "Barbell Bicep Curl (Straight Bar)", "impact": {"Biceps": 1.0}, "secondary": {"Forearms": 0.4}, "equip": "Barbell", "gentle": False},
    {"name": "EZ-Bar Bicep Curl", "impact": {"Biceps": 1.0}, "secondary": {"Forearms": 0.3}, "equip": "Barbell", "gentle": True},
    {"name": "Barbell Reverse Curl", "impact": {"Biceps": 0.7}, "secondary": {"Forearms": 1.0}, "equip": "Barbell", "gentle": False},
    {"name": "Barbell Preacher Curl", "impact": {"Biceps": 1.1}, "secondary": {"Forearms": 0.3}, "equip": "Barbell", "gentle": False},

    # --- SMITH MACHINE ---
    {"name": "Smith Machine Drag Curl", "impact": {"Biceps": 1.1}, "secondary": {"Rear Delts": 0.3}, "equip": "Smith Machine", "gentle": True},

    # --- DUMBBELLS ---
    {"name": "Dumbbell Alternating Curl", "impact": {"Biceps": 1.0}, "secondary": {"Forearms": 0.3}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Hammer Curl", "impact": {"Biceps": 0.8}, "secondary": {"Forearms": 1.0}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Incline Curl", "impact": {"Biceps": 1.2}, "secondary": {}, "equip": "Dumbbells", "gentle": False},
    {"name": "Dumbbell Concentration Curl", "impact": {"Biceps": 1.0}, "secondary": {}, "equip": "Dumbbells", "gentle": True},

    # --- CABLES ---
    {"name": "Cable Bicep Curl (Straight Bar)", "impact": {"Biceps": 1.0}, "secondary": {}, "equip": "Cables", "gentle": True},
    {"name": "Cable Rope Hammer Curl", "impact": {"Biceps": 0.8}, "secondary": {"Forearms": 1.0}, "equip": "Cables", "gentle": True},
    {"name": "Cable Behind-the-Back Curl", "impact": {"Biceps": 1.2}, "secondary": {}, "equip": "Cables", "gentle": True}]