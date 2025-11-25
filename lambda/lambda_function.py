"""
Lambda handler for IAM User Monitor.

This module orchestrates the IAM user scanning, DynamoDB writing, and metrics
emission with comprehensive observability and timeout handling.
"""

import os
from datetime import datetime
from typing import Dict, Any
from logger_config import setup_logging
from iam_scanner import scan_iam_users
from dynamodb_writer import write_user_records
from metrics_emitter import emit_metrics
from concurrency_lock import ConcurrencyLock

# Initialize logger
logger = setup_logging()

# Timeout threshold in milliseconds (30 seconds before timeout)
TIMEOUT_THRESHOLD_MS = 30000


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler entry point for IAM User Monitor.
    
    Orchestrates the complete monitoring workflow:
    1. Acquire concurrency lock
    2. Log invocation start with configuration
    3. Scan all IAM users
    4. Write user records to DynamoDB
    5. Emit CloudWatch metrics
    6. Log summary statistics
    7. Release concurrency lock
    
    Implements timeout detection, graceful handling, and concurrency prevention.
    
    Args:
        event: Lambda event (from EventBridge)
        context: Lambda context object with runtime information
        
    Returns:
        Dictionary with execution results and statistics
    """
    # Record start time
    start_time = datetime.utcnow()
    scan_timestamp = start_time.isoformat() + "Z"
    
    # Read configuration from environment
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    retention_days = int(os.environ.get('RETENTION_DAYS', '90'))
    
    # Initialize execution statistics
    stats = {
        "scan_timestamp": scan_timestamp,
        "total_users": 0,
        "records_written": 0,
        "errors": 0,
        "duration_seconds": 0.0,
        "success": False
    }
    
    # Step 0: Acquire concurrency lock
    lock = ConcurrencyLock(table_name=table_name)
    
    if not lock.acquire():
        # Another execution is in progress - exit immediately
        logger.warning(
            "Concurrency lock acquisition failed - another execution is in progress",
            extra={
                "scan_timestamp": scan_timestamp
            }
        )
        
        _finalize_execution(stats, start_time)
        
        return {
            "statusCode": 200,
            "status": "skipped_concurrent_execution",
            "message": "Another execution is in progress",
            "statistics": {
                "scan_timestamp": stats["scan_timestamp"],
                "duration_seconds": stats["duration_seconds"]
            }
        }
    
    # Log invocation start with configuration
    logger.info(
        "Lambda invocation started",
        extra={
            "scan_timestamp": scan_timestamp,
            "table_name": table_name,
            "log_level": log_level,
            "retention_days": retention_days,
            "function_name": context.function_name if context else "unknown",
            "request_id": context.request_id if context else "unknown"
        }
    )
    
    try:
        # Check timeout before starting scan
        if context and _check_timeout(context):
            logger.warning("Insufficient time remaining before scan - exiting gracefully")
            stats["success"] = False
            _finalize_execution(stats, start_time)
            lock.release()
            return _build_response(stats, "timeout_before_scan")
        
        # Step 1: Scan IAM users
        logger.info("Starting IAM user scan")
        users = scan_iam_users()
        stats["total_users"] = len(users)
        
        logger.info(
            f"IAM scan completed: {stats['total_users']} users found",
            extra={"total_users": stats["total_users"]}
        )
        
        # Check timeout before writing to DynamoDB
        if context and _check_timeout(context):
            logger.warning(
                "Approaching timeout after scan - exiting gracefully",
                extra={"total_users": stats["total_users"]}
            )
            stats["success"] = False
            _finalize_execution(stats, start_time)
            lock.release()
            return _build_response(stats, "timeout_after_scan")
        
        # Step 2: Write user records to DynamoDB
        logger.info(f"Writing {len(users)} user records to DynamoDB")
        write_stats = write_user_records(
            users=users,
            scan_timestamp=scan_timestamp,
            table_name=table_name,
            retention_days=retention_days
        )
        
        stats["records_written"] = write_stats["records_written"]
        stats["errors"] = write_stats["errors"]
        
        logger.info(
            f"DynamoDB write completed: {stats['records_written']} records written, {stats['errors']} errors",
            extra={
                "records_written": stats["records_written"],
                "errors": stats["errors"]
            }
        )
        
        # Determine overall success
        # Success if we scanned users and wrote at least some records (or there were no users)
        stats["success"] = stats["errors"] == 0 or stats["records_written"] > 0
        
        # Finalize execution statistics
        _finalize_execution(stats, start_time)
        
        # Step 3: Emit CloudWatch metrics
        logger.info("Emitting CloudWatch metrics")
        emit_metrics(stats)
        
        # Log summary statistics
        logger.info(
            "Lambda execution completed successfully",
            extra={
                "scan_timestamp": stats["scan_timestamp"],
                "total_users": stats["total_users"],
                "records_written": stats["records_written"],
                "errors": stats["errors"],
                "duration_seconds": stats["duration_seconds"],
                "success": stats["success"]
            }
        )
        
        # Release concurrency lock
        lock.release()
        
        return _build_response(stats, "success")
        
    except Exception as e:
        # Handle any unexpected errors
        logger.error(
            f"Lambda execution failed with error: {str(e)}",
            extra={
                "error_type": type(e).__name__,
                "scan_timestamp": scan_timestamp
            },
            exc_info=True
        )
        
        # Update statistics for failure
        stats["success"] = False
        _finalize_execution(stats, start_time)
        
        # Emit failure metrics
        try:
            emit_metrics(stats)
        except Exception as metrics_error:
            logger.error(f"Failed to emit failure metrics: {str(metrics_error)}")
        
        # Log final summary
        logger.error(
            "Lambda execution failed",
            extra={
                "scan_timestamp": stats["scan_timestamp"],
                "total_users": stats["total_users"],
                "records_written": stats["records_written"],
                "errors": stats["errors"],
                "duration_seconds": stats["duration_seconds"],
                "success": stats["success"]
            }
        )
        
        # Release concurrency lock on error
        lock.release()
        
        return _build_response(stats, "error", str(e))


def _check_timeout(context: Any) -> bool:
    """
    Check if Lambda execution is approaching timeout.
    
    Args:
        context: Lambda context object
        
    Returns:
        True if remaining time is less than threshold, False otherwise
    """
    if not context or not hasattr(context, 'get_remaining_time_in_millis'):
        return False
    
    remaining_time_ms = context.get_remaining_time_in_millis()
    
    if remaining_time_ms < TIMEOUT_THRESHOLD_MS:
        logger.warning(
            f"Approaching timeout: {remaining_time_ms}ms remaining",
            extra={"remaining_time_ms": remaining_time_ms}
        )
        return True
    
    return False


def _finalize_execution(stats: Dict[str, Any], start_time: datetime) -> None:
    """
    Calculate final execution statistics.
    
    Args:
        stats: Statistics dictionary to update
        start_time: Execution start time
    """
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds()
    stats["duration_seconds"] = round(duration, 3)


def _build_response(
    stats: Dict[str, Any],
    status: str,
    error_message: str = None
) -> Dict[str, Any]:
    """
    Build Lambda response dictionary.
    
    Args:
        stats: Execution statistics
        status: Status string (success, error, timeout_before_scan, timeout_after_scan)
        error_message: Optional error message
        
    Returns:
        Response dictionary
    """
    response = {
        "statusCode": 200 if stats["success"] else 500,
        "status": status,
        "statistics": {
            "scan_timestamp": stats["scan_timestamp"],
            "total_users": stats["total_users"],
            "records_written": stats["records_written"],
            "errors": stats["errors"],
            "duration_seconds": stats["duration_seconds"],
            "success": stats["success"]
        }
    }
    
    if error_message:
        response["error"] = error_message
    
    return response
