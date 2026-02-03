from miniature.prisma import Prisma

def get_db_client():
    db = Prisma()
    return db

async def connect():
    db = get_db_client()
    if not db.is_connected():
        await db.connect()
    return db