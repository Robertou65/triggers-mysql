# triggers-mysql

Desktop blog manager built with **PyQt6** and **MySQL**.

The application lets you:
- Create blogs from a GUI form
- View blogs and notifications in styled cards
- Delete notifications with confirmation
- Use MySQL triggers to automatically create/delete related records

## Tech Stack

- Python 3.14+
- PyQt6
- mysql-connector-python
- python-dotenv
- uv (dependency management and build backend)

## Project Structure

```text
triggers-mysql/
├── main.py
├── pyproject.toml
├── src/
│   └── triggers_mysql/
│       ├── __init__.py
│       ├── UI.py
│       ├── config.py
│       ├── model_clases.py
│       ├── repository.py
│       └── sql/
│           ├── __init__.py
│           ├── queries.py
│           ├── queries.sql
│           └── triggers.sql
└── README.md
```

## Application Flow

1. `main.py` starts a PyQt6 app.
2. It tries to connect to MySQL using env variables from `.env`.
3. A dialog reports whether DB connection succeeded or failed.
4. On success, the main menu window opens.
5. Actions call repository classes:
	 - `BlogRepository`
	 - `NotificationRepository`

## GUI Windows

- Main menu with vertical buttons
- Create blog window
	- Inputs: title, author, content, date (`QDateEdit` -> `datetime.date`)
	- Buttons: `delete all`, `submit`
- Display all blogs and notifications
	- Blogs: light red cards
	- Notifications: light green cards
	- Shows `no Data` when empty
- Display blogs only
- Display notifications only
- Delete notification
	- Shows notification cards + red `delete` button per item
	- Confirmation dialog before delete
- Exit confirmation dialog

## Database Setup

Create the database and tables before running the app.

Example schema:

```sql
CREATE DATABASE IF NOT EXISTS triggers;
USE triggers;

CREATE TABLE IF NOT EXISTS blog (
		id INT AUTO_INCREMENT PRIMARY KEY,
		title VARCHAR(255) NOT NULL,
		content TEXT NOT NULL,
		blog_date DATE NOT NULL,
		autor VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS notification (
		id INT AUTO_INCREMENT PRIMARY KEY,
		id_blog INT NOT NULL,
		notification_date DATE NOT NULL,
		content TEXT NOT NULL,
		CONSTRAINT fk_notification_blog
				FOREIGN KEY (id_blog) REFERENCES blog(id)
				ON DELETE CASCADE
);
```

Then apply triggers from `src/triggers_mysql/sql/triggers.sql`.

Current triggers:
- After inserting a blog, automatically create a notification
- After deleting a notification, delete its related blog

## Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=triggers
DB_PORT=3306
```

## Installation

Install dependencies (recommended with `uv`):

```bash
uv add pyqt6 mysql-connector-python python-dotenv
```

Or with pip:

```bash
python -m pip install pyqt6 mysql-connector-python python-dotenv
```

## Run the App

```bash
uv run main.py
```

## Build Package

```bash
uv build
```

This generates artifacts in `dist/`.

## Notes

- Source package is `src/triggers_mysql/`.
- Keep this as the single source of truth to avoid duplicate-module import conflicts.
- SQL query templates are loaded by `QueryLoader` from `src/triggers_mysql/sql/queries.sql`.

## Troubleshooting

- `ModuleNotFoundError` for package imports:
	- Ensure code imports from `src.triggers_mysql...` in local run context.
- DB connection dialog shows failure:
	- Verify `.env` values and MySQL server status.
- Trigger behavior not working:
	- Ensure triggers were created in the same database selected by `DB_NAME`.
