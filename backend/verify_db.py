"""
Database verification script for the Todo AI Chatbot application.
This script tests the database connection and verifies that tables exist.
"""

from sqlmodel import select
from db import engine, get_session
from models import Task
from sqlalchemy.exc import ProgrammingError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_database():
    """Verify that the database is properly set up."""
    logger.info("Verifying database connection and tables...")
    
    try:
        # Test the connection by trying to create a session
        with get_session() as session:
            logger.info("Database connection successful!")
            
            # Try to query the task table to see if it exists
            try:
                # This will fail if the table doesn't exist
                stmt = select(Task).limit(1)
                result = session.exec(stmt)
                
                # If we get here, the table exists
                logger.info("Task table exists and is accessible!")
                
                # Count existing tasks
                count_stmt = select(Task)
                count_result = session.exec(count_stmt)
                tasks = count_result.all()
                logger.info(f"Found {len(tasks)} existing tasks in the database.")
                
            except ProgrammingError as e:
                if "does not exist" in str(e) or "no such table" in str(e).lower():
                    logger.error(f"Task table does not exist: {str(e)}")
                    logger.info("This means the database tables were not created properly.")
                    logger.info("Run 'python initialize_db.py' to create the tables.")
                    return False
                else:
                    raise e
            
            except Exception as e:
                logger.error(f"Unexpected error querying the task table: {str(e)}")
                return False
                
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
    
    logger.info("Database verification completed successfully!")
    return True

if __name__ == "__main__":
    verify_database()