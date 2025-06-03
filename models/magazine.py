from db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?", 
                    (self.name, self.category, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)", 
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    def delete(self):
        if not self.id:
            raise ValueError("Cannot delete a magazine without an ID.")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM magazines WHERE id = ?", (self.id,))
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
            row = cursor.fetchone()
        finally:
            conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
        finally:
            conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [cls(id=row['id'], name=row['name'], category=row['category']) for row in rows]

    def articles(self):
        from models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [
            Article(
                id=row['id'], 
                title=row['title'], 
                author_id=row['author_id'], 
                magazine_id=row['magazine_id']
            ) for row in rows
        ]

    def contributors(self):
        from models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT a.* FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [Author(id=row['id'], name=row['name']) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [row['title'] for row in rows]

    def contributing_authors(self):
        from models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT a.*, COUNT(ar.id) as article_count
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
                GROUP BY a.id
                HAVING article_count > 2
            """, (self.id,))
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [Author(id=row['id'], name=row['name']) for row in rows]

    @classmethod
    def magazines_with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.* FROM magazines m
                JOIN (
                    SELECT magazine_id, COUNT(DISTINCT author_id) as author_count
                    FROM articles
                    GROUP BY magazine_id
                    HAVING author_count >= 2
                ) a ON m.id = a.magazine_id
            """)
            rows = cursor.fetchall()
        finally:
            conn.close()
        return [cls(id=row['id'], name=row['name'], category=row['category']) for row in rows]