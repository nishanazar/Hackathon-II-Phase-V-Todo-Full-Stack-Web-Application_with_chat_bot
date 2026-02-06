"""
Migration script to enhance the Task table with new fields and add indexes for performance.

This script adds the new columns required for the advanced features of the Phase V Todo AI Chatbot
and creates indexes for improved performance.
"""

import os
from sqlalchemy import create_engine, text
from settings import settings

def migrate_database():
    """Apply the database migration to enhance Task table and add indexes."""
    # Create database engine
    engine = create_engine(settings.database_url)

    # SQL statements to add new columns to the existing Task table
    alter_tasks_table = """
    ALTER TABLE IF EXISTS task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;
    ALTER TABLE IF EXISTS task ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 3;
    ALTER TABLE IF EXISTS task ADD COLUMN IF NOT EXISTS tags TEXT;
    ALTER TABLE IF EXISTS task ADD COLUMN IF NOT EXISTS recurring_interval VARCHAR(20);
    """

    # Create indexes for performance
    create_indexes = """
    CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date);
    CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
    CREATE INDEX IF NOT EXISTS idx_task_recurring_interval ON task(recurring_interval);
    CREATE INDEX IF NOT EXISTS idx_task_user_completed ON task(user_id, completed);
    """

    # Execute the migration
    with engine.connect() as conn:
        # Execute each statement
        conn.execute(text(alter_tasks_table))
        conn.execute(text(create_indexes))

        # Commit the transaction
        conn.commit()

    print("Database migration completed successfully!")
    print("- Added due_date column to task table")
    print("- Added priority column to task table")
    print("- Added tags column to task table")
    print("- Added recurring_interval column to task table")
    print("- Created indexes for performance")
    print("- Maintained all existing data and tables")


if __name__ == "__main__":
    migrate_database()