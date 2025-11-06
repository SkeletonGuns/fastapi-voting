from sqlalchemy import select, String, TEXT, cast, or_

from sqlalchemy.ext.asyncio import AsyncSession


class Base:
    def __init__(self, model, session: AsyncSession):
        self.session = session
        self.model = model


    async def add_instance(self, data: dict):
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()

        return instance


    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_by_id(self, id: int):
        instance = await self.session.get(self.model, id)
        return instance


    async def delete_by_instance(self, instance):
        await self.session.delete(instance)
        return True


    async def get_by_item(self, column, item: any):
        query = select(self.model).where(column == item)
        result = await self.session.execute(query)
        return result.scalars().first()


    async def paginate(self, query):
        # TODO: Реализовать алгоритм пагинации
        pass

    async def search_all(self, model, query, find):
        """Выборка значений по заданному условию поиска"""

        # --- Вспомогательные значение ---
        search_pattern = f"%{find}%"
        search_condition = list()

        # --- Процесс формирование запроса ---
        for column in model.__table__.columns:
            if isinstance(column.type, (TEXT, String)):
                search_condition.append(column.ilike(search_pattern))
            else:
                search_condition.append(cast(column, String).ilike(search_pattern))

        # --- Возврат продекорированного запроса ---
        query = query.filter(or_(*search_condition))
        return query