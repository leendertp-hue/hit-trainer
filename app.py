import streamlit as st
import json, time, hashlib
from supabase import create_client, Client
from exercises import MASTER_LIBRARY

# --- SUPABASE SETUP ---
# These will be set in Streamlit Cloud Settings > Secrets
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(URL, KEY)

# --- HELPER FUNCTIONS ---
def get_user_data(username):
    res = supabase.table("users").select("*").eq("username", username).execute()
    return res.data[0] if res.data else None

def save_program_to_cloud(username, program_json, week, day, has_prog=1):
    data = {
        "username": username,
        "program_data": program_json,
        "current_week": week,
        "current_day": day,
        "has_program": has_prog
    }
    # Upsert handles both first-time save and updates
    supabase.table("users").upsert(data, on_conflict="username").execute()

# --- AUTHENTICATION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🛡️ HIT Adaptive Trainer")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        u_log = st.text_input("Username", key="login_u")
        p_log = st.text_input("Password", type='password', key="login_p")
        if st.button("Login"):
            pwd_hash = hashlib.sha256(p_log.encode()).hexdigest()
            user_data = get_user_data(u_log)
            if user_data and user_data['password'] == pwd_hash:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u_log
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u_sign = st.text_input("New Username", key="sign_u")
        p_sign = st.text_input("New Password", type='password', key="sign_p")
        if st.button("Create Account"):
            pwd_hash = hashlib.sha256(p_sign.encode()).hexdigest()
            if get_user_data(u_sign):
                st.error("Username already exists.")
            else:
                supabase.table("users").insert({
                    "username": u_sign, 
                    "password": pwd_hash, 
                    "has_program": 0, 
                    "current_week": 1, 
                    "current_day": 1
                }).execute()
                st.success("Account created! Please login.")
    st.stop()

# --- LOGGED IN CONTENT ---
# --- LOGGED IN CONTENT ---
user = st.session_state['username']
user_data = get_user_data(user)

has_program = user_data['has_program']
week_num = user_data['current_week']
day_num = user_data['current_day']

if has_program:
    # Pull the program JSON from the cloud if not in session state
    if 'current_program' not in st.session_state:
        st.session_state.current_program = user_data['program_data']
    prog = st.session_state.current_program


# --- BRANCH 1: PROGRAM GENERATION / BUILDING ---
if not has_program:
    st.title("🏋️‍♂️ Get Started")
    mode = st.radio("How do you want to start?", ["Auto-Generate Plan", "Build Manual Plan"])

    # Shared settings
    goal = st.selectbox("Training Goal", ["Strength (5-8 reps)", "Hypertrophy (8-12 reps)", "Endurance (15-20 reps)"])
    rep_range = goal.split('(')[1].split(' ')[0] 
    low, high = map(int, rep_range.split('-'))
    days = st.select_slider("Workout Days Per Week", options=[2, 3, 4, 5, 6, 7], value=3)

    if mode == "Auto-Generate Plan":
        eq = st.multiselect("Available Equipment", ["Selectorized", "Plate-Loaded", "Cables", "Dumbbells", "Barbell", "Bodyweight", "Sled Machine", "Smith Machine"])
        if st.button("🚀 Generate My Plan"):
            from engine import HITEngine
            engine = HITEngine(days, eq, target_reps=rep_range)
            result = engine.generate_program()
            new_program = result["program"]
            
            # Save and Rerun
            save_program_to_cloud(user, new_program, 1, 1, has_prog=1)

    else:
        st.subheader("🛠️ Build Your Routine")
        custom_plan = {}
        all_library_names = [ex['name'] for ex in MASTER_LIBRARY]

        # Create input slots for each day
        for d in range(1, days + 1):
            with st.expander(f"📅 Day {d} Exercises", expanded=True):
                selected_for_day = st.multiselect(
                    f"Select exercises for Day {d}", 
                    options=all_library_names,
                    key=f"manual_day_{d}"
                )
                custom_plan[f"Day {d}"] = selected_for_day

        if st.button("💾 Save Manual Plan"):
            if any(len(v) == 0 for v in custom_plan.values()):
                st.error("Please add at least one exercise to every day!")
            else:
                # Create a lookup map from the library to check equipment
                lib_map = {ex['name']: ex for ex in MASTER_LIBRARY}
                
                structured_weeks = {"weeks": {}}
                for w in range(1, 7):
                    wk_key = f"Week {w}"
                    structured_weeks["weeks"][wk_key] = {}
                    for d_key, names in custom_plan.items():
                        day_exercises = []
                        for name in names:
                            ex_info = lib_map.get(name, {})
                            is_bw = ex_info.get('equip') == "Bodyweight"
                            is_weighted_bw = "Weighted" in name
                            
                            # If it's pure Bodyweight, we set target to 0 (to be filled by Discovery)
                            # Otherwise, use the standard middle-of-range rep target
                            if is_bw and not is_weighted_bw:
                                t_reps = 0 
                                p_type = "density"
                            else:
                                t_reps = (low + high) // 2
                                p_type = "standard"

                            day_exercises.append({
                                "name": name,
                                "prog_type": p_type,
                                "target_reps": t_reps,
                                "target_weight": 0.0,
                                "e1rm": 0.0,
                                "discovery_reps": 0 # The "Seed" for BW moves
                            })
                        
                        structured_weeks["weeks"][wk_key][d_key] = day_exercises
                
                save_program_to_cloud(user, structured_weeks, 1, 1, has_prog=1)
        


