from typing import Callable

from mysql.connector.connection_cext import CMySQLConnection
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
	QDateEdit,
	QDialog,
	QFormLayout,
	QFrame,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QMainWindow,
	QPushButton,
	QScrollArea,
	QTextEdit,
	QVBoxLayout,
	QWidget,
)

from .model_clases import Blog, Notification
from .repository import BlogRepository, NotificationRepository


class MessageDialog(QDialog):
	def __init__(self, title: str, message: str, parent: QWidget | None = None):
		super().__init__(parent)
		self.setWindowTitle(title)
		self.setModal(True)
		self.resize(200, 100)

		layout = QVBoxLayout(self)

		label = QLabel(message)
		label.setWordWrap(True)
		layout.addWidget(label)

		ok_button = QPushButton("ok")
		ok_button.clicked.connect(self.accept)
		layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)


class ConfirmDialog(QDialog):
	def __init__(self, title: str, message: str, parent: QWidget | None = None):
		super().__init__(parent)
		self.setWindowTitle(title)
		self.resize(200, 100)
		self.setModal(True)

		layout = QVBoxLayout(self)
		label = QLabel(message)
		label.setWordWrap(True)
		layout.addWidget(label)

		buttons = QHBoxLayout()
		yes_button = QPushButton("yes")
		no_button = QPushButton("not")
		yes_button.clicked.connect(self.accept)
		no_button.clicked.connect(self.reject)

		buttons.addWidget(yes_button)
		buttons.addWidget(no_button)
		layout.addLayout(buttons)


class CreateBlogDialog(QDialog):
	def __init__(self, blog_repo: BlogRepository, parent: QWidget | None = None):
		super().__init__(parent)
		self.blog_repo = blog_repo

		self.setWindowTitle("Create Blog")
		self.resize(560, 420)

		main_layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		self.title_input = QLineEdit()
		self.author_input = QLineEdit()
		self.content_input = QTextEdit()
		self.date_input = QDateEdit()
		self.date_input.setCalendarPopup(True)
		self.date_input.setDate(QDate.currentDate())

		form_layout.addRow("Title:", self.title_input)
		form_layout.addRow("Author:", self.author_input)
		form_layout.addRow("Content:", self.content_input)
		form_layout.addRow("Date:", self.date_input)

		main_layout.addLayout(form_layout)

		buttons_layout = QHBoxLayout()
		delete_all_button = QPushButton("delete all")
		submit_button = QPushButton("submit")

		delete_all_button.clicked.connect(self.clear_inputs)
		submit_button.clicked.connect(self.submit_blog)

		buttons_layout.addWidget(delete_all_button)
		buttons_layout.addWidget(submit_button)
		main_layout.addLayout(buttons_layout)

	def clear_inputs(self) -> None:
		self.title_input.clear()
		self.author_input.clear()
		self.content_input.clear()
		self.date_input.setDate(QDate.currentDate())

	def submit_blog(self) -> None:
		title = self.title_input.text().strip()
		author = self.author_input.text().strip()
		content = self.content_input.toPlainText().strip()

		if not title or not author or not content:
			MessageDialog("Validation", "All fields are required.", self).exec()
			return

		blog = Blog(
			id=0,
			title=title,
			content=content,
			blog_date=self.date_input.date().toPyDate(),
			autor=author,
		)

		try:
			self.blog_repo.insert(blog)
			MessageDialog("Create Blog", "Blog inserted correctly.", self).exec()
			self.accept()
		except Exception as err:
			MessageDialog("Create Blog", f"Insert failed: {err}", self).exec()


