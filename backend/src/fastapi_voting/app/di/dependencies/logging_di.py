import logging
import sys

from fastapi import Request


# --- Инструментарий ---
logger = logging.getLogger("fastapi-voting")


# --- Сервис ---
class LoggingExceptionDI:
    """Сервис для логирования в зависимости от контекста"""

    # --- Свойства класса ---
    available_context = ("HTTP", None)

    # --- Методы класса ---
    def __init__(self, context: str | None = None):
        if context not in self.available_context:
            raise ValueError("Context is not available")

        self.context = context

    def __call__(self, request: Request | None = None):
        self.request = request
        return self


    def info(self, detail: str):
        log_msg = self.get_log_string(detail)
        logger.info(log_msg)

    def warning(self, detail: str):
        log_msg = self.get_log_string(detail)
        logger.warning(log_msg)

    def critical(self, detail: str):
        log_msg = self.get_log_string(detail)
        logger.critical(log_msg)

    def error(self, detail: str):
        log_msg = self.get_log_string(detail)
        logger.error(log_msg)


    def get_log_string(self, detail: str):

        # --- Вспомогательные данные ---
        result = ""

        # --- Данные для логирования ---
        if self.context == "HTTP":
            url = self.request.url.path
            request_method = self.request.method

            user_agent = self.request.headers.get("User-Agent")
            referer = self.request.headers.get("Referer")
            origin = self.request.headers.get("Origin")
            host = self.request.headers.get("Host")

            result += f"{request_method} {url} - Origin: {origin}, User-Agent: {user_agent}, Host: {host}, Referer: {referer} | "

        # --- Формирование ответа ---
        result += f"Detail: {detail}"
        return result