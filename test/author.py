from models.author import Author
from models.magazine import Magazine
from models.article import Article
import pytest

@pytest.fixture
def setup_db():
    author = Author(name="Test Author")
    author.save()
    magazine = Magazine(name="Test Magazine", category="Testing")
    magazine.save()
    article = Article(title="Test Article", author_id=author.id, magazine_id=magazine.id)
    article.save()
    yield
    article.delete()
    magazine.delete()
    author.delete()

def test_author_creation(setup_db):
    author = Author.find_by_name("Test Author")
    assert author is not None
    assert author.name == "Test Author"

def test_author_articles(setup_db):
    author = Author.find_by_name("Test Author")
    articles = author.articles
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_author_magazines(setup_db):
    author = Author.find_by_name("Test Author")
    magazines = author.magazines
    assert len(magazines) == 1
    assert magazines[0].name == "Test Magazine"