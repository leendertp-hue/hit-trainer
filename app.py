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

# --- HELPER FUNCTIONS ---
def save_program_to_cloud(username, program_json, week, day, rep_range, eq_list, days_val, has_prog=1):
    data = {
        "username": username,
        "program_data": program_json,
        "current_week": week,
        "current_day": day,
        "target_reps": rep_range,
        "equipment": eq_list,
        "days_per_week": days_val,
        "has_program": has_prog
    }
    supabase.table("users").upsert(data, on_conflict="username").execute()
    # Upsert handles both first-time save and updates

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
     # 🟢 NEW: Beginner Mode Toggle
    is_beginner = st.checkbox("Beginner Mode", help="Prioritizes stable machines and joint-friendly movements.")
    days = st.select_slider("Workout Days Per Week", options=[2, 3, 4, 5, 6, 7], value=3)

# --- BRANCH 1: PROGRAM GENERATION / BUILDING ---
    # (Inside the "if not has_program:" block)
    if mode == "Auto-Generate Plan":
        eq = st.multiselect("Available Equipment", ["Selectorized", "Plate-Loaded", "Cables", "Dumbbells", "Barbell", "Bodyweight", "Sled Machine", "Smith Machine"])
        if st.button("🚀 Generate My Plan"):
            from engine import HITEngine
            engine = HITEngine(days, eq, target_reps=rep_range, beginner=is_beginner)
            result = engine.generate_program()
            
            if "error" in result:
                st.error(result["details"])
            else:
                new_program = result["program"]
                save_program_to_cloud(user, new_program, 1, 1, rep_range, eq, days, has_prog=1)
                st.rerun()

    elif mode == "Build Manual Plan":
        st.subheader("🛠️ Build Your Routine")
        custom_plan = {}
        all_library_names = [ex['name'] for ex in MASTER_LIBRARY]

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
                            
                            if is_bw and not is_weighted_bw:
                                t_reps, p_type = 0, "density"
                            else:
                                t_reps, p_type = (low + high) // 2, "standard"

                            day_exercises.append({
                                "name": name,
                                "prog_type": p_type,
                                "target_reps": t_reps,
                                "target_weight": 0.0,
                                "e1rm": 0.0,
                                "discovery_reps": 0
                            })
                        structured_weeks["weeks"][wk_key][d_key] = day_exercises
                
                # 🟢 FIXED: Added the missing arguments to match your new helper function
                # We use ['Manual'] so the database knows this wasn't an auto-gen list
                save_program_to_cloud(
                    user, 
                    structured_weeks, 
                    1, 1, 
                    rep_range, 
                    ["Manual"], 
                    days, 
                    has_prog=1
                )
                st.rerun()


