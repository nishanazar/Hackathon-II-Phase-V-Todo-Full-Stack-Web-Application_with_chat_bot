"""
Migration script to add Conversation and Message tables to the database,
and extend the tasks table with advanced features.

This script adds the new tables required for the Phase III Todo AI Chatbot
and extends the existing tasks table with advanced features without modifying existing data.
"""

import os
from sqlalchemy import create_engine, text
from settings import settings

def migrate_database():
    """Apply the database migration to add Conversation and Message tables and extend tasks table."""
    # Create database engine
    engine = create_engine(settings.database_url)

    # SQL statements to create the new tables
    create_conversations_table = """
    CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """

    create_messages_table = """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        conversation_id INTEGER NOT NULL,
        role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
        content TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id)
    );
    """

    # SQL statements to extend the tasks table with advanced features
    alter_tasks_add_columns = """
    ALTER TABLE task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;
    ALTER TABLE task ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium';
    ALTER TABLE task ADD COLUMN IF NOT EXISTS tags JSON DEFAULT '[]';
    ALTER TABLE task ADD COLUMN IF NOT EXISTS recurring_interval VARCHAR(20);
    """

    create_indexes = """
    CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
    CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
    CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON task(user_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_completed ON task(completed);
    CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON task(due_date);
    CREATE INDEX IF NOT EXISTS idx_tasks_priority ON task(priority);
    """

    # Execute the migration
    with engine.connect() as conn:
        # Execute each statement
        conn.execute(text(alter_tasks_add_columns))  # Extend tasks table first
        conn.execute(text(create_conversations_table))
        conn.execute(text(create_messages_table))
        conn.execute(text(create_indexes))

        # Commit the transaction
        conn.commit()

    print("Database migration completed successfully!")
    print("- Extended tasks table with advanced features (due_date, priority, tags, recurring_interval)")
    print("- Created conversations table")
    print("- Created messages table")
    print("- Created indexes for performance")
    print("- Maintained all existing data and tables")


if __name__ == "__main__":
    migrate_database()