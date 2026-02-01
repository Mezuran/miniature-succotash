import asyncio
import streamlit as st

from miniature.prisma import Prisma

@st.cache_resource
def get_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop

@st.cache_resource
def get_db_client():
    db = Prisma()
    return db

async def connect():
    db = get_db_client()
    if not db.is_connected():
        await db.connect()
    return db