"""
Database schema update script to fix the tags column type in PostgreSQL.
This script will drop and recreate the tags column with the correct JSON type.
"""

from sqlalchemy import create_engine, text
from settings import settings

def update_tags_column():
    """Update the tags column to use JSON type instead of text array."""
    # Create database engine
    engine = create_engine(settings.database_url)

    # SQL statements to update the tags column
    update_tags_column_sql = """
    -- Drop the existing tags column if it exists
    ALTER TABLE task DROP COLUMN IF EXISTS tags;
    
    -- Add the tags column with JSON type
    ALTER TABLE task ADD COLUMN tags JSON DEFAULT '[]'::json;
    """

    # Execute the update
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(text(update_tags_column_sql))
            trans.commit()
            print("SUCCESS: Tags column updated successfully to JSON type!")
        except Exception as e:
            print(f"ERROR: Error updating tags column: {e}")
            trans.rollback()

if __name__ == "__main__":
    update_tags_column()