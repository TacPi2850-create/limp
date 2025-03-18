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

# UI Streamlit
st.title("📆 Calendario Pulizie Domenicali")

# Selezione del mese e anno
today = datetime.today()
current_month = today.month
current_year = today.year

selected_year = st.selectbox("📅 Seleziona l'anno", [2025, 2026], index=0)
selected_month = st.selectbox("🗓️ Seleziona il mese", list(range(1, 13)), index=current_month-1)

# Generazione del calendario mensile
month_days = calendar.monthcalendar(selected_year, selected_month)

# Creiamo la tabella calendario migliorata
styled_table = "<style>th, td { text-align: center; padding: 8px; font-size: 16px; }</style>"
styled_table += "<table border='1' style='width:100%; border-collapse: collapse;'>"
styled_table += "<tr><th>Lun</th><th>Mar</th><th>Mer</th><th>Gio</th><th>Ven</th><th>Sab</th><th style='color: red;'>Dom</th></tr>"

for week in month_days:
    styled_table += "<tr>"
    for day in week:
        if day == 0:
            styled_table += "<td></td>"  # Giorno vuoto
        else:
            date = datetime(selected_year, selected_month, day).date()
            task = df[df["Data"] == date]
            if not task.empty:
                text = f"<b style='color: #FF6347'>{task.iloc[0]['Persona']}</b> - {task.iloc[0]['Mansione']}<br>"
                text += f"<b style='color: #4682B4'>{task.iloc[1]['Persona']}</b> - {task.iloc[1]['Mansione']}"
                styled_table += f"<td style='background-color: #F0F8FF; border: 2px solid black;'>{day}<br>{text}</td>"
            else:
                styled_table += f"<td>{day}</td>"
    styled_table += "</tr>"

styled_table += "</table>"

# Mostriamo la tabella con il calendario
st.markdown(styled_table, unsafe_allow_html=True)

st.write("📅 L'app mostra le pulizie per ogni domenica dell'anno. Puoi navigare tra i mesi per vedere le assegnazioni.")

