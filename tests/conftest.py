import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fast_hero.app import app
from fast_hero.database import get_session
from fast_hero.models import Base, User
from fast_hero.security import get_password_hash
from fast_hero.settings import Settings


@pytest.fixture
def session():
    engine = create_engine(Settings().DATABASE_URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)

    with Session() as session:
        yield session
        session.rollback()

    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    password = 'testpassword'
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testpassword'

    return user


@pytest.fixture
def other_user(session):
    password = 'testpassword'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testpassword'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


# Define uma fábrica para o modelo User, herdando de factory.Factory
class UserFactory(factory.Factory):
    # Uma classe interna Meta é usada para configurar a fábrica
    class Meta:
        # Define o modelo o qual a fábrica está construindo instâncias
        model = User

    # A cada chamada da fábrica o valor n é incrementado, então cada instancia gerada tera um id único
    id = factory.Sequence(lambda n: n)
    username = factory.LazyAttribute(lambda obj: f'test{obj.id}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
