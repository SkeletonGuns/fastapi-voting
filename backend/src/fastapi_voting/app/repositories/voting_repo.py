from sqlalchemy import select, and_, or_, String, TEXT, cast
from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_voting.app.models.voting import Voting
from src.fastapi_voting.app.models.user import User

from src.fastapi_voting.app.repositories.base_repo import Base


class VotingRepo(Base):

    def __init__(self, session: AsyncSession):
        super().__init__(Voting, session)


    async def delete(self, voting: Voting) -> None:
        voting.deleted = True
        self.session.add(voting)
        await self.session.commit()


    async def available_votings(self, user_id: int, find: str | None):
        """Возвращает перечень доступных конкретному пользователю голосований"""

        # --- Формирование фильтрующего запроса ---
        query = select(Voting).outerjoin(Voting.registered_users).where(
            and_(
                Voting.deleted == False,
                or_(
                    Voting.creator_id == user_id,
                    User.id == user_id,
                    Voting.public == True
                 )
            )
        ).distinct()

        # --- Выборка по значению для поиска ---
        if find is not None:
            search_pattern = f"%{find}%"
            search_condition = list()

            for column in Voting.__table__.columns:
                if isinstance(column.type, (TEXT, String)):
                    search_condition.append(column.ilike(search_pattern))
                else:
                    search_condition.append(cast(column, String).ilike(search_pattern))

            query = query.filter(or_(*search_condition))

        # --- Ответ ---
        result = await self.session.execute(query)
        return result.scalars().all()