class RecordsBaseDialog(QDialog):
	def __init__(self, title: str, parent: QWidget | None = None):
		super().__init__(parent)
		self.setWindowTitle(title)
		self.resize(860, 560)

		self.main_layout = QVBoxLayout(self)

		self.scroll = QScrollArea()
		self.scroll.setWidgetResizable(True)

		self.scroll_widget = QWidget()
		self.content_layout = QVBoxLayout(self.scroll_widget)
		self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		self.scroll.setWidget(self.scroll_widget)
		self.main_layout.addWidget(self.scroll)

		bottom_layout = QHBoxLayout()
		bottom_layout.addStretch(1)
		exit_button = QPushButton("exit")
		exit_button.clicked.connect(self.accept)
		bottom_layout.addWidget(exit_button)
		self.main_layout.addLayout(bottom_layout)

	def _clear_content(self) -> None:
		while self.content_layout.count():
			item = self.content_layout.takeAt(0)
			widget = item.widget()
			child_layout = item.layout()
			if widget is not None:
				widget.deleteLater()
			if child_layout is not None:
				self._delete_layout(child_layout)

	def _delete_layout(self, layout: QVBoxLayout | QHBoxLayout) -> None:
		while layout.count():
			item = layout.takeAt(0)
			widget = item.widget()
			child_layout = item.layout()
			if widget is not None:
				widget.deleteLater()
			if child_layout is not None:
				self._delete_layout(child_layout)

	def _no_data_label(self) -> QLabel:
		label = QLabel("no Data")
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setStyleSheet("font-size: 18px; font-weight: 600;")
		return label

	@staticmethod
	def _make_box(title: str, lines: list[str], bg_color: str) -> QFrame:
		box = QFrame()
		box.setFrameShape(QFrame.Shape.StyledPanel)
		box.setStyleSheet(
			"QFrame {"
			f"background-color: {bg_color};"
			"border: 1px solid #777;"
			"border-radius: 10px;"
			"padding: 8px;"
			"}"
		)

		layout = QVBoxLayout(box)
		header = QLabel(title)
		header.setStyleSheet("font-size: 15px; font-weight: 700;")
		layout.addWidget(header)

		for line in lines:
			label = QLabel(line)
			label.setWordWrap(True)
			layout.addWidget(label)

		return box

	def _add_section_title(self, text: str) -> None:
		title = QLabel(text)
		title.setStyleSheet("font-size: 17px; font-weight: 700; margin-top: 8px;")
		self.content_layout.addWidget(title)


class DisplayAllDialog(RecordsBaseDialog):
	def __init__(
		self,
		blog_repo: BlogRepository,
		notification_repo: NotificationRepository,
		parent: QWidget | None = None,
	):
		super().__init__("Display All Blogs and Notifications", parent)
		self.blog_repo = blog_repo
		self.notification_repo = notification_repo
		self.refresh()

	def refresh(self) -> None:
		self._clear_content()

		blogs = self.blog_repo.find_all()
		notifications = self.notification_repo.find_all()

		self._add_section_title("Blogs")
		if not blogs:
			self.content_layout.addWidget(self._no_data_label())
		else:
			for blog in blogs:
				box = self._make_box(
					title=f"Blog ID: {blog.id}",
					lines=[
						f"Title: {blog.title}",
						f"Author: {blog.autor}",
						f"Date: {blog.blog_date}",
						f"Content: {blog.content}",
					],
					bg_color="#ffd6d6",
				)
				self.content_layout.addWidget(box)

		self._add_section_title("Notifications")
		if not notifications:
			self.content_layout.addWidget(self._no_data_label())
		else:
			for notification in notifications:
				box = self._make_box(
					title=f"Notification ID: {notification.id}",
					lines=[
						f"Blog ID: {notification.id_blog}",
						f"Date: {notification.notification_date}",
						f"Content: {notification.content}",
					],
					bg_color="#d6f5d6",
				)
				self.content_layout.addWidget(box)


class DisplayBlogsDialog(RecordsBaseDialog):
	def __init__(self, blog_repo: BlogRepository, parent: QWidget | None = None):
		super().__init__("Display All Blogs", parent)
		self.blog_repo = blog_repo
		self.refresh()

	def refresh(self) -> None:
		self._clear_content()
		blogs = self.blog_repo.find_all()

		if not blogs:
			self.content_layout.addWidget(self._no_data_label())
			return

		for blog in blogs:
			box = self._make_box(
				title=f"Blog ID: {blog.id}",
				lines=[
					f"Title: {blog.title}",
					f"Author: {blog.autor}",
					f"Date: {blog.blog_date}",
					f"Content: {blog.content}",
				],
				bg_color="#ffd6d6",
			)
			self.content_layout.addWidget(box)


class DisplayNotificationsDialog(RecordsBaseDialog):
	def __init__(self, notification_repo: NotificationRepository, parent: QWidget | None = None):
		super().__init__("Display All Notifications", parent)
		self.notification_repo = notification_repo
		self.refresh()

	def refresh(self) -> None:
		self._clear_content()
		notifications = self.notification_repo.find_all()

		if not notifications:
			self.content_layout.addWidget(self._no_data_label())
			return

		for notification in notifications:
			box = self._make_box(
				title=f"Notification ID: {notification.id}",
				lines=[
					f"Blog ID: {notification.id_blog}",
					f"Date: {notification.notification_date}",
					f"Content: {notification.content}",
				],
				bg_color="#d6f5d6",
			)
			self.content_layout.addWidget(box)


