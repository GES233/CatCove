from sqlalchemy import select, update

from model.tables import Base


async def simple_select(request, model: Base, pk: int):
    session = request.ctx.session
    async with session.begin():
        sql = select(model).where(model.id==pk)
        result = await session.execute(sql)
        data = result.scalars().first()
        session.expunge(data) if data else None
    
    # after session commit.
    return data


async def insert_data(request, data: Base):
    session = request.ctx.session
    async with session.begin():
        session.add(data)
        await session.flush()
        session.expunge(data)
        return data


async def update_record(request, model: Base, pk: int, **kwargs):
    session = request.ctx.session
    async with session.begin():
        # terget = await session.execute(select(model).where(id=pk))
        try:
            sql = update(model).where(model.id == pk).values(**kwargs)
            await session.execute(sql)
        except Exception as e:
            ...
