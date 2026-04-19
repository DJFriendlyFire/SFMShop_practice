import logging


class LogService:
    def __init__(self, filename: str = "app.log"):

        logging.basicConfig(
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(filename),
                logging.StreamHandler(),
            ],
        )

        self.logger = logging.getLogger(__name__)

    def info(self, message: str, **kwargs):
        self.logger.info(f"{message} | {kwargs}")

    def error(self, message: str, **kwargs):
        self.logger.error(f"{message} | {kwargs}")

    def warning(self, message: str, **kwargs):
        self.logger.warning(f"{message} | {kwargs}")

    def critical(self, message: str, **kwargs):
        self.logger.critical(f"{message} | {kwargs}")


log_service = LogService()
