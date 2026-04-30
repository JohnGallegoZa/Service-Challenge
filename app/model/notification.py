from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from app.services.util import generate_unique_id
import os
from abc import ABC, abstractmethod

class NotificationError(Exception):
    pass

class ChannelUnavailableError(NotificacionError):
    pass

class DeliveryError(NotificacionError):
    pass

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, message: str) -> None:
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

class ConsoleChannel(NotificationChannel):
    def send(self, message: str) -> None:
        try:
            print(message)
        except Exception:
            raise DeliveryError("Error de salida")

    def get_channel_name(self) -> str:
        return "Console"

    def is_available(self) -> bool:
        return True

class FileChannel(NotificationChannel):
    def __init__(self, file_path: str):
        self.file_path : str = file_path

    def is_available(self) -> bool:
        pass

    def get_channel_name(self) -> str:
        return f"file: {self.file_path}"

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError("Canal no disponible")
        pass


class MockChannel(NotificationChannel):
    def if_available(self) -> bool:
        return False

    def get_channel_name(self) -> str:
        return "Mock"

    def send(self, message: str) -> None:
        raise ChannelUnavailableError("Error: canal Mock")


class NotificationService:
    def __init__(self, channel: NotificationChannel):
        self._channel = channel
        self._history : list[str]= []

    def send_notification(self, message: str) -> None:
        if not self._channel.is_available():
            raise ChannelUnavailableError("No esta disponible")

        self._channel.send(message)
        self._history.append(message)