# --- BRANCH 2: ACTIVE TRAINING ---
else:
    # 1. LAZY LOAD JSON
    # We already fetched user_data at the top of the script!
    if 'current_program' not in st.session_state:
        st.session_state.current_program = user_data['program_data']
    
    prog = st.session_state.current_program

# 2. THE SMART GPS
    active_week, active_day = 1, 1 # Defaults
    found_spot = False
    
    for w_idx in range(1, 7):
        w_key = f"Week {w_idx}"
        # Filter keys to find how many "Days" are in this week
        days_in_week = [k for k in prog['weeks'][w_key].keys() if "Day" in k and "_status" not in k]
        
        for d_idx in range(1, len(days_in_week) + 1):
            d_key = f"Day {d_idx}"
            if prog['weeks'][w_key].get(f"{d_key}_status") != "completed":
                active_week, active_day = w_idx, d_idx
                found_spot = True
                break
        if found_spot: break

    # Sync to the variables the rest of the app uses
    week_num = active_week
    day_num = active_day
    # Initialize Engine for Swaps/Reports
    from engine import HITEngine
    # Logic to approximate original settings if they aren't in state
    settings = st.session_state.get("user_settings", {"days": 3, "eq": ["Dumbbells", "Cables", "Selectorized"], "rep_range": "8-12"})
    engine = HITEngine(settings['days'], settings['eq'], settings['rep_range'])

    # SIDEBAR VOLUME REPORT
    # Filter: Only grab exercise names from dictionary values that are actually lists
    all_week_names = []
    week1_data = st.session_state.current_program['weeks']['Week 1']
    
    for key, content in week1_data.items():
        if isinstance(content, list):
            for ex in content:
                all_week_names.append(ex['name'])

    report = engine.calculate_volume_report(all_week_names)
    
    with st.sidebar:
        st.subheader("📊 Weekly Stimulus")
        st.bar_chart(report)
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

        st.divider()
        st.subheader("📈 Strength Trends")
        
        # 1. Get a unique list of all exercise names in the program
        # We use a set to avoid duplicates
        ex_names = sorted(list(set(
            ex['name'] 
            for w in prog['weeks'].values() 
            for d in w.values() 
            if isinstance(d, list) 
            for ex in d
        )))
        
        selected_graph_ex = st.selectbox("Select Exercise to Track", ex_names)

        # 2. Extract the e1rm for that exercise for Weeks 1 through 6
        weeks_axis = []
        e1rm_axis = []
        
        for w_idx in range(1, 7):
            w_key = f"Week {w_idx}"
            found_in_week = False
            
            # Look through every day in that week
            for d_key, d_content in prog['weeks'][w_key].items():
                if isinstance(d_content, list):
                    for ex in d_content:
                        if ex['name'] == selected_graph_ex:
                            weeks_axis.append(w_key)
                            e1rm_axis.append(ex.get('e1rm', 0))
                            found_in_week = True
                            break
                if found_in_week: break
        
        # 3. Plot the data
        if e1rm_axis:
            # We create a dictionary for the chart
            chart_data = {"Week": weeks_axis, "e1RM (kg)": e1rm_axis}
            st.line_chart(data=chart_data, x="Week", y="e1RM (kg)")

    day_key = f"Day {day_num}"
    week_key = f"Week {week_num}"
    
    # Grab the current session exercises
    exs = st.session_state.current_program['weeks'][week_key][day_key]

    # UI HEADER
    has_baseline = any(ex.get('e1rm', 0) > 0 for ex in exs)
    st.title("🧪 Discovery Mode" if not has_baseline else f"🚀 Training Mode: W{week_num}")
    st.subheader(f"Session: {day_key}")

    session_results = []

    # --- START OF THE EXERCISE LOOP ---
    for i, ex in enumerate(exs):
        btn_id = f"swp_{i}_{week_num}_{day_num}_{ex['name'].replace(' ', '_')}"
        
        # Check if this is a Density exercise
        is_density = ex.get('prog_type') == "density"
        icon = "⏱️" if is_density else "🏋️"

        with st.expander(f"{icon} {ex['name']}", expanded=False):
            
            # --- 1. SMART SWAP BUTTON ---
            if week_num == 1:
                if st.button("🔄 Swap Exercise", key=btn_id):
                    all_week_names = []
                    for d_k, d_v in st.session_state.current_program["weeks"]["Week 1"].items():
                        if isinstance(d_v, list):
                            for m in d_v:
                                all_week_names.append(m['name'])
                    
                    new_move_data = engine.get_single_swap(ex['name'], all_week_names)
                    
                    if new_move_data:
                        for w in range(1, 7):
                            st.session_state.current_program["weeks"][f"Week {w}"][day_key][i] = new_move_data
                        
                        save_program_to_cloud(user, st.session_state.current_program, week_num, day_num)
                        
                        st.success(f"Optimized swap: {new_move_data['name']}")
                        st.rerun()
                    else:
                        st.error("No suitable alternative found in the library.")

            # --- 2. DYNAMIC TIMER & TARGET DISPLAY ---
            if is_density:
                # Bodyweight UI: 1 min Discovery (W1) or 5 min Density (W2+)
                if week_num == 1:
                    st.info("🎯 **Discovery:** Max reps in **1 Minute**.")
                    default_s = 60
                else:
                    st.success(f"🔥 **Goal:** {ex['target_reps']} Reps in **5 Minutes**.")
                    default_s = 300
                timer_label = "Start Work Block"
            else:
                # Weighted UI: Standard Rep Targets
                st.write(f"🎯 **Target:** {ex['target_reps']} reps @ {ex.get('target_weight', 0)}kg")
                t_reps = ex['target_reps']
                default_s = 180 if t_reps <= 6 else 120 if t_reps <= 12 else 90
                timer_label = f"Rest Timer ({default_s//60}m suggested)"

            with st.expander(f"⏱️ {timer_label}"):
                t_col1, t_col2, t_col3 = st.columns([1, 1, 1])
                with t_col1:
                    user_timer = st.number_input("Time (sec)", value=default_s, step=30, key=f"t_in_{i}")
                with t_col2:
                    if st.button("▶️ Start", key=f"t_start_{i}", use_container_width=True):
                        t_disp = st.empty()
                        for t in range(user_timer, -1, -1):
                            mm, ss = divmod(t, 60)
                            t_disp.subheader(f"⏳ {mm:02d}:{ss:02d}")
                            time.sleep(1)
                        t_disp.success("🏁 Time's Up!" if is_density else "🔥 Set Start!")
                with t_col3: 
                    if st.button("⏹️ Stop/Reset", key=f"t_stop_{i}", use_container_width=True):
                        st.rerun()

            # --- 3. DATA ENTRY ---
            if is_density:
                # No weight input for bodyweight
                r_act = st.number_input("Total Reps Achieved", key=f"r_in_{i}", step=1, value=0)
                w_act = 0.0
            else:
                col_w, col_r = st.columns(2)
                with col_w:
                    w_act = st.number_input("Weight (kg)", key=f"w_in_{i}", step=2.5, value=float(ex.get('target_weight', 0)))
                with col_r:
                    r_act = st.number_input("Reps", key=f"r_in_{i}", step=1, value=int(ex.get('target_reps', 10)))

            # Append results for the session_results list (used by Save & Finish button)
            session_results.append({
                "name": ex['name'],
                "weight": w_act,
                "reps": r_act,
                "is_density": is_density
            })

