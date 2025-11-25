"""
Property-based tests for structured logging consistency.

Feature: iam-user-monitor, Property 7: Structured logging consistency
Validates: Requirements 5.5
"""

import json
import logging
import os
from io import StringIO
from typing import Any, Dict, List, Optional

from hypothesis import given, settings, strategies as st

from logger_config import StructuredFormatter, setup_logging


# Strategy for generating log levels
log_levels = st.sampled_from([
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
])

# Strategy for generating logger names
logger_names = st.text(min_size=1, max_size=50, alphabet=st.characters(
    whitelist_categories=('Lu', 'Ll', 'Nd'),
    whitelist_characters='-_.'
))

# Strategy for generating log messages
log_messages = st.text(min_size=0, max_size=500)

# Strategy for optional extra fields
optional_user_name = st.one_of(st.none(), st.text(min_size=1, max_size=100))
optional_error_code = st.one_of(st.none(), st.text(min_size=1, max_size=50))
optional_request_id = st.one_of(st.none(), st.text(min_size=1, max_size=100))
optional_error_type = st.one_of(st.none(), st.text(min_size=1, max_size=100))
optional_scan_timestamp = st.one_of(st.none(), st.text(min_size=1, max_size=50))
optional_total_users = st.one_of(st.none(), st.integers(min_value=0, max_value=10000))
optional_records_written = st.one_of(st.none(), st.integers(min_value=0, max_value=10000))
optional_errors = st.one_of(st.none(), st.integers(min_value=0, max_value=1000))
optional_duration_seconds = st.one_of(st.none(), st.floats(min_value=0.0, max_value=300.0, allow_nan=False, allow_infinity=False))


def create_log_record(
    level: int,
    logger_name: str,
    message: str,
    user_name: Optional[str] = None,
    error_code: Optional[str] = None,
    request_id: Optional[str] = None,
    error_type: Optional[str] = None,
    scan_timestamp: Optional[str] = None,
    total_users: Optional[int] = None,
    records_written: Optional[int] = None,
    errors: Optional[int] = None,
    duration_seconds: Optional[float] = None,
    exc_info: Optional[tuple] = None
) -> logging.LogRecord:
    """Create a log record with optional extra fields."""
    record = logging.LogRecord(
        name=logger_name,
        level=level,
        pathname="test.py",
        lineno=1,
        msg=message,
        args=(),
        exc_info=exc_info
    )
    
    # Add optional extra fields
    if user_name is not None:
        record.user_name = user_name
    if error_code is not None:
        record.error_code = error_code
    if request_id is not None:
        record.request_id = request_id
    if error_type is not None:
        record.error_type = error_type
    if scan_timestamp is not None:
        record.scan_timestamp = scan_timestamp
    if total_users is not None:
        record.total_users = total_users
    if records_written is not None:
        record.records_written = records_written
    if errors is not None:
        record.errors = errors
    if duration_seconds is not None:
        record.duration_seconds = duration_seconds
    
    return record


# Feature: iam-user-monitor, Property 7: Structured logging consistency
@settings(max_examples=100)
@given(
    level=log_levels,
    logger_name=logger_names,
    message=log_messages,
    user_name=optional_user_name,
    error_code=optional_error_code,
    request_id=optional_request_id,
    error_type=optional_error_type,
    scan_timestamp=optional_scan_timestamp,
    total_users=optional_total_users,
    records_written=optional_records_written,
    errors=optional_errors,
    duration_seconds=optional_duration_seconds
)
def test_structured_logging_consistency(
    level: int,
    logger_name: str,
    message: str,
    user_name: Optional[str],
    error_code: Optional[str],
    request_id: Optional[str],
    error_type: Optional[str],
    scan_timestamp: Optional[str],
    total_users: Optional[int],
    records_written: Optional[int],
    errors: Optional[int],
    duration_seconds: Optional[float]
):
    """
    Property 7: Structured logging consistency
    
    For any log entry produced by the system, it should use consistent field names
    and structured format suitable for automated log analysis.
    
    Validates: Requirements 5.5
    """
    # Create a log record with the generated values
    record = create_log_record(
        level=level,
        logger_name=logger_name,
        message=message,
        user_name=user_name,
        error_code=error_code,
        request_id=request_id,
        error_type=error_type,
        scan_timestamp=scan_timestamp,
        total_users=total_users,
        records_written=records_written,
        errors=errors,
        duration_seconds=duration_seconds
    )
    
    # Format the log record using StructuredFormatter
    formatter = StructuredFormatter()
    formatted_output = formatter.format(record)
    
    # Parse the output as JSON - this verifies it's valid JSON
    try:
        log_data = json.loads(formatted_output)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Log output is not valid JSON: {formatted_output}") from e
    
    # Verify required fields are always present with consistent names
    required_fields = ["timestamp", "level", "logger", "message"]
    for field in required_fields:
        assert field in log_data, f"Required field '{field}' missing from log output"
    
    # Verify timestamp format (ISO 8601 with Z suffix)
    assert isinstance(log_data["timestamp"], str), "timestamp should be a string"
    assert log_data["timestamp"].endswith("Z"), "timestamp should end with 'Z'"
    assert "T" in log_data["timestamp"], "timestamp should contain 'T' separator"
    
    # Verify level is a string and matches expected value
    assert isinstance(log_data["level"], str), "level should be a string"
    expected_level_name = logging.getLevelName(level)
    assert log_data["level"] == expected_level_name, f"level should be '{expected_level_name}'"
    
    # Verify logger name matches
    assert isinstance(log_data["logger"], str), "logger should be a string"
    assert log_data["logger"] == logger_name, "logger name should match"
    
    # Verify message matches
    assert isinstance(log_data["message"], str), "message should be a string"
    assert log_data["message"] == message, "message should match"
    
    # Verify optional fields are included with consistent names when present
    if user_name is not None:
        assert "user_name" in log_data, "user_name should be present when provided"
        assert log_data["user_name"] == user_name, "user_name should match"
    
    if error_code is not None:
        assert "error_code" in log_data, "error_code should be present when provided"
        assert log_data["error_code"] == error_code, "error_code should match"
    
    if request_id is not None:
        assert "request_id" in log_data, "request_id should be present when provided"
        assert log_data["request_id"] == request_id, "request_id should match"
    
    if error_type is not None:
        assert "error_type" in log_data, "error_type should be present when provided"
        assert log_data["error_type"] == error_type, "error_type should match"
    
    if scan_timestamp is not None:
        assert "scan_timestamp" in log_data, "scan_timestamp should be present when provided"
        assert log_data["scan_timestamp"] == scan_timestamp, "scan_timestamp should match"
    
    if total_users is not None:
        assert "total_users" in log_data, "total_users should be present when provided"
        assert log_data["total_users"] == total_users, "total_users should match"
    
    if records_written is not None:
        assert "records_written" in log_data, "records_written should be present when provided"
        assert log_data["records_written"] == records_written, "records_written should match"
    
    if errors is not None:
        assert "errors" in log_data, "errors should be present when provided"
        assert log_data["errors"] == errors, "errors should match"
    
    if duration_seconds is not None:
        assert "duration_seconds" in log_data, "duration_seconds should be present when provided"
        # Use approximate comparison for floats
        assert abs(log_data["duration_seconds"] - duration_seconds) < 0.0001, "duration_seconds should match"
    
    # Verify no unexpected fields are present (only known fields)
    expected_fields = set(required_fields)
    if user_name is not None:
        expected_fields.add("user_name")
    if error_code is not None:
        expected_fields.add("error_code")
    if request_id is not None:
        expected_fields.add("request_id")
    if error_type is not None:
        expected_fields.add("error_type")
    if scan_timestamp is not None:
        expected_fields.add("scan_timestamp")
    if total_users is not None:
        expected_fields.add("total_users")
    if records_written is not None:
        expected_fields.add("records_written")
    if errors is not None:
        expected_fields.add("errors")
    if duration_seconds is not None:
        expected_fields.add("duration_seconds")
    
    actual_fields = set(log_data.keys())
    unexpected_fields = actual_fields - expected_fields
    assert len(unexpected_fields) == 0, f"Unexpected fields in log output: {unexpected_fields}"


