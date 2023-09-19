import logging


# Writing your own logger class is not necessary. Use the built-in logging module
# instead. It has all the functionality you have implemented here and more.
class Logger:
    """A class to handle logging of errors, warnings, and messages.

    Attributes:
        config (dict): A dictionary holding the logging configuration settings.
    """

    def __init__(self, config: dict) -> None:
        """Initializes Logger with logging configuration settings.

        Args:
            config (dict): Logging configuration settings dictionary.
        """
        self.log_level = getattr(logging, config["logging"]["level"].upper())
        self.log_file = config["logging"]["logfile"]
        logging.basicConfig(level=self.log_level, filename=self.log_file)

    def log_error(self, error_message: str) -> None:
        """Logs error messages to the configured log file.

        Args:
            error_message (str): Error message to log.
        """
        self._log_message(error_message, log_type="error")

    def log_info(self, info_message: str) -> None:
        """Logs informational messages to the configured log file.

        Args:
            info_message (str): Information message to log.
        """
        self._log_message(info_message, log_type="info")

    def log_warning(self, warning_message: str) -> None:
        """Logs warning messages to the configured log file.

        Args:
            warning_message (str): Warning message to log.
        """
        self._log_message(warning_message, log_type="warning")

    def _log_message(self, message: str, log_type: str) -> None:
        """Logs messages of specified type to the configured log file.

        Args:
            message (str): Message to log.
            log_type (str): Type of log message (e.g., "info", "error", "warning").
        """
        if log_type == "info":
            logging.info(message)
        elif log_type == "warning":
            logging.warning(message)
        elif log_type == "error":
            logging.error(message)
        else:
            raise ValueError(f"Unsupported log_type: {log_type}")

        print(f"[{log_type.upper()}] {message}")
