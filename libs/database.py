from typing import Tuple, Union, Optional, List, Unpack

from prisma import Prisma
from prisma.models import Rank as RankModel, Player as PlayerModel
from prisma.types import RankUpdateInput, PlayerUpdateInput

class Rank:
    @staticmethod
    async def get_by_mmr(db: Prisma, rating: int) -> Tuple[bool, Union[Exception, Optional[RankModel]]]:
        try:
            rank = await db.rank.find_first(
                where={'min_rating': {'lte': rating}}, 
                order={'min_rating': 'desc'}
            )
            return True, rank
        except Exception as e:
            return False, e
        
    @staticmethod
    async def get_all(db: Prisma) -> Tuple[bool, Union[Exception, List[RankModel]]]:
        try:
            players = await db.rank.find_many()
            return True, players
        except Exception as e:
            return False, e

    @staticmethod
    async def get_by_name(db: Prisma, value: str) -> Tuple[bool, Union[Exception, Optional[RankModel]]]:
        try:
            rank = await db.rank.find_first(where={'name': value})
            return True, rank
        except Exception as e:
            return False, e
        
    @staticmethod
    async def create(db: Prisma, name: str, min_rating: int) -> Tuple[bool, Union[Exception, RankModel]]:
        try:
            rank = await db.rank.create(data={'name': name, 'min_rating': min_rating})
            return True, rank
        except Exception as e:
            return False, e 

    @staticmethod
    async def delete_by_name(db: Prisma, name: str) -> Tuple[bool, Union[Exception, Optional[RankModel]]]:
        try:
            rank = await db.rank.delete(where={'name': name})
            return True, rank
        except Exception as e:
            return False, e

    @staticmethod
    async def update_by_name(db: Prisma, name: str, **kwargs: Unpack[RankUpdateInput]) -> Tuple[bool, Union[Exception, Optional[RankModel]]]:
        try:
            rank = await db.rank.update(where={'name': name}, data=kwargs)
            return True, rank
        except Exception as e:
            return False, e
        
    @staticmethod
    async def update(db: Prisma, rank_id: int, **kwargs: Unpack[RankUpdateInput]) -> Tuple[bool, Union[Exception, Optional[RankModel]]]:
        try:
            rank = await db.rank.update(where={'id': rank_id}, data=kwargs)
            return True, rank
        except Exception as e:
            return False, e
        

class Player:
    @staticmethod
    async def get_all(db: Prisma) -> Tuple[bool, Union[Exception, List[PlayerModel]]]:
        try:
            players = await db.player.find_many(include={'rank': True}, order={'rating': 'desc'})
            return True, players
        except Exception as e:
            return False, e

        
    @staticmethod
    async def update_by_name(db: Prisma, name: str, **kwargs: Unpack[PlayerUpdateInput]) -> Tuple[bool, Union[Exception, Optional[PlayerModel]]]:
        try:
            player = await db.player.update(where={'name': name}, data=kwargs)
            return True, player
        except Exception as e:
            return False, e
        
    @staticmethod
    async def update(db: Prisma, player_id: int, **kwargs: Unpack[PlayerUpdateInput]) -> Tuple[bool, Union[Exception, Optional[PlayerModel]]]:
        try:
            player = await db.player.update(where={'id': player_id}, data=kwargs)
            return True, player
        except Exception as e:
            return False, e

    @staticmethod
    async def get_by_name(db: Prisma, value: str) -> Tuple[bool, Union[Exception, Optional[PlayerModel]]]:
        try:
            player = await db.player.find_first(where={'name': value})
            return True, player
        except Exception as e:
            return False, e
        
    @staticmethod
    async def delete_by_name(db: Prisma, name: str) -> Tuple[bool, Union[Exception, Optional[PlayerModel]]]:
        try:
            success, player = await Player.get_by_name(db, name)
            if not success or not player:
                raise Exception(f'Could not find the player named {name}')
            
            deleted_player = await db.player.delete(where={'id': player.id})
            return True, deleted_player
        except Exception as e:
            return False, e
    
    @staticmethod
    async def create(db: Prisma, name: str, rating: int) -> Tuple[bool, Union[Exception, PlayerModel]]:
        try:
            success, rank = await Rank.get_by_mmr(db, rating)
            
            if not success or not rank:
                raise ValueError(f'No valid rank found for rating {rating}')
            
            player = await db.player.create(data={
                'name': name, 
                'rating': rating, 
                'rank_id': rank.id
            })
            return True, player
        except Exception as e:
            return False, e