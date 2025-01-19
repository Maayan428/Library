import logging

class Logger:
    _log = None

    @staticmethod
    def get_logger():
        if Logger._log is None:
            Logger._log = logging.getLogger("LibraryLogger")
            handler = logging.FileHandler("Action_History.txt")
            formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            Logger._log.setLevel(logging.INFO)
            Logger._log.addHandler(handler)
        return Logger._log

    @staticmethod
    def log_decorator(success_message, fail_message):
        def decorator(func):
            def wrapper(*args, **kwargs):
                log = Logger.get_logger()
                try:
                    result = func(*args, **kwargs)
                    log.info(success_message)
                    return result
                except Exception:
                    log.error(fail_message)
                    return None
            return wrapper
        return decorator