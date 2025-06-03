from .connection import get_connection
from ..models import Author, Magazine, Article

def seed_database():
    """Populate database with sample data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    
    # Sample authors
    authors = [
        Author(name="Agatha Christie"),
        Author(name="Isaac Asimov"),
        Author(name="Toni Morrison")
    ]
    for author in authors:
        author.save()
    
    # Sample magazines
    magazines = [
        Magazine(name="Mystery Monthly", category="Mystery"),
        Magazine(name="Sci-Fi Chronicles", category="Science Fiction"),
        Magazine(name="Literary Legends", category="Literature")
    ]
    for magazine in magazines:
        magazine.save()
    
    # Sample articles
    articles = [
        {"title": "Murder on the Orient Express", "author": "Agatha Christie", "magazine": "Mystery Monthly"},
        {"title": "Foundation", "author": "Isaac Asimov", "magazine": "Sci-Fi Chronicles"},
        {"title": "Beloved", "author": "Toni Morrison", "magazine": "Literary Legends"}
    ]
    
    for article in articles:
        author = Author.find_by_name(article["author"])
        magazine = Magazine.find_by_name(article["magazine"])
        if author and magazine:  # Ensure author and magazine exist
            Article(
                title=article["title"],
                author_id=author.id,
                magazine_id=magazine.id
            ).save()
    
    conn.close()