# --- 2. INSTRUCTIONS ---
            if is_density:
                # DENSITY INSTRUCTIONS (Bodyweight)
                if week_num == 1:
                    st.info("⏱️ **Discovery Mode:** Perform as many reps as possible in **1 Minute**. Don't pace yourself—go for broke. This baseline sets your volume for the next 5 weeks.")
                else:
                    st.markdown(f"""
                    ### 🎯 The Mission: **{ex['target_reps']} Reps**
                    **Time Domain:** 5-Minute Block
                    
                    * Perform the target reps as quickly as possible.
                    * Rest only as much as needed to keep your form perfect.
                    * If you finish before 5 minutes, you've beaten the density goal!
                    """)
            else:
                # STANDARD HIT INSTRUCTIONS (Weighted)
                if not (has_baseline and ex.get('target_weight', 0) > 0):
                    st.info("**Discovery Mode:** Find a weight that takes you to failure within your target rep range. This sets your baseline.")
                else:
                    st.metric("Suggested Load", f"{ex['target_weight']} kg")
                    st.markdown(f"""
                    ### 🎯 The Mission: **{ex['target_reps']} Reps**
                    This is your **Main Working Set**. To trigger progress, you must give 100% effort here.
                    
                    **Warm-up:** 1-2 lighter sets (50% and 75% load) to prep.
                    **The Rule:** Only the *first* set counts toward your progression math.
                    """)
            
            # Store the data for the Save & Finish function
            session_results.append({
                'name': ex['name'],
                'weight': w_act, 
                'reps': r_act, 
                'target_reps': ex['target_reps'],
                'is_density': is_density # Adding this flag makes the math step easier
            })
