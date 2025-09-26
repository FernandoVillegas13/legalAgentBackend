from datetime import datetime
from typing import Any, Optional

class ToolResult:
    def __init__(self, tool_name: str, input_params: dict, result: Any):
        self.tool_name = tool_name
        self.input_params = input_params
        self.result = result
        self.success = True
        self.error_message = None
        self.execution_time = None
        self.timestamp = datetime.now()