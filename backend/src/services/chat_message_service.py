from sqlmodel import Session, select
from typing import List, Optional
from ..models.chat_message import ChatMessage, ChatMessageCreate, ChatMessageUpdate
import uuid


def create_chat_message(*, session: Session, chat_message_create: ChatMessageCreate) -> ChatMessage:
    """
    Create a new chat message
    """
    db_chat_message = ChatMessage.model_validate(chat_message_create)
    session.add(db_chat_message)
    session.commit()
    session.refresh(db_chat_message)
    return db_chat_message


def get_chat_message_by_id(*, session: Session, chat_message_id: uuid.UUID) -> Optional[ChatMessage]:
    """
    Get a chat message by its ID
    """
    return session.get(ChatMessage, chat_message_id)


def get_chat_messages_by_session(*, session: Session, chat_session_id: uuid.UUID) -> List[ChatMessage]:
    """
    Get all chat messages for a specific session
    """
    statement = select(ChatMessage).where(ChatMessage.chat_session_id == chat_session_id)
    return session.exec(statement).all()


def update_chat_message(*, session: Session, chat_message: ChatMessage, chat_message_update: ChatMessageUpdate) -> ChatMessage:
    """
    Update a chat message
    """
    data = chat_message_update.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(chat_message, field, value)
    
    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)
    return chat_message


def delete_chat_message(*, session: Session, chat_message_id: uuid.UUID) -> bool:
    """
    Delete a chat message
    """
    chat_message = session.get(ChatMessage, chat_message_id)
    if not chat_message:
        return False
    
    session.delete(chat_message)
    session.commit()
    return True