from sqlmodel import Session, select
from typing import Optional
from ..models.ai_config import AIConfig, AIConfigCreate, AIConfigUpdate
import uuid


def get_default_ai_config(*, session: Session) -> Optional[AIConfig]:
    """
    Get the default AI configuration
    """
    # For now, just return the first config or create a default one
    statement = select(AIConfig)
    ai_config = session.exec(statement).first()
    if not ai_config:
        # Create a default configuration
        default_config = AIConfigCreate()
        ai_config = AIConfig.model_validate(default_config)
        session.add(ai_config)
        session.commit()
        session.refresh(ai_config)
    return ai_config


def create_ai_config(*, session: Session, ai_config_create: AIConfigCreate) -> AIConfig:
    """
    Create a new AI configuration
    """
    db_ai_config = AIConfig.model_validate(ai_config_create)
    session.add(db_ai_config)
    session.commit()
    session.refresh(db_ai_config)
    return db_ai_config


def get_ai_config_by_id(*, session: Session, ai_config_id: uuid.UUID) -> Optional[AIConfig]:
    """
    Get an AI configuration by its ID
    """
    return session.get(AIConfig, ai_config_id)


def update_ai_config(*, session: Session, ai_config: AIConfig, ai_config_update: AIConfigUpdate) -> AIConfig:
    """
    Update an AI configuration
    """
    data = ai_config_update.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(ai_config, field, value)
    
    session.add(ai_config)
    session.commit()
    session.refresh(ai_config)
    return ai_config


def delete_ai_config(*, session: Session, ai_config_id: uuid.UUID) -> bool:
    """
    Delete an AI configuration
    """
    ai_config = session.get(AIConfig, ai_config_id)
    if not ai_config:
        return False
    
    session.delete(ai_config)
    session.commit()
    return True