import pytest
from sqlmodel import Session, SQLModel
from backend.models import Conversation, Message
from backend.db import engine

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_conversation(session: Session):
    """Test creating a new conversation."""
    conversation = Conversation(user_id="test_user_123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    assert conversation.id is not None
    assert conversation.user_id == "test_user_123"
    assert conversation.created_at is not None
    assert conversation.updated_at is not None

def test_create_message(session: Session):
    """Test creating a new conversation with associated messages."""
    # Create a conversation first
    conversation = Conversation(user_id="test_user_123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Create a message associated with the conversation
    message = Message(
        user_id="test_user_123",
        conversation_id=conversation.id,
        role="user",
        content="Hello, this is a test message!"
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    
    assert message.id is not None
    assert message.user_id == "test_user_123"
    assert message.conversation_id == conversation.id
    assert message.role == "user"
    assert message.content == "Hello, this is a test message!"
    assert message.created_at is not None

def test_message_role_validation(session: Session):
    """Test that message roles are properly validated."""
    conversation = Conversation(user_id="test_user_123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Valid roles should work
    user_message = Message(
        user_id="test_user_123",
        conversation_id=conversation.id,
        role="user",
        content="User message"
    )
    assistant_message = Message(
        user_id="test_user_123",
        conversation_id=conversation.id,
        role="assistant",
        content="Assistant response"
    )
    
    session.add(user_message)
    session.add(assistant_message)
    session.commit()
    
    assert user_message.role == "user"
    assert assistant_message.role == "assistant"

def test_conversation_messages_relationship(session: Session):
    """Test the relationship between conversations and messages."""
    # Create a conversation
    conversation = Conversation(user_id="test_user_123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    
    # Add multiple messages to the conversation
    message1 = Message(
        user_id="test_user_123",
        conversation_id=conversation.id,
        role="user",
        content="First message"
    )
    message2 = Message(
        user_id="test_user_123",
        conversation_id=conversation.id,
        role="assistant",
        content="Response to first message"
    )
    
    session.add(message1)
    session.add(message2)
    session.commit()
    
    # Refresh the conversation to get the related messages
    session.refresh(conversation)
    
    # Verify the relationship works
    assert len(conversation.messages) >= 2  # At least the 2 we added
    message_contents = [msg.content for msg in conversation.messages]
    assert "First message" in message_contents
    assert "Response to first message" in message_contents