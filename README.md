### Hexlet tests and linter status:
[![Actions Status](https://github.com/Alexander-kkk/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Alexander-kkk/python-project-83/actions)


### SonarQube status:
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Alexander-kkk_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Alexander-kkk_python-project-83)


# Page Analyzer
Page Analyzer is a Flask web application that allows users to analyze web pages. The application checks website availability and extracts SEO elements like title, description, and H1 tags.

## Features
- ✅ URL validation and normalization
- ✅ SEO analysis (title, H1, description)
- ✅ HTTP status code checking
- ✅ History of checks for each URL
- ✅ Clean, responsive UI with Bootstrap

## Live Demo
**Try it here**: [https://python-project-83-h95e.onrender.com](https://python-project-83-h95e.onrender.com)

## Technologies
- **Backend**: Python 3.13, Flask
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS, Bootstrap, Jinja2
- **Tools**: uv (package manager), Ruff (linting), Pytest (testing)
- **Libraries**: BeautifulSoup4, Requests, Validators

## Quick Start

### 1. Clone and setup
```bash
git clone https://github.com/Alexander-kkk/python-project-83.git
cd python-project-83
cp .env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY
```

### 2. Install dependencies
```bash
make install
```

### 3. Setup database
```bash
createdb page_analyzer
psql page_analyzer < database.sql
```

### 4. Run the app
```bash
make dev      # Development server
make start    # Production server
```

### Project Commands
```bash
make install   # Install dependencies
make dev       # Run development server
make start     # Run production server
make lint      # Lint code with Ruff
make test      # Run tests
```