class DeleteNotificationsDialog(RecordsBaseDialog):
	def __init__(self, notification_repo: NotificationRepository, parent: QWidget | None = None):
		super().__init__("Delete Notifications", parent)
		self.notification_repo = notification_repo
		self.refresh()

	def refresh(self) -> None:
		self._clear_content()
		notifications = self.notification_repo.find_all()

		if not notifications:
			self.content_layout.addWidget(self._no_data_label())
			return

		for notification in notifications:
			row = QWidget()
			row_layout = QHBoxLayout(row)

			box = self._make_box(
				title=f"Notification ID: {notification.id}",
				lines=[
					f"Blog ID: {notification.id_blog}",
					f"Date: {notification.notification_date}",
					f"Content: {notification.content}",
				],
				bg_color="#d6f5d6",
			)

			delete_button = QPushButton("delete")
			delete_button.setStyleSheet(
				"QPushButton {"
				"background-color: #d9534f;"
				"color: white;"
				"font-weight: 700;"
				"padding: 8px 12px;"
				"border: none;"
				"border-radius: 6px;"
				"}"
			)
			delete_button.clicked.connect(
				self._build_delete_handler(notification.id)
			)

			row_layout.addWidget(box, stretch=1)
			row_layout.addWidget(delete_button, stretch=0, alignment=Qt.AlignmentFlag.AlignVCenter)

			self.content_layout.addWidget(row)

	def _build_delete_handler(self, notification_id: int) -> Callable[[], None]:
		def _delete() -> None:
			confirm = ConfirmDialog(
				"Delete Notification",
				f"Are you sure to delete notification with ID={notification_id}",
				self,
			)

			if confirm.exec() == QDialog.DialogCode.Accepted:
				try:
					self.notification_repo.delete(notification_id)
					self.refresh()
				except Exception as err:
					MessageDialog("Delete Notification", f"Delete failed: {err}", self).exec()

		return _delete


class BlogMainWindow(QMainWindow):
	def __init__(self, connection: CMySQLConnection):
		super().__init__()
		self.connection = connection
		self.blog_repo = BlogRepository(connection)
		self.notification_repo = NotificationRepository(connection)
		self._allow_close = False

		self.setWindowTitle("Blog Program")
		self.resize(420, 460)

		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		layout = QVBoxLayout(central_widget)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		title = QLabel("Blog Program")
		title.setStyleSheet("font-size: 22px; font-weight: 700; margin-bottom: 8px;")
		title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(title)

		buttons_config = [
			("create a new blog", self.open_create_blog),
			("display all blogs and notifications", self.open_display_all),
			("display all blogs", self.open_display_blogs),
			("display all notifications", self.open_display_notifications),
			("delete notification", self.open_delete_notifications),
			("exit", self.handle_exit),
		]

		for text, callback in buttons_config:
			button = QPushButton(text)
			button.setMinimumHeight(44)
			button.clicked.connect(callback)
			layout.addWidget(button)

	def open_create_blog(self) -> None:
		CreateBlogDialog(self.blog_repo, self).exec()

	def open_display_all(self) -> None:
		try:
			DisplayAllDialog(self.blog_repo, self.notification_repo, self).exec()
		except Exception as err:
			MessageDialog("Display", f"Error loading data: {err}", self).exec()

	def open_display_blogs(self) -> None:
		try:
			DisplayBlogsDialog(self.blog_repo, self).exec()
		except Exception as err:
			MessageDialog("Display Blogs", f"Error loading data: {err}", self).exec()

	def open_display_notifications(self) -> None:
		try:
			DisplayNotificationsDialog(self.notification_repo, self).exec()
		except Exception as err:
			MessageDialog("Display Notifications", f"Error loading data: {err}", self).exec()

	def open_delete_notifications(self) -> None:
		try:
			DeleteNotificationsDialog(self.notification_repo, self).exec()
		except Exception as err:
			MessageDialog("Delete Notifications", f"Error loading data: {err}", self).exec()

	def handle_exit(self) -> None:
		confirm = ConfirmDialog("Exit", "Do you want to exit?", self)
		if confirm.exec() == QDialog.DialogCode.Accepted:
			self._allow_close = True
			self.close()

	def closeEvent(self, event) -> None:  # type: ignore[override]
		if self._allow_close:
			event.accept()
			return

		confirm = ConfirmDialog("Exit", "Do you want to exit?", self)
		if confirm.exec() == QDialog.DialogCode.Accepted:
			self._allow_close = True
			event.accept()
		else:
			event.ignore()