# --- BRANCH 2: ACTIVE TRAINING ---
else:
    session_results = []

    if 'current_program' not in st.session_state:
        st.session_state.current_program = user_data['program_data']
    
    prog = st.session_state.current_program
    week_num = user_data['current_week']
    day_num = user_data['current_day']

    # ... (Keep your Program Completion / Reset logic here) ...

    day_key = f"Day {day_num}"
    week_key = f"Week {week_num}"
    exs = prog['weeks'][week_key][day_key]

    # 🟢 NEW ENGINE INIT: This is the part you're replacing
    from engine import HITEngine
    
    user_rep_range = user_data.get('target_reps', '8-12')
    user_equipment = user_data.get('equipment', ["Bodyweight"])
    user_days = user_data.get('days_per_week', 3)
    
    engine = HITEngine(
        days=user_days, 
        equipment=user_equipment, 
        target_reps=user_rep_range,
        beginner=user_data.get('is_beginner', False)
    )

    # 3. THE SMART GPS
    week_num = user_data['current_week']
    day_num = user_data['current_day']

    # 4. Handle Program Completion
    if week_num > 6:
        st.balloons()
        st.title("🏆 Program Complete!")
        st.write("You've finished the 6-week cycle. Ready to reset?")
        if st.button("♻️ Reset & Start New Cycle"):
            save_program_to_cloud(user, prog, 1, 1, has_prog=0)
            st.session_state.clear()
            st.rerun()
        st.stop()


    # --- 7. SIDEBAR --- Placeholder

    with st.sidebar:
        st.subheader("📊 Average Weekly Stimulus")
        
        tracked_muscles = [
            "Pectorals", "Upper Back", "Quads", "Hamstrings/Glutes", 
            "Front Delts", "Side Delts", "Rear Delts", "Triceps", "Biceps"
        ]
        
        # 1. Get ALL exercise names from the entire program
        all_program_names = [
            ex['name'] 
            for w_val in prog['weeks'].values() 
            for d_val in w_val.values() 
            if isinstance(d_val, list) 
            for ex in d_val
        ]

        # 2. Calculate locally
        local_report = {m: 0.0 for m in tracked_muscles}
        for name in all_program_names:
            ex_data = next((x for x in MASTER_LIBRARY if x['name'] == name), None)
            if ex_data:
                for m, val in ex_data.get('impact', {}).items():
                    if m in local_report:
                        local_report[m] += val
                for m, val in ex_data.get('secondary', {}).items():
                    if m in local_report:
                        local_report[m] += val
        
        # 3. DIVIDE BY 6 to get the Weekly Average
        # This brings a "12" back down to a "2"
        weekly_avg_report = {m: round(val / 6, 1) for m, val in local_report.items()}
        
        st.bar_chart(weekly_avg_report)


        st.subheader("📈 Strength Trends")
        
        # 1. Get unique names of all exercises currently in your 6-week block
        ex_names_in_prog = sorted(list(set(all_program_names)))
        selected_graph_ex = st.selectbox("Select Exercise to Track", ex_names_in_prog)

        # 2. Build the data points by scanning each week
        trend_data = []
        for w_idx in range(1, 7):
            wk_key = f"Week {w_idx}"
            found_in_week = False
            
            # Look through every day of that specific week
            for d_key, d_val in prog['weeks'][wk_key].items():
                if isinstance(d_val, list):
                    for ex_entry in d_val:
                        if ex_entry['name'] == selected_graph_ex:
                            # Pull the e1RM (it starts at 0 and grows as you finish sessions)
                            trend_data.append({
                                "Week": f"W{w_idx}", 
                                "e1RM (kg)": ex_entry.get('e1rm', 0)
                            })
                            found_in_week = True
                            break # Found it for this week, move to the next week
                if found_in_week: break

        # 3. Plot it
        if trend_data:
            import pandas as pd
            df_trend = pd.DataFrame(trend_data)
            
            # We set 'Week' as the index so it shows up on the X-axis
            st.line_chart(df_trend.set_index("Week"))
            
            # Helpful hint for Discovery Mode
            if df_trend["e1RM (kg)"].max() == 0:
                st.caption("ℹ️ Complete a session to see your first data point.")
        else:
            st.info("Select an exercise to see your progression.")

    # 8. UI HEADER
    has_baseline = any(ex.get('e1rm', 0) > 0 for ex in exs)
    st.title("🧪 Discovery Mode" if not has_baseline else f"🚀 Training Mode: W{week_num}")
    st.subheader(f"Session: {day_key}")

# --- START OF THE EXERCISE LOOP ---
    for i, ex in enumerate(exs):
        unique_key_suffix = f"w{week_num}_d{day_num}_{i}" # Defined early to prevent NameErrors
        btn_id = f"swp_{unique_key_suffix}_{ex['name'].replace(' ', '_')}"
        is_density = ex.get('prog_type') == "density"
        icon = "⏱️" if is_density else "🏋️"
        
        # 1. Initialize Rest Time
        if is_density:
            default_s = 60 if week_num == 1 else 300
        else:
            t_reps = ex.get('target_reps', 10)
            default_s = 90 + (t_reps * 5)

        with st.expander(f"{icon} {ex['name']}", expanded=False):

