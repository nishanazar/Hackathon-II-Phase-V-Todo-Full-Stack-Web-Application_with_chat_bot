import logging
from datetime import datetime
import os

# Set up logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)

# Also configure the root logger
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)


def log_info(message: str, extra_data: dict = None):
    """Log an info message"""
    if extra_data:
        message = f"{message} | Extra data: {extra_data}"
    logger.info(message)


def log_error(message: str, extra_data: dict = None, exc_info=False):
    """Log an error message"""
    if extra_data:
        message = f"{message} | Extra data: {extra_data}"
    logger.error(message, exc_info=exc_info)


def log_warning(message: str, extra_data: dict = None):
    """Log a warning message"""
    if extra_data:
        message = f"{message} | Extra data: {extra_data}"
    logger.warning(message)


def log_debug(message: str, extra_data: dict = None):
    """Log a debug message"""
    if extra_data:
        message = f"{message} | Extra data: {extra_data}"
    logger.debug(message)


def log_ai_interaction(user_id: str, user_message: str, ai_response: str, session_id: str = None):
    """Log AI agent interactions"""
    log_info(
        "AI Agent Interaction",
        {
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response
        }
    )