from models.author import Author
from models.magazine import Magazine
from models.article import Article
import pytest

@pytest.fixture
def setup_db():
    author1 = Author(name="Test Author 1")
    author1.save()
    author2 = Author(name="Test Author 2")
    author2.save()
    magazine = Magazine(name="Test Magazine", category="Testing")
    magazine.save()
    article1 = Article(title="Test Article 1", author_id=author1.id, magazine_id=magazine.id)
    article1.save()
    article2 = Article(title="Test Article 2", author_id=author1.id, magazine_id=magazine.id)
    article2.save()
    article3 = Article(title="Test Article 3", author_id=author2.id, magazine_id=magazine.id)
    article3.save()
    yield
    article3.delete()
    article2.delete()
    article1.delete()
    magazine.delete()
    author2.delete()
    author1.delete()

def test_magazine_creation(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    assert magazine is not None
    assert magazine.name == "Test Magazine"
    assert magazine.category == "Testing"

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    articles = magazine.articles()
    assert len(articles) == 3
    titles = [article.title for article in articles]
    assert "Test Article 1" in titles
    assert "Test Article 2" in titles
    assert "Test Article 3" in titles

def test_magazine_contributors(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    contributors = magazine.contributors()
    assert len(contributors) == 2
    names = [author.name for author in contributors]
    assert "Test Author 1" in names
    assert "Test Author 2" in names

def test_magazine_article_titles(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    titles = magazine.article_titles()
    assert len(titles) == 3
    assert "Test Article 1" in titles
    assert "Test Article 2" in titles
    assert "Test Article 3" in titles

def test_magazine_contributing_authors(setup_db):
    magazine = Magazine.find_by_name("Test Magazine")
    article4 = Article(title="Test Article 4", author_id=Author.find_by_name("Test Author 1").id, magazine_id=magazine.id)
    article4.save()
    
    contributing_authors = magazine.contributing_authors()
    assert len(contributing_authors) == 1
    assert contributing_authors[0].name == "Test Author 1"
    
    article4.delete()

def test_magazines_with_multiple_authors(setup_db):
    magazine2 = Magazine(name="Single Author Magazine", category="Testing")
    magazine2.save()
    article4 = Article(title="Single Author Article", author_id=Author.find_by_name("Test Author 1").id, magazine_id=magazine2.id)
    article4.save()
    
    multi_author_mags = Magazine.magazines_with_multiple_authors()
    assert len(multi_author_mags) == 1
    assert multi_author_mags[0].name == "Test Magazine"

    article4.delete()
    magazine2.delete()