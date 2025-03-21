import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta

# Funzione per generare il calendario delle pulizie
def generate_schedule():
    sundays = pd.date_range(start="2025-03-23", periods=52, freq='W-SUN').date
    tasks = ["🛁 Bagno", "🍽️ Cucina"]
    persons = ["JL1", "JL2"]

    data = []
    for i, sunday in enumerate(sundays):
        data.append({"Data": sunday, "Persona": persons[i % 2], "Mansione": tasks[0]})
        data.append({"Data": sunday, "Persona": persons[(i + 1) % 2], "Mansione": tasks[1]})

    return pd.DataFrame(data)

# Creiamo il calendario delle pulizie
df = generate_schedule()

# Stile CSS migliorato per layout, sfondo e contrasto
st.markdown("""
    <style>
        body, .stApp { background-color: #D6EAF8; }
        .main { background-color: #D6EAF8; }
        .sidebar .sidebar-content { background-color: #D6EAF8; }
        h1, h2, h3, h4, h5, h6, label { color: #0D47A1 !important; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; background-color: #000000; border: 2px solid #FFFFFF; }
        th, td { text-align: center; padding: 12px; font-size: 18px; border: 2px solid #FFFFFF; color: white; background-color: #222; }
        th { background-color: #1F618D; color: white; }
        .sunday { background-color: #1C1C1C !important; font-weight: bold; border: 2px solid #FFFFFF; }
        .task-person-jl1 { color: #FFD700; font-weight: bold; }
        .task-person-jl2 { color: #00FA9A; font-weight: bold; }
        .stSelectbox label, .stDateInput label { color: #0D47A1 !important; font-weight: bold; }
        .stTitle { color: #0D47A1 !important; }
    </style>
""", unsafe_allow_html=True)

# UI Streamlit con layout a colonne
st.markdown("<h1 style='color: #0D47A1;'>📆 Calendario Pulizie Domenicali</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    selected_year = st.selectbox("📅 Seleziona l'anno", [2025, 2026], index=0)
    selected_month = st.selectbox("🗓️ Seleziona il mese", list(range(1, 13)), index=datetime.today().month - 1)
    selected_date = st.date_input("📅 Seleziona una data per vedere i dettagli delle pulizie", value=datetime.today())
    daily_tasks = df[df["Data"] == selected_date]
    if not daily_tasks.empty:
        st.write("### Dettagli Pulizie per:", selected_date.strftime('%d %B %Y'))
        st.table(daily_tasks)
    else:
        st.write("Un lugar limpio es un lugar feliz! 😊")

# Generazione del calendario mensile
month_days = calendar.monthcalendar(selected_year, selected_month)

# Creazione tabella calendario
calendar_html = "<table>"
calendar_html += "<tr><th>Lun</th><th>Mar</th><th>Mer</th><th>Gio</th><th>Ven</th><th>Sab</th><th style='color: red;'>Dom</th></tr>"

for week in month_days:
    calendar_html += "<tr>"
    for day in week:
        if day == 0:
            calendar_html += "<td></td>"  # Giorno vuoto
        else:
            date = datetime(selected_year, selected_month, day).date()
            task = df[df["Data"] == date]
            cell_content = f"<b>{day}</b><br>"
            
            if not task.empty:
                cell_content += f"<span class='task-person-jl1'>{task.iloc[0]['Persona']}</span> {task.iloc[0]['Mansione']}<br>"
                cell_content += f"<span class='task-person-jl2'>{task.iloc[1]['Persona']}</span> {task.iloc[1]['Mansione']}"
                calendar_html += f"<td class='sunday'>{cell_content}</td>"
            else:
                calendar_html += f"<td>{cell_content}</td>"
    calendar_html += "</tr>"
calendar_html += "</table>"

# Mostriamo la tabella calendario nella seconda colonna
with col2:
    st.markdown(calendar_html, unsafe_allow_html=True)
