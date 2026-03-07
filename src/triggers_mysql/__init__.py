"""Public package interface for triggers_mysql."""

from .config import DB_CONFIG
from .model_clases import Blog, Notification
from .repository import BlogRepository, NotificationRepository, Repository

__all__ = [
    "DB_CONFIG",
    "Blog",
    "Notification",
    "Repository",
    "BlogRepository",
    "NotificationRepository",
]
