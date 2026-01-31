import asyncio
import streamlit as st
import pandas as pd

from libs.database import Player, Rank
from libs.connection import connect, get_event_loop
from libs.utils import generate_random_string

PAGE_CONFIG = {"title": "My Master Page", "icon": ":material/data_table:"}

st.header("Master Page")

async def main():
    db = await connect()

    tab_1, tab_2 = st.tabs([':material/account_box: Players', ':material/badge: Ranks'])
    with tab_1:
        col_1, col_2, col_3 = st.columns(3)
        
        with col_1:
            with st.popover(':material/add: Create new player', width='stretch'):
                p_name = st.text_input("Name", key="p_name")
                p_rate = st.number_input("Rating", min_value=0, value=1000, step=10, key="p_mmr")
                
                if st.button("Save Player", key='btn-save-player'):
                    with st.spinner("Saving..."):
                        success_p, res = await Player.create(db, p_name, int(p_rate))
                        if success_p:
                            st.success(f"Player {res.name} created! (Player ID: {res.id})", icon=':material/check:')
                        else:
                            st.error(f"Error: {res}", icon=':material/error:')

        with col_2:
            with st.popover(':material/remove: Delete player', width='stretch'):
                result, res = await Player.get_all(db)
                if not result:
                    st.error(f'Error: {res}')
                else:
                    players_selected = st.multiselect(
                        "Which player you want to delete?",
                        [player.name for player in res.copy()],
                        key="multiselect_delete_players"
                    )
                    if st.button("Delete Confirm", key='btn-delete-player'):
                        if not players_selected:
                            st.warning('Please choose selected player.', icon=':material/warning:')
                            return
                        
                        for player_name in players_selected:
                            success_p, player = await Player.delete_by_name(db, player_name)
                            if not result or not player:
                                st.error(f'Error: {player}', icon=':material/warning:')
                                break
                        
                        st.success(f'Successfully removing {list(map(lambda name: name, players_selected))}', icon=':material/check:')

        st.divider()

        success_p, list_p = await Player.get_all(db)

        if not success_p:
            st.error(f'Error {list_p}', icon=':material/error:')
        else:
            if len(list_p) <= 0:
                st.info('There is no player in the database.', icon=':material/info:')
            
            table_data = []
            for p in list_p.copy():
                p_dict = p.model_dump()
                p_dict['rank_name'] = p.rank.name if p.rank else "Unranked"
                table_data.append(p_dict)

            df_players = pd.DataFrame(table_data)

            edited_players = st.data_editor(
                df_players,
                column_config={
                    "rank_id": None,
                    "rank": None,

                    "id": st.column_config.TextColumn("ID", disabled=True),
                    "name": st.column_config.TextColumn("Name (Editable)", required=True),
                    "rating": st.column_config.NumberColumn("MMR (Editable)", min_value=0, step=10, required=True),
                    "rank_name": st.column_config.TextColumn("Rank", disabled=True)
                },
                hide_index=True,
                width='stretch',
                key="editor_players"
            )

            editor_state = st.session_state.get("editor_players", {})
            edited_rows = editor_state.get("edited_rows", {})

            if edited_rows:
                with col_3:
                    if st.button("Save Player Changes", icon=':material/edit:', width='stretch'):
                        with st.spinner("Updating database..."):
                            for _, row in edited_players.iterrows():
                                success, rank = await Rank.get_by_mmr(db, int(row['rating']))
                                
                                if not success or not rank:
                                    st.error(f"Error calculating rank for {row['name']}: {rank}", icon=':material/error:')
                                    continue
                                
                                update_success, update_result = await Player.update(
                                    db, 
                                    int(row['id']),
                                    id=int(row['id']),
                                    name=row['name'],
                                    rating=int(row['rating']),
                                    rank_id=rank.id
                                )

                                if not update_success:
                                    st.error(f"Failed to update {row['name']}: {update_result}", icon=':material/error:')
                            
                            st.success("All changes saved!", icon=':material/check:')
                            st.rerun()

    with tab_2:
        col_1, col_2, col_3 = st.columns(3)
        
        with col_1:
            with st.popover(':material/add: Create new rank', width='stretch'):
                r_name = st.text_input("Name", key="new_r_name")
                r_min_rate = st.number_input("Minimum rating", min_value=0, value=1000, step=10, key="new_r_min_rate")
                
                if st.button("Save Rank", key='btn-save-rank'):
                    with st.spinner("Saving..."):
                        success_p, res = await Rank.create(db, r_name, int(r_min_rate))
                        if success_p:
                            st.success(f"Rank {res.name} created! (Rank ID: {res.id})", icon=':material/check:')
                        else:
                            st.error(f"Error: {res}", icon=':material/error:')

        with col_2:
            with st.popover(':material/remove: Delete rank', width='stretch'):
                result, res = await Rank.get_all(db)
                if not result:
                    st.error(f'Error: {res}')
                else:
                    ranks_selected = st.multiselect(
                        "Which rank you want to delete?",
                        [rank.name for rank in res.copy()],
                        key="multiselect_delete_ranks"
                    )

                    if st.button("Delete Confirm", key='btn-delete-rank'):
                        if ranks_selected:
                            st.warning('Please choose selected rank.', icon=':material/warning:')
                        else:
                            for player_name in ranks_selected:
                                success_p, player = await Rank.delete_by_name(db, player_name)
                                if not result or not player:
                                    st.error(f'Error: {player}', icon=':material/warning:')
                                    break

                            st.success(f'Successfully removing {list(map(lambda name: name, ranks_selected))}', icon=':material/check:')

        st.divider()

        success_r, list_r = await Rank.get_all(db)

        if not success_r:
            st.error(f'Error {list_r}', icon=':material/error:')
        else:
            if len(list_r) <= 0:
                st.info('There is no player in the database.', icon=':material/info:')
            
            df_ranks = pd.DataFrame([r.model_dump() for r in list_r.copy()])

            edited_ranks = st.data_editor(
                df_ranks,
                column_config={
                    'players': None,

                    "id": st.column_config.TextColumn("ID", disabled=True),
                    "name": st.column_config.TextColumn("Name (Editable)", required=True),
                    "min_rating": st.column_config.NumberColumn("Min MMR (Editable)", min_value=0, step=10, required=True),
                },
                hide_index=True,
                width='stretch',
                key="editor_ranks"
            )

            editor_state = st.session_state.get("editor_ranks", {})
            edited_rows = editor_state.get("edited_rows", {})

            if edited_rows:
                with col_3:
                    if st.button("Save Rank Changes", icon=':material/edit:', width='stretch'):
                        with st.spinner("Updating database..."):
                            for _, row in edited_ranks.iterrows():
                                update_success, update_result = await Rank.update(
                                    db,
                                    row['id'],
                                    name=row['name'],
                                    min_rating=row['min_rating']
                                )

                                if not update_success:
                                    st.error(f"Failed to update {row['name']}: {update_result}", icon=':material/error:')
                            
                            st.success("All changes saved!", icon=':material/check:')
                            st.rerun()

if __name__ == "__main__":
    loop = get_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main())