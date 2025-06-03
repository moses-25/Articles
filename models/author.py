from db.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
            else:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    def delete(self):
        if not self.id:
            raise ValueError("Author must have an ID to be deleted.")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM authors WHERE id = ?", (self.id,))
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
            row = cursor.fetchone()
        finally:
            conn.close()
        if row:
            return cls(id=row['id'], name=row['name'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
        finally:
            conn.close()
        if row:
            return cls(id=row['id'], name=row['name'])
        return None

    def articles(self):
        from models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [Article(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]

    def magazines(self):
        from models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [Magazine(id=row['id'], name=row['name'], category=row['category']) for row in rows]

    def add_article(self, magazine, title):
        from models.article import Article
        if not self.id:
            raise ValueError("Author must be saved before adding articles.")
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [row['category'] for row in rows]