INSERT INTO blog (title, content, blog_date, autor) VALUES (%s,%s,%s,%s);

SELECT id, title, content, blog_date, autor FROM blog WHERE id = %s;

SELECT id, title, content, blog_date, autor FROM blog;

DELETE FROM blog WHERE id = %s;

INSERT INTO notification (id_blog, notification_date, content) VALUES (%s,%s,%s);

SELECT id, id_blog, notification_date, content FROM notification WHERE id = %s;

SELECT id, id_blog, notification_date, content FROM notification;

DELETE FROM notification WHERE id = %s;

