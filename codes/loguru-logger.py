import os
import sys
from pathlib import Path
from loguru import logger
from typing import Optional, Callable

class CustomLogger:

    def __init__(self,
                 default_level="INFO",
                 ):

        logger.remove()
        self.logger = logger
        self.default_level = default_level
        self.handlers = {}  # for saving the info of the added handlers
        self.levels = {}    # for saving the info of the added levels

    def add_level(self,
                  name: str,
                  no: int,
                  color: Optional[str] = None):
        """
        add a custom log level.
        
        Args:
            name (str): custom level name.
            no (int): the number of the level, for comparing the level.
            color (str, optional): the color of the level in the terminal, e.g. "<cyan>".
        """
        try:
            self.logger.level(name, no=no, color=color)
            self.levels[name] = {"no": no, "color": color}
            self.logger.info(f"successfully add a custom level: {name} (number: {no})")
        except Exception as e:
            self.logger.error(f"failed to add a custom level {name}: {e}")

    def add_handler(self,
                    handler_type: str = "stdout",
                    level: Optional[str] = None,
                    output_path: Optional[str] = None,
                    rotation: Optional[str] = None,
                    retention: Optional[str] = None,
                    compression: Optional[str] = None,
                    format_str: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <10} | {message}",
                    filter_func: Optional[Callable] = None,
                    handler_id: Optional[str] = None,
                    ):
        """
        add a log handler, support stdout or file output.
        
        Args:
            handler_type (str): stdout or file
            level (str, optional):
                log level, may assigned via env. var's, e.g. LOG_LEVEL="DEBUG" / DEBUG=True
            format_str (str): log output format.
            filter_func (callable, optional): filter function
            handler_id (str, optional): custom handler id, auto generated if not provided.

            - for file output:
                output_path (str, optional): for file output, specify the file path.
                rotation (str, optional): file rotation condition, e.g. "500 MB".
                retention (str, optional): retention condition of the old logs, e.g. "10 days".
                compression (str, optional): compression format, e.g. "zip".
        
        Returns:
            int: handler id
        """
        level = None or os.environ.get("LOG_LEVEL", None)
        if level is None:
            is_debug_mode = os.environ.get("DEBUG", "False").lower() in ["true", "1"]
            level = self.default_level if not is_debug_mode else "DEBUG"

        try:
            if handler_type.lower() == "stdout":
                handler_id_actual = self.logger.add(
                    sink=sys.stdout,
                    level=level,
                    format=format_str,
                    filter=filter_func
                )
                handler_name = handler_id if handler_id else f"stdout_handler_{handler_id_actual}"
                self.handlers[handler_name] = {
                    "type": "stdout",
                    "level": level,
                    "id": handler_id_actual
                }
                return handler_id_actual

            elif handler_type.lower() == "file":
                if not output_path:
                    raise ValueError("file output must specify the output_path")
                
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                handler_id_actual = self.logger.add(
                    sink=output_path,
                    level=level,
                    rotation=rotation,
                    retention=retention,
                    compression=compression,
                    format=format_str,
                    filter=filter_func
                )
                handler_name = handler_id if handler_id else f"file_handler_{handler_id_actual}"
                self.handlers[handler_name] = {
                    "type": "file",
                    "level": level,
                    "path": output_path,
                    "id": handler_id_actual
                }
                self.logger.info(f"successfully add a file output handler: {handler_name}, path: {output_path}")
                return handler_id_actual

            else:
                raise ValueError(f"unsupported handler type: {handler_type}")
        except Exception as e:
            self.logger.error(f"failed to add a handler: {e}")
            return None

    def remove_handler(self, handler_id_or_name):
        """
        remove a specified handler.
        
        Args:
            handler_id_or_name (str or int): handler id or name
        """
        try:
            if isinstance(handler_id_or_name, str) and handler_id_or_name in self.handlers:
                handler_id = self.handlers[handler_id_or_name]["id"]
                self.logger.remove(handler_id)
                self.handlers.pop(handler_id_or_name)
                self.logger.info(f"successfully remove a handler: {handler_id_or_name}")
            elif isinstance(handler_id_or_name, int):
                self.logger.remove(handler_id_or_name)
                for name, info in list(self.handlers.items()):
                    if info["id"] == handler_id_or_name:
                        del self.handlers[name]

        except Exception as e:
            self.logger.error(f"failed to remove a handler: {e}")

    def get_logger(self):
        return self.logger


if __name__ == "__main__":
    # initialize the logger
    custom_logger = CustomLogger(default_level="DEBUG")

    # add a custom level
    custom_logger.add_level("TEMP", no=25, color="<cyan>")

    # add a stdout handler
    custom_logger.add_handler(
        handler_type="stdout",
        level="DEBUG",
        handler_id="stdout_main"
    )

    # add a system log file handler
    custom_logger.add_handler(
        handler_type="file",
        level="INFO",
        output_path="logs/system.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        filter_func=lambda record: record["level"].name != "TEMP",
        handler_id="system_file"
    )

    # add a model temp result log file handler
    custom_logger.add_handler(
        handler_type="file",
        level="TEMP",
        output_path="logs/model_temp.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        filter_func=lambda record: record["level"].name == "TEMP",
        handler_id="model_temp_file"
    )

    # get the logger object for testing
    logger = custom_logger.get_logger()
    logger.debug("this is a debug message")
    logger.info("this is a system info message")
    logger.warning("this is a system warning message")
    logger.error("this is a system error message")
    logger.log("TEMP", "this is a model temp result message")

    # remove a handler for testing
    custom_logger.remove_handler("stdout_main")
    logger.info("after removing the stdout handler, the message should not be displayed in the terminal")
