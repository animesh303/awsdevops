"""
Structured logging configuration for IAM User Monitor.

This module sets up JSON-formatted logging with consistent field names
for automated log analysis.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict


class StructuredFormatter(logging.Formatter):
    """
    Custom log formatter that outputs structured JSON logs with consistent field names.
    
    Ensures all log entries have a predictable structure for automated analysis.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as a JSON string with consistent fields.
        
        Args:
            record: The log record to format
            
        Returns:
            JSON-formatted log string
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add any extra fields from the log record
        # These are fields added via extra={} in logging calls
        if hasattr(record, "user_name"):
            log_data["user_name"] = record.user_name
        if hasattr(record, "error_code"):
            log_data["error_code"] = record.error_code
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "error_type"):
            log_data["error_type"] = record.error_type
        if hasattr(record, "scan_timestamp"):
            log_data["scan_timestamp"] = record.scan_timestamp
        if hasattr(record, "total_users"):
            log_data["total_users"] = record.total_users
        if hasattr(record, "records_written"):
            log_data["records_written"] = record.records_written
        if hasattr(record, "errors"):
            log_data["errors"] = record.errors
        if hasattr(record, "duration_seconds"):
            log_data["duration_seconds"] = record.duration_seconds
        
        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """
    Configure and return a logger with structured JSON formatting.
    
    Reads LOG_LEVEL from environment variable (defaults to INFO).
    Sets up a handler with StructuredFormatter for consistent JSON output.
    
    Returns:
        Configured logger instance
    """
    # Get log level from environment variable, default to INFO
    log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    
    # Map string to logging level
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    
    log_level = log_level_map.get(log_level_str, logging.INFO)
    
    # Create logger
    logger = logging.getLogger("iam-user-monitor")
    logger.setLevel(log_level)
    
    # Remove any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create console handler with structured formatter
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(StructuredFormatter())
    
    logger.addHandler(handler)
    
    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False
    
    return logger
