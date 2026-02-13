import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# ================= LOAD MODEL =================


model = joblib.load("calories_model.pkl")


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Calories Burn Dashboard",
    page_icon="🔥",
    layout="wide"
)

# ================= DARK + GLASS UI =================
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0f2027, #000000);
        color: white;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR =================
st.sidebar.title("User Inputs")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
gender = 0 if gender == "Male" else 1


# ================= SLIDER + INPUT SYNC =================
def synced_input(label, min_val, max_val, default, key):

    # Initialize once
    if key not in st.session_state:
        st.session_state[key] = default
        st.session_state[f"{key}_slider"] = default
        st.session_state[f"{key}_input"] = default

    def slider_changed():
        st.session_state[key] = st.session_state[f"{key}_slider"]
        st.session_state[f"{key}_input"] = st.session_state[key]

    def input_changed():
        st.session_state[key] = st.session_state[f"{key}_input"]
        st.session_state[f"{key}_slider"] = st.session_state[key]

    col1, col2 = st.sidebar.columns([3, 2])

    with col1:
        st.slider(
            label,
            min_val,
            max_val,
            st.session_state[key],
            key=f"{key}_slider",
            on_change=slider_changed
        )

    with col2:
        st.number_input(
            "",
            min_val,
            max_val,
            st.session_state[key],
            key=f"{key}_input",
            on_change=input_changed
        )

    return st.session_state[key]




# ================= INPUTS =================
age = synced_input("Age", 10, 80, 25, "age")
height = synced_input("Height (cm)", 120, 220, 170, "height")
weight = synced_input("Weight (kg)", 30, 150, 70, "weight")
duration = synced_input("Exercise Duration (min)", 1, 180, 30, "duration")
heart_rate = synced_input("Heart Rate", 60, 200, 120, "heart_rate")

body_temp = st.sidebar.number_input("Body Temperature (°C)", 35.0, 42.0, 37.0)
calorie_goal = st.sidebar.number_input("Daily Calorie Goal", 100, 2000, 500)
# ================= INTENSITY CALC =================
max_hr = 220 - age
intensity_pct = (heart_rate / max_hr) * 100 if max_hr > 0 else 0

# ================= CALCULATIONS =================
bmi = weight / ((height / 100) ** 2)


# ================= MAIN =================
st.title("Calories Burn Prediction Dashboard")

