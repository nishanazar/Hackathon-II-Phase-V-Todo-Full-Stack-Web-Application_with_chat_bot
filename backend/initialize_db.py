"""
Database initialization script for the Todo AI Chatbot application.
This script ensures all required tables are created properly in your database.
"""

from sqlmodel import SQLModel
from db import engine
from models import Task, Conversation, Message
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize the database with all required tables."""
    logger.info("Starting database initialization...")
    
    try:
        # Import all models to ensure they're registered with SQLModel
        from models import Task, Conversation, Message
        
        # Create all tables
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        
        logger.info("Database tables created successfully!")
        logger.info("Tables created:")
        for table in SQLModel.metadata.tables.values():
            logger.info(f"  - {table.name}")
            
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        raise
    
    logger.info("Database initialization completed successfully!")

if __name__ == "__main__":
    initialize_database()