import streamlit as st
import pandas as pd

from libs import Utils

# Penting dikasih, setiap page
PAGE_CONFIG = {"title": "My Master Page", "icon": ":material/data_table:"}

# Page body
st.header("Master Page")
st.write("Welcome to the Page.")

player_data = {
    "ID": [
        "P001",
        "P002",
        "P003"
    ],
    "Nickname": ["DragonSlayer", "ShadowKill", "GrokAI"],
    "MMR": ["100", "700", "1200"],
    "Rank": ["🔴 Low", "🟡 Mid", "🟢 High"]
}

df = pd.DataFrame(player_data)

# Tampilkan dataframe TANPA index
st.dataframe(
    df,
    hide_index=True,  # <--- Ini kuncinya
    use_container_width=True
)

tab1, tab2, tab3 = st.tabs([":material/add: Tambah", ":material/remove: Hapus", ":material/edit: Edit"])

with tab1:
    nickname = st.text_input("Nickname", placeholder="Cth. DragonSlayer", key=Utils.generate_random_string(5))
    mmr = st.number_input("MMR", min_value=100, key=Utils.generate_random_string(5))

    if st.button("Tambah", key='btn-tambah'):
        st.write("Ciao")
    
with tab2:
    option = st.selectbox(
        "Pilih akun yang ingin di edit.",
        ("DragonSlayer", "ShadowKill", "GrokAI"),
        key=Utils.generate_random_string(5)
    )

    st.markdown('---')
    st.caption('Masukan value dibawah ini.')

    id = st.text_input("ID", placeholder="Cth. P001", key=Utils.generate_random_string(5))
    nickname = st.text_input("Nickname", placeholder="Cth. DragonSlayer", key=Utils.generate_random_string(5))
    mmr = st.number_input("MMR", min_value=100, key=Utils.generate_random_string(5))

    if st.button("Edit", key='btn-edit'):
        st.write("Ciao")

with tab3:
    option = st.selectbox(
        "Pilih akun yang ingin di hapus.",
        ("DragonSlayer", "ShadowKill", "GrokAI"),
        key=Utils.generate_random_string(5)
    )

    if st.button("Hapus", key='btn-hapus'):
        st.write("Ciao")