# Feature: iam-user-monitor, Property 7: Structured logging consistency (with exceptions)
@settings(max_examples=100)
@given(
    level=log_levels,
    logger_name=logger_names,
    message=log_messages
)
def test_structured_logging_with_exceptions(
    level: int,
    logger_name: str,
    message: str
):
    """
    Property 7: Structured logging consistency (exception handling)
    
    For any log entry with exception information, it should include the exception
    in a consistent format.
    
    Validates: Requirements 5.5
    """
    # Create an exception
    try:
        raise ValueError("Test exception")
    except ValueError:
        import sys
        exc_info = sys.exc_info()
    
    # Create a log record with exception info
    record = create_log_record(
        level=level,
        logger_name=logger_name,
        message=message,
        exc_info=exc_info
    )
    
    # Format the log record
    formatter = StructuredFormatter()
    formatted_output = formatter.format(record)
    
    # Parse as JSON
    log_data = json.loads(formatted_output)
    
    # Verify exception field is present
    assert "exception" in log_data, "exception field should be present when exc_info is provided"
    assert isinstance(log_data["exception"], str), "exception should be a string"
    assert "ValueError" in log_data["exception"], "exception should contain exception type"
    assert "Test exception" in log_data["exception"], "exception should contain exception message"


# Feature: iam-user-monitor, Property 7: Structured logging consistency (setup_logging)
@settings(max_examples=100)
@given(
    log_level_str=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "invalid"])
)
def test_setup_logging_consistency(log_level_str: str):
    """
    Property 7: Structured logging consistency (logger setup)
    
    For any log level configuration, setup_logging should return a logger
    with consistent structured formatting.
    
    Validates: Requirements 5.5
    """
    # Set environment variable
    os.environ["LOG_LEVEL"] = log_level_str
    
    # Setup logger
    logger = setup_logging()
    
    # Verify logger is configured
    assert logger is not None, "setup_logging should return a logger"
    assert logger.name == "iam-user-monitor", "logger should have correct name"
    assert len(logger.handlers) > 0, "logger should have at least one handler"
    
    # Verify handler has StructuredFormatter
    handler = logger.handlers[0]
    assert isinstance(handler.formatter, StructuredFormatter), "handler should use StructuredFormatter"
    
    # Capture log output
    stream = StringIO()
    test_handler = logging.StreamHandler(stream)
    test_handler.setFormatter(StructuredFormatter())
    
    test_logger = logging.getLogger("test-logger")
    test_logger.handlers.clear()
    test_logger.addHandler(test_handler)
    test_logger.setLevel(logging.DEBUG)
    
    # Log a message
    test_message = "Test message"
    test_logger.info(test_message)
    
    # Get output
    output = stream.getvalue().strip()
    
    # Verify output is valid JSON with consistent structure
    log_data = json.loads(output)
    assert "timestamp" in log_data, "log should have timestamp field"
    assert "level" in log_data, "log should have level field"
    assert "logger" in log_data, "log should have logger field"
    assert "message" in log_data, "log should have message field"
    assert log_data["message"] == test_message, "message should match"
