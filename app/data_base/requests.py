from app.data_base.models import *
from sqlalchemy import select, update, delete


async def get_categories():
    async with async_session() as session:
        categories = await session.scalars(select(Category))
        return categories
