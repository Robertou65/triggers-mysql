import sys

import mysql.connector as mysql
from PyQt6.QtWidgets import QApplication

from src.triggers_mysql.config import DB_CONFIG
from src.triggers_mysql.UI import BlogMainWindow, MessageDialog


def main() -> int:
    app = QApplication(sys.argv)

    try:
        connection = mysql.connect(**DB_CONFIG)
        MessageDialog("Database", "Database connected correctly.").exec()
    except mysql.Error as err:
        MessageDialog("Database", f"Database connection failed: {err}").exec()
        return 1

    window = BlogMainWindow(connection)
    window.show()

    exit_code = app.exec()
    if connection.is_connected():
        connection.close()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())