# --- FINISH SESSION ---
    st.divider()
    
    # 1. SMART CHECK: Weighted needs Weight > 0; Density only needs Reps > 0
    all_filled = all(
        (res['reps'] > 0 and res['weight'] > 0) if not res.get('is_density') 
        else res['reps'] > 0 
        for res in session_results
    )

    if st.button("✅ Save & Finish Session", 
                 disabled=not all_filled, 
                 use_container_width=True, 
                 key=f"save_btn_w{week_num}_d{day_num}"):
        
        prog = st.session_state.current_program
        prog['weeks'][week_key][day_key + "_status"] = "completed"
        
        # ... [Your existing math logic for Brzycki and Density multipliers] ...

        # Calculate next GPS spot
        actual_days = [k for k in prog['weeks']["Week 1"].keys() if "Day" in k and "_status" not in k]
        total_days_in_week = len(actual_days)
        
        if day_num < total_days_in_week:
            new_day, new_week = day_num + 1, week_num
        else:
            new_day, new_week = 1, week_num + 1

        # SAVE TO SUPABASE
        save_program_to_cloud(user, prog, new_week, new_day)
        
        st.success(f"Session Saved to Cloud!")
        st.balloons()
        time.sleep(1)
        st.rerun()
        
        # 2. UPDATE PROGRESSION (The Branching Logic)
        for res in session_results:
            if res.get('is_density'):
                # --- DENSITY MATH (Bodyweight) ---
                # If Week 1, this 'res['reps']' is our baseline seed.
                if week_num == 1:
                    baseline = res['reps']
                else:
                    # Look back at Week 1 to find the original baseline
                    # (This ensures calculations stay anchored to the discovery set)
                    baseline = res.get('discovery_reps', res['reps'])

                # Multipliers: W1=1.0x (1min), W2=3.0x (5min), W3=3.2x, W4=3.4x, W5=3.6x, W6=Deload
                multipliers = {1: 1.0, 2: 3.0, 3: 3.2, 4: 3.4, 5: 3.6, 6: 3.4}
                
                for w_idx in range(week_num, 7):
                    wk_key = f"Week {w_idx}"
                    if wk_key not in prog['weeks']: continue
                    
                    for d_k, d_v in prog['weeks'][wk_key].items():
                        if isinstance(d_v, list):
                            for ex_entry in d_v:
                                if ex_entry['name'] == res['name']:
                                    # Save baseline in Week 1 slot for future lookup
                                    if week_num == 1:
                                        ex_entry['discovery_reps'] = baseline
                                    
                                    # Update Target Reps based on the baseline seed
                                    # Example: 10 reps in 1 min becomes 32 reps in 5 mins for Week 3
                                    ex_entry['target_reps'] = int(baseline * multipliers.get(w_idx, 3.0))
                                    ex_entry['target_weight'] = 0.0
                                    ex_entry['e1rm'] = baseline # Using reps as e1rm for trend tracking
            
            else:
                # --- BRZYCKI MATH (Weighted) ---
                e1rm = res['weight'] * (36 / (37 - res['reps']))
                
                for w_idx in range(week_num, 7):
                    wk_key = f"Week {w_idx}"
                    if wk_key not in prog['weeks']: continue
                    for d_k, d_v in prog['weeks'][wk_key].items():
                        if isinstance(d_v, list):
                            for ex_entry in d_v:
                                if ex_entry['name'] == res['name']:
                                    ex_entry['e1rm'] = e1rm
                                    new_w = e1rm * (37 - ex_entry['target_reps']) / 36
                                    ex_entry['target_weight'] = round(new_w / 2.5) * 2.5

        # 3. DATABASE GPS & SAVE (Keep as is)
        actual_days = [k for k in prog['weeks']["Week 1"].keys() if "Day" in k and "_status" not in k]
        total_days_in_week = len(actual_days)
        
        if day_num < total_days_in_week:
            new_day, new_week = day_num + 1, week_num
        else:
            new_day, new_week = 1, week_num + 1

        save_program_to_cloud(user, prog, new_week, new_day)
        
        st.success(f"Session Saved! Next up: Week {new_week} Day {new_day}")
        st.balloons()
        time.sleep(1)
        st.rerun()