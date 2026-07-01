
class ExcelBridgeError(Exception):
    """Base exception for all ExcelBridge related errors."""
    pass

class ConnectorAuthError(ExcelBridgeError):
    """Raised when authentication with the data platform fails."""
    pass

class QueryExecutionError(ExcelBridgeError):
    """Raised when a SQL query fails to execute properly."""
    pass

class JobExecutionError(ExcelBridgeError):
    """Raised when a Notebook or Job fails to trigger or complete."""
    pass

class UnsupportedPlatformError(ExcelBridgeError):
    """Raised when a requested platform is not supported by the factory."""
    pass