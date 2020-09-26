import logging

logger = logging.getLogger("sensifai")


class ApiError(Exception):
    def __init__(self, message):
        self.message = message
        logger.error(f"ApiError: {self.message}")
        super().__init__(self.message)


class ClientError(Exception):
    def __init__(self, message):
        self.message = message
        logger.error(f"ClientError: {self.message}")
        super().__init__(self.message)
