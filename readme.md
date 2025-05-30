# Articles Management System
A Python-based system for managing articles, authors, and magazines with a relational database backend.

![Project Architecture](docs/images/project-architecture.png) 

## Features

- **Author Management**: Create, read, update, and delete author profiles
- **Magazine Management**: Manage magazine details and categories
- **Article System**: Full CRUD operations for articles with tagging
- **Subscription System**: Track magazine subscribers
- **Search & Filter**: Find articles by author, magazine, or tags
- **Analytics**: Track article view counts and popularity

## Tech Stack

- **Python 3.10+**
- **SQLAlchemy ORM**
- **PostgreSQL** (SQLite supported for development)
- **Alembic** for database migrations
- **Pytest** for testing

## Project Structure
articles-project/
├── articles/ # Core application package
│ ├── models/ # Database models
│ ├── controllers/ # Business logic
│ ├── db/ # Database configuration
│ └── cli.py # Command-line interface
├── scripts/ # Database setup scripts
├── tests/ # Unit and integration tests
└── requirements.txt # Dependencies
## Getting Started
### Prerequisites
- Python 3.10+
- SQLite 
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/articles-project.git
   cd articles-project