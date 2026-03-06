CREATE TRIGGER after_user_insert_blog
AFTER INSERT ON blog
FOR EACH ROW 
INSERT INTO notification (id_blog, notification_date, content)
VALUES (NEW.id, NEW.blog_date, CONCAT('New blog created: @', NEW.autor, ', ', NEW.title));


CREATE TRIGGER after_user_delete_notification
AFTER DELETE ON notification
FOR EACH ROW
DELETE FROM blog WHERE id = OLD.id_blog;