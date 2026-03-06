import mysql.connector as mysql
from mysql.connector.connection_cext import CMySQLConnection
import datetime, subprocess

from config import DB_CONFIG
from repository import BlogRepository, NotificationRepository
from model_clases import Blog, Notification
from sql.queries import QueryLoader

def ask_for_data() -> Blog:
    return Blog(
        id=0,
        title=str(input("Type a title for your blog: ")),
        content=str(input("Enter your blog content: ")),
        blog_date=datetime.date.today(),
        autor=str(input("Enter your name: "))
    )

def item_to_str(item:Blog | Notification) -> str:
    if isinstance(item, Blog):
        return f"ID: {item.id}\nBlog: {item.title} by {item.autor} on {item.blog_date}\nContent: {item.content}"
    if isinstance(item, Notification):
        return f"ID: {item.id}\nNotification: {item.content} on {item.notification_date}"

def display_text() -> int:
    print("-"*100)
    print("Blog Program")
    print("-"*100)
    print("1. create a new blog")
    print("2. display all blogs and notifications")
    print("3. display all blogs")
    print("4. display all notifications")
    print("5. delete notification")
    print("6. clean Terminal")
    print("7. exit")
    print("-"*100)
    return int(input("Option: "))

def main():
    try:
        conn = mysql.connect(**DB_CONFIG)
        while True:
            option = display_text()
            print("-"*100)

            if option == 1:
                blog = ask_for_data()
                BlogRepository(conn).insert(blog)
            if option == 2:
                blogs = BlogRepository(conn).find_all()
                notifications = NotificationRepository(conn).find_all()

                for b, n in zip(blogs, notifications):
                    print(f"{item_to_str(b)}\n\n{item_to_str(n)}\n{"-"*100}6")
            if option == 3:
                blogs = BlogRepository(conn).find_all()

                for b in blogs:
                    print(f"{item_to_str(b)}\n{"-"*100}")
            if option == 4:
                notifications = NotificationRepository(conn).find_all()

                for n in notifications:
                    print(f"{item_to_str(n)}\n{"-"*100}")
            if option == 5:
                item_id = int(input("Enter the notification id to delete: "))

                NotificationRepository(conn).delete(item_id)
            if option == 6:
                subprocess.run(['clear'])
            if option == 7:
                break

        conn.close()
    except mysql.Error as err:
        raise RuntimeError(err) from err
    except ValueError as err:
        raise RuntimeError(err) from err
    
if __name__ == "__main__":
    main()

    #result = subprocess.run(['clear'])