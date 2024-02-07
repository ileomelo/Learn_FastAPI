from sqlalchemy import select

from fast_hero.models import User


def teste_create_user(session):
    new_user = User(
        username='Alice', password='alicesecret', email='alice@email.com'
    )
    session.add(new_user)
    session.commit()
    user = session.scalar(select(User).where(User.username == 'Alice'))

    assert user.username == 'Alice'
