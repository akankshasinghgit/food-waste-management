# 🍽️ Local Food Wastage Management System

A platform connecting food providers (restaurants, supermarkets, catering services) with receivers (NGOs, individuals, shelters) to reduce food wastage.

**🔗 Live App:** [food-wastage-akanksha.streamlit.app](https://food-wastage-akanksha.streamlit.app)

## Tech Stack

`Python` · `MySQL (Aiven Cloud)` · `Streamlit` · `Plotly` · `Pandas` · `SQLAlchemy`

## Features

- **Home** — live dashboard with key metrics and quick insights
- **SQL Queries** — 15 analytical queries with search, CSV export, and chart previews
- **Filters** — live search and filter food listings by city, food type, and meal type
- **CRUD Operations** — add, update, and delete food listings and claims
- **EDA Charts** — interactive bar/pie charts and an expiry date range explorer

## Dataset

Four linked tables, ~1,000 records each: `providers`, `receivers`, `food_listings`, `claims`.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add your database credentials in `.streamlit/secrets.toml`:

```toml
[database]
host = "your-host"
port = 3306
user = "your-user"
password = "your-password"
name = "your-database"
```