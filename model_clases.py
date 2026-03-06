from dataclasses import dataclass
from datetime import date

@dataclass
class Blog:
    id: int
    title: str
    content: str
    blog_date: date
    autor: str

@dataclass
class Notification:
    id: int
    id_blog: int
    notification_date: date
    content: str