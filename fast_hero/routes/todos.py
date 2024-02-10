from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_hero.database import get_session
from fast_hero.models import Todo, User
from fast_hero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fast_hero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])
CurrentUser = Annotated[User, Depends(get_current_user)]
DatabaseSession = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=TodoList)
def list_todos(
    session: DatabaseSession,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        # Verifica se o titulo da tarefa contem a string fornecida
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        # Compara o estado da tarefa com o valor fornecido
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: CurrentUser, session: DatabaseSession):
    db_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


"""
A linha for key, value in todo.model_dump(exclude_unset=True).items(): está iterando através de todos os campos definidos na instância ''todo'' do modelo de atualização. A função model_dump é um método que vem do modelo BaseModel do Pydantic e permite exportar o modelo para um dicionário.

O parâmetro exclude_unset=True é importante aqui, pois significa que apenas os campos que foram explicitamente definidos (ou seja, aqueles que foram incluídos na solicitação PATCH) serão incluídos no dicionário resultante. Isso permite que você atualize apenas os campos que foram fornecidos na solicitação, deixando os outros inalterados.

Após obter a chave e o valor de cada campo definido, a linha setattr(db_todo, key, value) é usada para atualizar o objeto 'db_todo' que representa a tarefa no banco de dados. A função setattr é uma função embutida do Python que permite definir o valor de um atributo em um objeto. Neste caso, ele está definindo o atributo com o nome igual à chave (ou seja, o nome do campo) no objeto 'db_todo' com o valor correspondente.

Dessa forma, somente os campos enviados ao schema sejam atualizados no objeto.
"""


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: DatabaseSession, user: CurrentUser, todo: TodoUpdate
):

    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(status_code=404, detail='Task not found')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: DatabaseSession, user: CurrentUser):

    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(status_code=404, detail='Task not found')

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully'}
