from sqlalchemy.ext.asyncio import create_async_engine


def create_engine(url: str, is_echo: bool = True):
    return create_async_engine(url, echo=is_echo)
