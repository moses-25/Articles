from models.author import Author
from models.magazine import Magazine
from models.article import Article
from db.connection import get_connection

def setup_sample_data():
    """Create sample data for demonstration purposes."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    
    # Create authors
    authors = [
        Author(name="Isaac Asimov"),
        Author(name="Arthur C. Clarke"),
        Author(name="Philip K. Dick"),
        Author(name="Ursula K. Le Guin")
    ]
    for author in authors:
        author.save()
    
    # Create magazines
    magazines = [
        Magazine(name="Science Fiction Weekly", category="Science Fiction"),
        Magazine(name="Galactic Chronicles", category="Space Opera"),
        Magazine(name="Dystopian Times", category="Dystopian"),
        Magazine(name="Literary Legends", category="General Fiction")
    ]
    for magazine in magazines:
        magazine.save()
        
    # Create articles
    articles = [
        {"title": "Foundation", "author": "Isaac Asimov", "magazine": "Science Fiction Weekly"},
        {"title": "2001: A Space Odyssey", "author": "Arthur C. Clarke", "magazine": "Galactic Chronicles"},
        {"title": "Do Androids Dream of Electric Sheep?", "author": "Philip K. Dick", "magazine": "Dystopian Times"},
        {"title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "magazine": "Science Fiction Weekly"},
        {"title": "I, Robot", "author": "Isaac Asimov", "magazine": "Literary Legends"},
        {"title": "Childhood's End", "author": "Arthur C. Clarke", "magazine": "Galactic Chronicles"},
        {"title": "The Man in the High Castle", "author": "Philip K. Dick", "magazine": "Dystopian Times"},
        {"title": "A Wizard of Earthsea", "author": "Ursula K. Le Guin", "magazine": "Literary Legends"}
    ]
    
    for article_data in articles:
        author = Author.find_by_name(article_data["author"])
        magazine = Magazine.find_by_name(article_data["magazine"])
        article = Article(
            title=article_data["title"],
            author_id=author.id,
            magazine_id=magazine.id
        )
        article.save()
    
    conn.close()

def run_demo_queries():
    """Run and print results of example queries."""
    print("\n=== DEMONSTRATION QUERIES ===\n")
    
    # 1. Get all articles by Isaac Asimov
    print("1. All articles by Isaac Asimov:")
    isaac_asimov = Author.find_by_name("Isaac Asimov")
    for article in isaac_asimov.articles():
        print(f"- {article.title}")
    print()
    
    # 2. Find all magazines Isaac Asimov has contributed to
    print("2. Magazines Isaac Asimov has contributed to:")
    for magazine in isaac_asimov.magazines():
        print(f"- {magazine.name} ({magazine.category})")
    print()
    
    # 3. Get all authors who have written for Science Fiction Weekly
    print("3. Authors who have written for Science Fiction Weekly:")
    science_fiction_weekly = Magazine.find_by_name("Science Fiction Weekly")
    for author in science_fiction_weekly.contributors():
        print(f"- {author.name}")
    print()
    
    # 4. Find magazines with articles by at least 2 different authors
    print("4. Magazines with articles by at least 2 authors:")
    for magazine in Magazine.magazines_with_multiple_authors():
        print(f"- {magazine.name} ({magazine.category})")
        print("  Contributors:")
        for author in magazine.contributors():
            print(f"  - {author.name}")
    print()
    
    # 5. Count the number of articles in each magazine
    print("5. Article count per magazine:")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, COUNT(a.id) as article_count
        FROM magazines m
        LEFT JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
        ORDER BY article_count DESC
    """)
    for row in cursor.fetchall():
        print(f"- {row['name']}: {row['article_count']} articles")
    conn.close()
    print()
    
    # 6. Find the author who has written the most articles
    print("6. Author with most articles:")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.name, COUNT(ar.id) as article_count
        FROM authors a
        JOIN articles ar ON a.id = ar.author_id
        GROUP BY a.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    print(f"- {row['name']} with {row['article_count']} articles")
    conn.close()
    print()
    
    # 7. Show contributing authors (with >2 articles) for each magazine
    print("7. Contributing authors (with >2 articles) per magazine:")
    for magazine in Magazine.all():
        contributing_authors = magazine.contributing_authors()
        if contributing_authors:
            print(f"- {magazine.name}:")
            for author in contributing_authors:
                print(f"  - {author.name}")
    print()

def main():
    print("Setting up sample data...")
    setup_sample_data()
    
    run_demo_queries()
    
    print("=== DEMONSTRATION COMPLETE ===")

if __name__ == "__main__":
    main()