from sqlalchemy.future import select

from model.tables import Base


async def simple_select(request, model: Base, pk: int):
    session = request.ctx.session
    async with session.begin():
        sql = select(model).where(model.id==pk)
        result = await session.execute(sql)
        data = result.scalars()
        session.expunge(data) if data else None
    
    # after session commit.
    return data