if st.sidebar.button("Predict Calories 🔥"):

    input_data = np.array([[gender, age, height, weight,
                            duration, heart_rate, body_temp, bmi]])

    calories = model.predict(input_data)[0]
    calorie_burn_rate = calories / duration if duration > 0 else 0

    # ================= METRICS =================
    m1, m2, m3 = st.columns(3)
    m1.metric("🔥 Calories Burned", f"{calories:.1f} kcal")
    m2.metric("❤️ Avg Heart Rate", f"{heart_rate} bpm")
    m3.metric("📊 BMI", f"{bmi:.2f}")

    # ================= CALORIE GOAL RING =================
    st.divider()
    st.markdown("### Calorie Goal Progress")
    
    progress = min(calories / calorie_goal, 1) if calorie_goal > 0 else 0



    
    # ---- CENTERED, SMALL CONTAINER ----
    col_left, col_center, col_right = st.columns([2, 1.5, 2])
    
    with col_center:
        fig, ax = plt.subplots(figsize=(1.9, 1.9))  # 👈 SMALL & SAFE
    
        # Transparent background
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
    
        progress_color = "#ff6a6a"
        remainder_color = "#1f2933"
    
        ax.pie(
            [progress, 1 - progress],
            startangle=90,
            colors=[progress_color, remainder_color],
            wedgeprops=dict(width=0.25, edgecolor="none")
        )
    
        ax.text(
            0, 0,
            f"{int(progress * 100)}%",
            ha="center",
            va="center",
            fontsize=18,
            weight="bold",
            color="white"
        )
    
        ax.axis("equal")
        ax.axis("off")
    
        # 🚨 VERY IMPORTANT
        st.pyplot(fig, use_container_width=False, transparent=True)
    
    # ---- INFO BELOW ----
    st.markdown(
        f"""
        <div style="
            text-align:center;
            margin-top:10px;
            color:#d1d5db;
            font-size:14px;
        ">
            🔥 <b>{calories:.1f} kcal</b> burned &nbsp;•&nbsp;
            🎯 Goal <b>{calorie_goal} kcal</b> &nbsp;•&nbsp;
            ⏳ <b>{max(calorie_goal - calories, 0):.1f} kcal</b> left
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ================= ACTIVITY CONTRIBUTION (CARDS) =================
    st.divider()
    st.markdown("### Activity Contribution")
        
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(
            f"""
            ### Duration
            <div style="font-size:26px; font-weight:bold;">
                {duration} min
            </div>
     
            """,
            unsafe_allow_html=True
        )
    
    with c2:
        st.markdown(
            f"""
            ### Heart Rate
            <div style="font-size:26px; font-weight:bold;">
                {heart_rate} bpm
            </div>
        
            """,
            unsafe_allow_html=True
        )
    
    with c3:
        st.markdown(
            f"""
            ### Body Temp
            <div style="font-size:26px; font-weight:bold;">
                {body_temp:.1f} °C
          
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align:center; font-size:14px; color:#d1d5db;">
            These factors collectively influence calorie burn, but are measured
            in different units and are best interpreted individually.
        </div>
        """,
        unsafe_allow_html=True
    )


# ================= CALORIE BURN RATE =================
    st.divider()
    st.markdown("### Calories Burn Rate")
    
    col_rate, col_desc = st.columns([1, 2])
    
    with col_rate:
        st.metric(
            label="Burn Rate",
            value=f"{calorie_burn_rate:.2f} kcal/min"
        )
    
    with col_desc:
        st.markdown(
            f"""
            <div style="color:#d1d5db; font-size:14px;">
                This represents how <b>intense</b> your workout was.<br>
                At your current pace, you burn approximately
                <b>{calorie_burn_rate:.2f} calories per minute</b>.
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
# ================= BMI HEALTH INSIGHT =================
    st.divider()
    st.markdown("### BMI Health Insight")
    
   
    # ================= BMI CATEGORY (FIXED) =================
    bmi_raw = weight / ((height / 100) ** 2)   # keep raw
    bmi = round(bmi_raw, 2)                    # only for display
    
    if bmi_raw < 18.5:
        bmi_status = "Underweight"
        bmi_color = "#3b82f6"
        bmi_msg = "You may need to focus on healthy weight gain and nutrition."
    elif bmi_raw < 25:
        bmi_status = "Normal"
        bmi_color = "#22c55e"
        bmi_msg = "You are in a healthy weight range. Keep it up!"
    elif bmi_raw < 30:
        bmi_status = "Overweight"
        bmi_color = "#facc15"
        bmi_msg = "Consider regular exercise and balanced nutrition."
    else:
        bmi_status = "Obese"
        bmi_color = "#ef4444"
        bmi_msg = "It’s recommended to consult a healthcare professional."

    
    col_bmi, col_bmi_info = st.columns([1, 2])
    
    with col_bmi:
        st.markdown(
            f"""
            <div style="
                font-size:24px;
                font-weight:bold;
                color:{bmi_color};
            ">
                {bmi_status}
            </div>
            <div style="color:#d1d5db; margin-top:6px;">
                BMI Value: <b>{bmi:.2f}</b>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_bmi_info:
        st.markdown(
            f"""
            <div style="color:#d1d5db; font-size:14px;">
                Body Mass Index (BMI) is a general indicator of body composition.<br><br>
                <b>Health Insight:</b> {bmi_msg}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================= WORKOUT INTENSITY ZONE =================
    st.divider()
    st.markdown("### Workout Intensity Zone")
    
    
    col_zone, col_info = st.columns([1, 2])
    
    # ---- Determine zone ----
    if intensity_pct < 70:
        zone = "Fat Burn Zone"
        color = "#22c55e"
        message = "Light to moderate intensity. Great for endurance and fat loss."
    elif intensity_pct < 85:
        zone = "Cardio Zone"
        color = "#facc15"
        message = "Moderate to high intensity. Ideal for cardiovascular fitness."
    else:
        zone = "Peak Zone"
        color = "#ef4444"
        message = "Very high intensity. Suitable for short bursts only."
    
    with col_zone:
        st.markdown(
            f"""
            <div style="
                font-size:22px;
                font-weight:bold;
                color:{color};
            ">
                {zone}
            </div>
            <div style="color:#d1d5db; margin-top:6px;">
                {intensity_pct:.1f}% of max HR
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_info:
        st.markdown(
            f"""
            <div style="color:#d1d5db; font-size:14px;">
                Based on your heart rate (<b>{heart_rate} bpm</b>) and estimated
                maximum heart rate (<b>{max_hr} bpm</b>).<br><br>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================= SESSION SUMMARY DATA =================
    session_summary = {
        "Age": age,
        "Gender": "Male" if gender == 0 else "Female",
        "Height (cm)": height,
        "Weight (kg)": weight,
        "Duration (min)": duration,
        "Heart Rate (bpm)": heart_rate,
        "Body Temperature (°C)": body_temp,
        "Calories Burned (kcal)": round(calories, 1),
        "Calories Burn Rate (kcal/min)": round(calorie_burn_rate, 2),
        "Workout Intensity Zone": zone,
        "Intensity (% of Max HR)": round(intensity_pct, 1),
        "BMI": round(bmi, 2),
        "BMI Category": bmi_status,
        "Daily Calorie Goal (kcal)": calorie_goal,
        "Goal Completion (%)": int(progress * 100)
    }
    
    session_df = pd.DataFrame([session_summary])
# ================= SESSION REPORT (CARD FORMAT) =================
    st.divider()
    st.markdown("### Session Report Card")
    
    
    # ---- ROW 1 ----
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            #### 👤 User Details
            - **Age:** {age}  
            - **Gender:** {"Male" if gender == 0 else "Female"}  
            - **Height:** {height} cm  
            - **Weight:** {weight} kg
            """
        )
    
    with col2:
        st.markdown(
            f"""
            #### 🫀 Health Metrics
            - **BMI:** {bmi:.2f} ({bmi_status})  
            - **Heart Rate:** {heart_rate} bpm  
            - **Body Temp:** {body_temp} °C  
            """
        )
    
    st.markdown("---")
    
    # ---- ROW 2 ----
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(
            f"""
            #### 🏃 Workout Summary
            - **Duration:** {duration} min  
            - **Calories Burned:** {calories:.1f} kcal  
            - **Burn Rate:** {calorie_burn_rate:.2f} kcal/min  
            """
        )
    
    with col4:
        st.markdown(
            f"""
            #### 🔥 Performance Insight
            - **Intensity Zone:** {zone}  
            - **Intensity Level:** {intensity_pct:.1f}% of max HR  
            - **Daily Goal:** {calorie_goal} kcal  
            - **Goal Completion:** {int(progress * 100)}%
            """
        )
    
  
    
    # ---- FOOTER NOTE ----
    st.markdown(
        """
        <div style="font-size:13px; color:#d1d5db; text-align:center;">
            This report summarizes your workout session based on the provided inputs
            and machine learning predictions. Values are indicative and for
            informational purposes only.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
# ================= PERSONALIZED TIPS & RECOVERY =================
    st.divider()
    st.markdown("### 💡 Personalized Tips & Recovery")
       
    tips = []
    
    # ---- Tips based on BMI ----
    if bmi_raw < 18.5:
        tips.append("Focus on nutrient-rich foods and gradual strength training to support healthy weight gain.")
    elif bmi_raw < 25:
        tips.append("Maintain your healthy lifestyle with a balance of cardio and strength workouts.")
    elif bmi_raw < 30:
        tips.append("Regular moderate-intensity workouts and mindful eating can help manage weight effectively.")
    else:
        tips.append("Consider low-impact exercises and consult a healthcare professional for a personalized plan.")
    
    # ---- Tips based on Intensity ----
    if intensity_pct >= 85:
        tips.append("High-intensity session detected. Limit such workouts to short durations to avoid overtraining.")
    elif intensity_pct >= 70:
        tips.append("Great cardio intensity! Ensure adequate hydration and recovery.")
    else:
        tips.append("Light-to-moderate intensity workout. Ideal for endurance and recovery days.")
    
    # ---- Tips based on Burn Rate ----
    if calorie_burn_rate >= 10:
        tips.append("High calorie burn rate. Ensure sufficient calorie intake to support recovery.")
    elif calorie_burn_rate >= 6:
        tips.append("Moderate calorie burn rate. Consistency will lead to long-term benefits.")
    else:
        tips.append("Low calorie burn rate. Consider increasing duration or intensity gradually.")
    
    # ---- Display tips ----
    st.markdown("#### Fitness Insights")
    for tip in tips:
        st.markdown(f"- {tip}")
    
    # ---- Rest & Recovery Message ----
    st.markdown("---")
    st.markdown(
        """
        <div style="
            font-size:15px;
            text-align:left;
            color:#d1d5db;
        ">
            <b>Recovery Reminder:</b><br>
            Allow your body time to rest after this workout.
            Proper sleep, hydration, and stretching are essential
            for muscle recovery and injury prevention.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ================= DOWNLOAD BUTTON =================
    st.markdown(
    """
    <hr style="
        border: none;
        border-top: 1px solid rgba(255,255,255,0.15);
        margin: 25px 0;
    ">
    """,
    unsafe_allow_html=True
    )

    
    st.download_button(
        label="⬇️ Download Session Report (CSV)",
        data=session_df.to_csv(index=False),
        file_name="calorie_burn_session_report.csv",
        mime="text/csv"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)


else:
    st.info("⬅ Adjust inputs and click **Predict Calories**")

