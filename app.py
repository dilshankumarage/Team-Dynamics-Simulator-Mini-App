import streamlit as st
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Team member profiles ---
team_members = {
    "Anna": "Empathetic UX designer, values collaboration, easily discouraged by tension.",
    "Leo": "Goal-oriented marketer, loves taking initiative, thrives under pressure.",
    "Mira": "Analytical dev, quiet but deeply loyal, prefers clarity and structure."
}

# --- Leadership Scenarios ---
scenarios = {
    "morale_low": "Morale is low after a missed deadline.",
    "burnout": "Team is burnt out after a successful product launch.",
    "dominating_member": "One member is dominating all decisions, others feel unheard."
}

# --- Leadership Actions per Scenario ---
actions = {
    "morale_low": [
        "Give an emotional team pep talk",
        "Push next milestone to give breathing room",
        "Privately check in with Mira first"
    ],
    "burnout": [
        "Organize a team offsite to decompress",
        "Acknowledge team's work and delay next sprint",
        "Have 1-on-1s to address burnout concerns"
    ],
    "dominating_member": [
        "Address it openly in next team meeting",
        "Speak privately with the dominant member",
        "Rotate facilitation responsibilities"
    ]
}

# --- AI Prompt ---
def get_team_reaction(scenario, action):
    prompt = f"""
You are simulating a leadership training scenario.

Team Members:
1. Anna – {team_members['Anna']}
2. Leo – {team_members['Leo']}
3. Mira – {team_members['Mira']}

Scenario:
{scenario}

Leadership Action:
{action}

For each team member, describe their emotional and behavioral response. 
Also provide a 1-line summary of the team's overall morale and alignment.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# --- Streamlit UI ---
st.set_page_config(page_title="Team Dynamics Simulator", layout="centered")
st.title("👥 Team Dynamics Simulator")
st.markdown("Simulate how leadership decisions impact your team's mood and behavior.")

# --- Step 1: Select Scenario ---
scenario_key = st.selectbox("📌 Select a situation:", list(scenarios.keys()), format_func=lambda x: scenarios[x])
scenario_text = scenarios[scenario_key]

# --- Step 2: Show Team ---
st.markdown("### 👥 Meet Your Team")
for name, bio in team_members.items():
    st.markdown(f"**{name}** – {bio}")

# --- Step 3: Choose Action ---
selected_action = st.radio("🎯 Choose a leadership action:", actions[scenario_key])

# --- Step 4: Get AI Result ---
if st.button("🔍 Simulate Team Reactions"):
    with st.spinner("Thinking like a leadership coach..."):
        result = get_team_reaction(scenario_text, selected_action)
        st.markdown("### 🧠 Team Reactions")
        st.markdown(result)
