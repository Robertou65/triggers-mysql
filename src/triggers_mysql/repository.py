from abc import ABC, abstractmethod
from dataclasses import astuple
from typing import TypeVar, Generic, List
from mysql.connector.connection_cext import CMySQLConnection

from .model_clases import Blog, Notification
from .sql.queries import QueryLoader

T = TypeVar('T')

class Repository(ABC, Generic[T]):
    @abstractmethod
    def insert(self, item:T) -> None:
        pass

    @abstractmethod
    def find_by_id(self, item_id:int) -> T:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def delete(self, item_id:int) -> None:
        pass

class BlogRepository(Repository[Blog]):
    def __init__(self, connection:CMySQLConnection):
        self.connection = connection

    def insert(self, item:Blog) -> None:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('insert_blog')
            values = astuple(item)[1:]

            cursor.execute(sql, values)
            self.connection.commit()
        finally:
            cursor.close()

    def find_by_id(self, item_id:int) -> Blog:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('find_id_blog')

            cursor.execute(sql, (item_id,))
            result = cursor.fetchone()

            if result is None:
                raise ValueError(f"Blog with id {item_id} not found")

            return Blog(*result)
        finally:
            cursor.close()

    def find_all(self) -> List[Blog]:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('find_all_blog')

            cursor.execute(sql)
            result = cursor.fetchall()

            return [Blog(*row) for row in result]
        finally:
            cursor.close()
        
    def delete(self, item_id:int) -> None:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('delete_blog')

            cursor.execute(sql, (item_id,))
            self.connection.commit()

        finally:
            cursor.close()

class NotificationRepository(Repository[Notification]):
    def __init__(self, connection:CMySQLConnection):
        self.connection = connection

    def insert(self, item:Notification) -> None:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('insert_notification')
            values = astuple(item)[1:]

            cursor.execute(sql, values)
            self.connection.commit()

        finally:
            cursor.close()

    def find_by_id(self, item_id:int) -> Notification:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('find_id_notification')

            cursor.execute(sql, (item_id,))
            result = cursor.fetchone()

            if result is None:
                raise ValueError(f"Notification with id {item_id} not found")

            return Notification(*result)
        finally:
            cursor.close()

    def find_all(self) -> List[Notification]:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('find_all_notification')

            cursor.execute(sql)
            result = cursor.fetchall()

            return [Notification(*row) for row in result]
        finally:
            cursor.close()

    def delete(self, item_id:int) -> None:
        try:
            cursor = self.connection.cursor()

            sql = QueryLoader().get('delete_notification')

            cursor.execute(sql, (item_id,))
            self.connection.commit()

        finally:
            cursor.close()