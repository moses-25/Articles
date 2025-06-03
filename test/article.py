from models.author import Author
from models.magazine import Magazine
from models.article import Article
import pytest

@pytest.fixture
def setup_db():
    # Setup test data
    author = Author(name="Test Author")
    author.save()
    magazine = Magazine(name="Test Magazine", category="Testing")
    magazine.save()
    article = Article(title="Test Article", author_id=author.id, magazine_id=magazine.id)
    article.save()
    yield  # Provide a teardown point
    # Cleanup test data
    article.delete()
    magazine.delete()
    author.delete()

def test_article_creation(setup_db):
    article = Article.find_by_title("Test Article")
    assert article is not None
    assert article.title == "Test Article"
    assert article.author_id is not None
    assert article.magazine_id is not None

def test_article_author(setup_db):
    article = Article.find_by_title("Test Article")
    assert article is not None
    author = article.author()
    assert author is not None
    assert author.name == "Test Author"

def test_article_magazine(setup_db):
    article = Article.find_by_title("Test Article")
    assert article is not None
    magazine = article.magazine()
    assert magazine is not None
    assert magazine.name == "Test Magazine"
    assert magazine.category == "Testing"

def test_article_all(setup_db):
    author = Author.find_by_name("Test Author")
    assert author is not None
    magazine = Magazine.find_by_name("Test Magazine")
    assert magazine is not None
    
    article2 = Article(title="Test Article 2", author_id=author.id, magazine_id=magazine.id)
    article2.save()
    
    all_articles = Article.all()
    assert len(all_articles) >= 2
    titles = [article.title for article in all_articles]
    assert "Test Article" in titles
    assert "Test Article 2" in titles
    
    article2.delete()

def test_article_save_and_delete(setup_db):
    author = Author(name="New Test Author")
    author.save()
    magazine = Magazine(name="New Test Magazine", category="New Testing")
    magazine.save()
    
    article = Article(title="New Test Article", author_id=author.id, magazine_id=magazine.id)
    article.save()
    
    found_article = Article.find_by_title("New Test Article")
    assert found_article is not None
    assert found_article.id == article.id
    
    article.delete()
    found_article = Article.find_by_title("New Test Article")
    assert found_article is None
    
    magazine.delete()
    author.delete()