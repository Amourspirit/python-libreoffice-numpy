class OxtLoggerDummy:
    """Dummy Logger Class"""

    def __init__(self, log_file: str = "", log_name: str = "", *args, **kwargs):
        self.log_file = False
        self.is_debug = True
        self.is_info = True
        self.is_warning = True
        self.is_error = True

    def setLevel(self, level):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def warn(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, exc_info=True, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass

    def fatal(self, msg, *args, **kwargs):
        pass
