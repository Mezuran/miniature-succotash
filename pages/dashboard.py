import streamlit as st
import pandas as pd

# Penting dikasih, setiap page
PAGE_CONFIG = {"title": "My Dashboard", "icon": ":material/home:"}

# Page body
st.subheader("SISTEM MATCHMAKING UNTUK GAME KOMPETITIF MENGGUNAKAN ALGORITMA GREEDY")
st.write("Welcome to the dashboard.")

option = st.selectbox(
    "Rank Matchmaking",
    ("🔴Low", "🟡Mid", "🟢High"),
    index=None,
    placeholder="Pilih Rank..",
)

col1, col2, col3 = st.columns([1, 0.2, 1], vertical_alignment="center")

with col1:
    st.number_input('Team 1', width='stretch', min_value=1)

with col3:
    st.number_input("Team 2", width='stretch', min_value=1)

if st.button("Submit Match"):
    st.write("Succesfully Matching Player")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Team 1")
        player_data = {
            "Player": [
                "P001",
                "P002",
                "P003"
            ],
            "Nickname": ["DragonSlayer", "ShadowKill", "GrokAI"],
            "MMR": ["100", "700", "1200"],
            "Rank": ["🔴", "🟡", "🟢"]
        }
        df = pd.DataFrame(player_data)

        # Tampilkan dataframe TANPA index
        st.dataframe(
            df,
            hide_index=True,  # <--- Ini kuncinya
            use_container_width=True
        )

    with col2:
        st.write("Team 2")
        player_data = {
            "Player": [
                "P001",
                "P002",
                "P003"
            ],
            "Nickname": ["DragonSlayer", "ShadowKill", "GrokAI"],
            "MMR": ["100", "700", "1200"],
            "Rank": ["🔴", "🟡", "🟢"]
        }
        df = pd.DataFrame(player_data)

        # Tampilkan dataframe TANPA index
        st.dataframe(
            df,
            hide_index=True,  # <--- Ini kuncinya
            use_container_width=True
        )


if st.button("Reset", type="primary"):
    st.write("You Reset The Matchmaking")

st.write("You selected:", option)

