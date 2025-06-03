from db.connection import get_connection

class Article:
    def __init__(self, id=None, title=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute("""
                    UPDATE articles 
                    SET title = ?, author_id = ?, magazine_id = ? 
                    WHERE id = ?
                """, (self.title, self.author_id, self.magazine_id, self.id))
            else:
                cursor.execute("""
                    INSERT INTO articles (title, author_id, magazine_id) 
                    VALUES (?, ?, ?)
                """, (self.title, self.author_id, self.magazine_id))
                self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    def delete(self):
        if not self.id:
            raise ValueError("Cannot delete an article without an ID.")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM articles WHERE id = ?", (self.id,))
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
            row = cursor.fetchone()
        finally:
            conn.close()
        if row:
            return cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id'])
        return None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
            row = cursor.fetchone()
        finally:
            conn.close()
        if row:
            return cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id'])
        return None

    def author(self):
        from models.author import Author
        if not self.author_id:
            return None
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from models.magazine import Magazine
        if not self.magazine_id:
            return None
        return Magazine.find_by_id(self.magazine_id)

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles")
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]