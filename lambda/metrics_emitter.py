"""
CloudWatch metrics emitter module for IAM User Monitor.

This module handles publishing custom CloudWatch metrics for monitoring
the IAM user scanning operations.
"""

import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
from logger_config import setup_logging

# Initialize logger
logger = setup_logging()


def emit_metrics(stats: Dict[str, Any]) -> None:
    """
    Emit custom CloudWatch metrics for IAM user monitoring.
    
    Publishes the following metrics to CloudWatch:
    - UsersScanned: Count of users scanned
    - RecordsWritten: Count of records written to DynamoDB
    - Errors: Count of errors encountered
    - Duration: Execution duration in milliseconds
    - Success: Binary success indicator (1 or 0)
    
    Metric emission failures are logged but do not raise exceptions,
    ensuring they don't block the main monitoring workflow.
    
    Args:
        stats: Dictionary containing execution statistics with keys:
            - total_users: Number of users scanned
            - records_written: Number of records written to DynamoDB
            - errors: Number of errors encountered
            - duration_seconds: Execution duration in seconds
            - success: Boolean indicating overall success
    """
    try:
        # Create CloudWatch client
        cloudwatch = boto3.client('cloudwatch')
        
        # Prepare metric data
        metric_data = []
        
        # UsersScanned metric
        if 'total_users' in stats:
            metric_data.append({
                'MetricName': 'UsersScanned',
                'Value': float(stats['total_users']),
                'Unit': 'Count'
            })
        
        # RecordsWritten metric
        if 'records_written' in stats:
            metric_data.append({
                'MetricName': 'RecordsWritten',
                'Value': float(stats['records_written']),
                'Unit': 'Count'
            })
        
        # Errors metric
        if 'errors' in stats:
            metric_data.append({
                'MetricName': 'Errors',
                'Value': float(stats['errors']),
                'Unit': 'Count'
            })
        
        # Duration metric (convert seconds to milliseconds)
        if 'duration_seconds' in stats:
            duration_ms = stats['duration_seconds'] * 1000
            metric_data.append({
                'MetricName': 'Duration',
                'Value': duration_ms,
                'Unit': 'Milliseconds'
            })
        
        # Success metric (binary indicator)
        if 'success' in stats:
            success_value = 1.0 if stats['success'] else 0.0
            metric_data.append({
                'MetricName': 'Success',
                'Value': success_value,
                'Unit': 'None'
            })
        
        # Publish metrics if we have any
        if metric_data:
            cloudwatch.put_metric_data(
                Namespace='IAMUserMonitor',
                MetricData=metric_data
            )
            
            logger.info(
                f"Successfully emitted {len(metric_data)} CloudWatch metrics",
                extra={
                    "metrics_count": len(metric_data),
                    "metrics": [m['MetricName'] for m in metric_data]
                }
            )
        else:
            logger.warning("No metrics to emit - stats dictionary was empty or missing expected keys")
    
    except ClientError as e:
        # Log AWS-specific error details but don't raise
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
        request_id = e.response.get('ResponseMetadata', {}).get('RequestId', 'Unknown')
        
        logger.error(
            f"CloudWatch API error during metric emission: {error_message}",
            extra={
                "error_code": error_code,
                "error_type": "ClientError",
                "request_id": request_id
            }
        )
        # Non-blocking: do not raise exception
        
    except Exception as e:
        # Log unexpected errors but don't raise
        logger.error(
            f"Unexpected error during metric emission: {str(e)}",
            extra={
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        # Non-blocking: do not raise exception
