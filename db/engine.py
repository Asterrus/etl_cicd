from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)


def create_engine(url: str, is_echo: bool = True) -> AsyncEngine:
    return create_async_engine(
        url,
        echo=is_echo,
    )