# --- A. Swap Button ---
            if week_num == 1:
                if st.button("🔄 Swap Exercise", key=btn_id):
                    # 1. Get current names to avoid duplicates
                    all_week_names = [m['name'] for d_v in prog["weeks"]["Week 1"].values() if isinstance(d_v, list) for m in d_v]
                    
                    # 2. Get the new move from the engine
                    new_move_data = engine.get_single_swap(ex['name'], all_week_names)
                    
                    if new_move_data:
                        # 3. Update the local variable
                        for w in range(1, 7):
                            prog["weeks"][f"Week {w}"][day_key][i] = new_move_data
                        
                        # 4. Save to Cloud
                        # ✅ NEW
                        save_program_to_cloud(
                            user, 
                            prog, 
                            week_num, 
                            day_num, 
                            user_data['target_reps'], 
                            user_data['equipment'], 
                            user_data['days_per_week']
                        )
                        
                        # 5. FORCE REFRESH: Delete the cached program and the input values
                        if 'current_program' in st.session_state:
                            del st.session_state.current_program
                        
                        # Clear the inputs specifically for this slot
                        if f"w_in_{unique_key_suffix}" in st.session_state:
                            del st.session_state[f"w_in_{unique_key_suffix}"]
                        if f"r_in_{unique_key_suffix}" in st.session_state:
                            del st.session_state[f"r_in_{unique_key_suffix}"]

                        st.rerun()

