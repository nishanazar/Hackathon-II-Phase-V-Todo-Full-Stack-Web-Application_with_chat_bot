from sqlmodel import Session, select
from typing import List, Optional
from ..models.chat_session import ChatSession, ChatSessionCreate, ChatSessionUpdate
import uuid


def create_chat_session(*, session: Session, chat_session_create: ChatSessionCreate) -> ChatSession:
    """
    Create a new chat session
    """
    db_chat_session = ChatSession.model_validate(chat_session_create)
    session.add(db_chat_session)
    session.commit()
    session.refresh(db_chat_session)
    return db_chat_session


def get_chat_session_by_id(*, session: Session, chat_session_id: uuid.UUID) -> Optional[ChatSession]:
    """
    Get a chat session by its ID
    """
    return session.get(ChatSession, chat_session_id)


def get_chat_sessions_by_user(*, session: Session, user_id: str) -> List[ChatSession]:
    """
    Get all chat sessions for a specific user
    """
    statement = select(ChatSession).where(ChatSession.user_id == user_id)
    return session.exec(statement).all()


def update_chat_session(*, session: Session, chat_session: ChatSession, chat_session_update: ChatSessionUpdate) -> ChatSession:
    """
    Update a chat session
    """
    data = chat_session_update.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(chat_session, field, value)
    
    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)
    return chat_session


def delete_chat_session(*, session: Session, chat_session_id: uuid.UUID) -> bool:
    """
    Delete a chat session
    """
    chat_session = session.get(ChatSession, chat_session_id)
    if not chat_session:
        return False
    
    session.delete(chat_session)
    session.commit()
    return True