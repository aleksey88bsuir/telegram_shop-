from app.data_base.models import *
from sqlalchemy import select, update, delete


async def get_categories() -> list[Category]:
    async with async_session() as session:
        categories = await session.scalars(select(Category).filter(
            Category.is_active))
        return categories


async def get_items_by_category(category_id: int) -> list[Item]:
    async with async_session() as session:
        items = await session.scalars(
            select(Item).where(Item.category == category_id,
                               Item.is_active))
        return items


async def get_item_by_id(item_id: int) -> Item:
    async with async_session() as session:
        item = await session.scalar(
            select(Item).where(Item.id == item_id))
        return item
