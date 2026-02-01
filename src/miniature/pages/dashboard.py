import asyncio
import random
import streamlit as st
import pandas as pd

from miniature.libs.database import Player
from miniature.libs.connection import connect, get_event_loop
from miniature.prisma.models import Player as PlayerModel

PAGE_CONFIG = {"title": "Auto Matchmaking", "icon": ":material/diversity_3:"}

st.header(":material/all_match: Auto Matchmaking System")
st.caption("Sistem pencarian match otomatis berdasarkan jumlah pemain per tim.")

def greedy_balance_teams(players: list[PlayerModel]) -> tuple[list[PlayerModel], list[PlayerModel]]:
    """
    Algoritma Greedy:
    1. Urutkan player dari MMR tertinggi.
    2. Masukkan player ke tim yang total MMR-nya lebih rendah saat ini.
    """
    sorted_players = sorted(players, key=lambda x: x.rating, reverse=True)
    
    team_1 = []
    team_2 = []
    sum_1 = 0
    sum_2 = 0

    for player in sorted_players:
        if sum_1 <= sum_2:
            team_1.append(player)
            sum_1 += player.rating
        else:
            team_2.append(player)
            sum_2 += player.rating
            
    return team_1, team_2

def display_team_stats(team_name: str, players: list[PlayerModel]):
    """Menampilkan statistik tim dalam bentuk metrics dan dataframe."""
    if not players:
        st.caption(f"*{team_name} tidak memiliki pemain.*")
        return
    
    total_mmr = sum(p.rating for p in players)
    avg_mmr = total_mmr / len(players) if players else 0
    
    st.subheader(f":material/groups: {team_name}")
    st.metric(label=":material/avg_pace: Team Power", value=f"{total_mmr:,} MMR", delta=f"Avg: {avg_mmr:.0f}")

    data = []
    for p in players:
        rank_name = p.rank.name if p.rank else "Unranked"
        data.append({
            "Nickname": p.name,
            "MMR": p.rating,
            "Rank": f"{rank_name}"
        })
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        column_config={
            "Nickname": st.column_config.TextColumn("Player Name"),
            "MMR": st.column_config.NumberColumn("Rating"),
            "Rank": st.column_config.TextColumn("Tier"),
        },
        hide_index=True,
        width='stretch'
    )

async def main():
    db = await connect()

    success, all_players = await Player.get_all(db)
    if not success:
        st.error(f"Gagal mengambil data database: {all_players}")
        return

    with st.container(border=True):
        st.markdown("### :material/settings: Match Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            rank_filter = st.selectbox(
                "Rank Pool Filter",
                ("All Ranks", "Low (< 1000)", "Mid (1000 - 2000)", "High (> 2000)"),
                help="Hanya pilih pemain dari rentang skill tertentu."
            )

        with col2:
            team_size = st.number_input(
                "Jumlah Player per Team", 
                min_value=1, 
                max_value=10, 
                value=5,
                step=1,
                help="Contoh: Jika diisi 5, sistem akan mencari 10 pemain untuk 5 vs 5."
            )

    # 3. Filtering Logic
    pool_players = []
    if "Low" in rank_filter:
        pool_players = [p for p in all_players if p.rating < 1000]
    elif "Mid" in rank_filter:
        pool_players = [p for p in all_players if 1000 <= p.rating <= 2000]
    elif "High" in rank_filter:
        pool_players = [p for p in all_players if p.rating > 2000]
    else:
        pool_players = all_players # All Ranks

    total_needed = team_size * 2
    available_count = len(pool_players)

    st.caption(f"Status Pool: Ditemukan **{available_count}** pemain yang sesuai kriteria filter.")

    if st.button(":material/search: Find Match", type="primary", width='stretch'):
        if available_count == 0:
            st.warning("Tidak ada pemain sama sekali di kategori rank ini.", icon=":material/warning:")
        else:
            with st.spinner("Mengacak pemain dan menyeimbangkan tim..."):
                await asyncio.sleep(0.5)
                
                if available_count <= total_needed:
                    match_participants = pool_players
                    if available_count < total_needed:
                        st.toast(f"Pemain kurang ({available_count}/{total_needed}). Menggunakan seluruh pemain.", icon=":material/info:")
                else:
                    match_participants = random.sample(pool_players, total_needed)

                team_a, team_b = greedy_balance_teams(match_participants)

                st.success("Match Found & Balanced!", icon=":material/check:")
                
                col_res_1, col_res_2 = st.columns(2)
                with col_res_1:
                    display_team_stats("Team Red", team_a)
                with col_res_2:
                    display_team_stats("Team Blue", team_b)

                diff = abs(sum(p.rating for p in team_a) - sum(p.rating for p in team_b))
                st.info(f"Selisih Total MMR kedua tim hanya: **{diff}** poin.", icon=":material/info:")

if __name__ == "__main__":
    loop = get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())