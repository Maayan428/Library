import logging


class Logger:
    """
    Logger class for managing application-wide logging.
    - Logs messages to 'Action_History.txt'.
    - Provides a decorator for automatically logging the success or failure of functions.
    """
    _log = None

    @staticmethod
    def get_logger():
        """
        Returns a singleton logger instance.
        - If the logger does not exist, initializes it with a file handler and formatter.
        - Logs messages with a timestamp and message content.
        """
        if Logger._log is None:
            Logger._log = logging.getLogger("LibraryLogger")
            handler = logging.FileHandler("Action_History.txt")  # Logs are written to this file.
            formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            Logger._log.setLevel(logging.INFO)  # Sets the logging level to INFO.
            Logger._log.addHandler(handler)
        return Logger._log

    @staticmethod
    def log_decorator(success_message, fail_message):
        """
        Decorator for logging the execution status of a function.
        - Logs 'success_message' if the function executes successfully.
        - Logs 'fail_message' if the function raises an exception.

        Args:
            success_message (str): Message to log on successful execution.
            fail_message (str): Message to log on failure.

        Returns:
            Decorated function with logging.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                log = Logger.get_logger()
                try:
                    result = func(*args, **kwargs)
                    log.info(success_message)  # Log success message.
                    return result
                except Exception:
                    log.error(fail_message)  # Log failure message.
                    return None

            return wrapper

        return decorator