# --- Rest Timer UI (Inside an Expander) ---

            with st.expander(f"⏱️ Rest and Work Timer"):
                
                @st.fragment(run_every=1.0)
                def timer_component(d_s, k):
                    # State initialization for this specific timer
                    if f"active_{k}" not in st.session_state:
                        st.session_state[f"active_{k}"] = False
                        st.session_state[f"endtime_{k}"] = 0

                    c1, c2 = st.columns([2, 1])
                    with c1:
                        # Value persists even when expander closes
                        u_timer = st.number_input("Seconds", value=d_s, key=f"in_{k}")
                    with c2:
                        st.write("") 
                        btn_col1, btn_col2 = st.columns(2)
                        
                        # START
                        if btn_col1.button("▶️", key=f"go_{k}"):
                            st.session_state[f"endtime_{k}"] = time.time() + u_timer
                            st.session_state[f"active_{k}"] = True
                        
                        # STOP
                        if btn_col2.button("🛑", key=f"stop_{k}"):
                            st.session_state[f"active_{k}"] = False
                            st.rerun()

                    t_placeholder = st.empty()
                    if st.session_state[f"active_{k}"]:
                        remaining = int(st.session_state[f"endtime_{k}"] - time.time())
                        if remaining > 0:
                            t_placeholder.subheader(f"⏳ {remaining//60:02d}:{remaining%60:02d}")
                        else:
                            t_placeholder.success("Done!")
                            st.session_state[f"active_{k}"] = False
                    else:
                        t_placeholder.info("Timer Ready")

                # Call the fragment inside the expander
                timer_component(default_s, unique_key_suffix)

            # --- C. New Instructions Block ---
            # --- Instructions Block (Sleek UI) ---
            if is_density:
                if week_num == 1:
                    st.warning("⚠️ **Discovery Mode — Find your Limits**")
                    st.markdown(f"**The Mission:** Perform as many high-quality reps as possible in **1 minute**. This baseline determines your path for the next 5 weeks.")
                else:
                    st.success(f"🔥 **Goal: Week {week_num} Density**")
                    # Using a 'subheader' or bigger text for the main goal
                    st.markdown(f"### Target: **{ex['target_reps']} Reps** in **5 Minutes**")
            else:
                if week_num == 1:
                    st.warning("⚠️ **Discovery Mode — Find your Limits**")
                    col_a, col_b = st.columns(2)
                    col_a.write(f"**Rep Target:** {ex['target_reps']}")
                    col_b.write(f"**Rest:** {default_s//60}m {default_s%60}s")
                    
                    st.write("1. Work up in weight, performing the target reps at each step.")
                    st.info(f"2. Capture the weight where you reach **absolute failure** as close to **{ex['target_reps']} reps** as possible.")
                else:
                    st.success(f"🏋️ **Target — Work Time**")
                    # Highlight the specific weight and rep goal
                    st.markdown(f"### **{ex.get('target_weight', 0)}kg** for **{ex['target_reps']} Reps**")
                    
                    with st.container(border=True): # Adds a subtle box around the tip
                        st.write("💡 *Outperform the target if you can. If time permits, attempt 2–3 sets, but record the results of your **first** set below.*")
                    
                    st.caption(f"⏱️ Recovery: {default_s//60}m {default_s%60}s rest is essential for peak intensity.")


            # --- D. Data Entry ---
            if is_density:
                w_act = 0.0
                r_act = st.number_input(
                    "Total Reps Achieved", 
                    key=f"r_in_{unique_key_suffix}", 
                    step=1, 
                    value=0
                )
            else:
                col_w, col_r = st.columns(2)
                with col_w: 
                    w_act = st.number_input(
                        "Weight (kg)", 
                        key=f"w_in_{unique_key_suffix}", 
                        value=float(ex.get('target_weight', 0))
                    )
                with col_r: 
                    r_act = st.number_input(
                        "Reps", 
                        key=f"r_in_{unique_key_suffix}", 
                        value=int(ex.get('target_reps', 10))
                    )

            # COLLECT DATA
            session_results.append({
                'name': ex['name'],
                'weight': w_act, 
                'reps': r_act, 
                'target_reps': ex['target_reps'],
                'is_density': is_density
            })

  # --- 9. FINISH SESSION ---
    st.divider()

    all_filled = all(
        (res['reps'] > 0 and res['weight'] > 0) if not res.get('is_density') 
        else res['reps'] > 0 
        for res in session_results
    )

    if st.button("✅ Save & Finish Session", 
                 disabled=not all_filled, 
                 use_container_width=True, 
                 key=f"save_btn_w{week_num}_d{day_num}"):
        
        # A. Update Progression Math (Locked to day_key)
        for res in session_results:
            if res.get('is_density'):
                # DENSITY MATH
                # If W1, current reps is baseline. If W2+, we need to find the W1 discovery_reps.
                if week_num == 1:
                    baseline = res['reps']
                else:
                    # Look back at W1 for the same exercise to find the anchor
                    w1_exs = prog['weeks']['Week 1'][day_key]
                    baseline = next((e['discovery_reps'] for e in w1_exs if e['name'] == res['name']), res['reps'])

                multipliers = {1: 1.0, 2: 3.0, 3: 3.2, 4: 3.4, 5: 3.6, 6: 3.4}
                
                # ONLY update this specific day across future weeks
                for w_idx in range(week_num, 7):
                    target_wk = f"Week {w_idx}"
                    for ex_entry in prog['weeks'][target_wk][day_key]:
                        if ex_entry['name'] == res['name']:
                            if week_num == 1: ex_entry['discovery_reps'] = baseline
                            ex_entry['target_reps'] = int(baseline * multipliers.get(w_idx, 3.0))
                            ex_entry['e1rm'] = baseline
            else:
                # BRZYCKI MATH (Weighted)
                e1rm = res['weight'] * (36 / (37 - res['reps']))
                
                # ONLY update this specific day across future weeks
                for w_idx in range(week_num, 7):
                    target_wk = f"Week {w_idx}"
                    for ex_entry in prog['weeks'][target_wk][day_key]:
                        if ex_entry['name'] == res['name']:
                            ex_entry['e1rm'] = e1rm
                            new_w = e1rm * (37 - ex_entry['target_reps']) / 36
                            ex_entry['target_weight'] = round(new_w / 2.5) * 2.5

        # B. Mark Status
        prog['weeks'][week_key][day_key + "_status"] = "completed"

        # C. Next GPS Spot
        actual_days = [k for k in prog['weeks']["Week 1"].keys() if "Day" in k and "_status" not in k]
        if day_num < len(actual_days):
            new_day, new_week = day_num + 1, week_num
        else:
            new_day, new_week = 1, week_num + 1

        # D. Save to Supabase
        # ✅ NEW
        save_program_to_cloud(
            user, 
            prog, 
            new_week, 
            new_day, 
            user_data['target_reps'], 
            user_data['equipment'], 
            user_data['days_per_week']
        )
        
        # E. FORCE REFRESH: Kill session state so it re-pulls fresh data from Cloud
        if 'current_program' in st.session_state:
            del st.session_state.current_program
        
        st.success("Session Saved to Cloud!")
        st.balloons()
        time.sleep(1)
        st.rerun()