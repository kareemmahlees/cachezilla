# pylint: disable=import-error,missing-class-docstring,too-few-public-methods

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine


class Post(SQLModel, table=True):  # type: ignore[call-arg]
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str


POSTGRES_URL = "postgresql://cachezilla:cachezilla@localhost:54321"

engine = create_engine(POSTGRES_URL)

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_post():
    post = Post(title="test post", description="test description")

    with Session(engine) as session:
        session.add(post)
        session.commit()


def main():
    create_db_and_tables()
    create_post()


if __name__ == "__main__":
    create_db_and_tables()
    create_post()
