# BudBud

**BudBud: A Buddy for your Bud!**    

"Bud Search" allows users to locate cannabis dispensaries nearby that offer a desired strain, and renders an interactive map with navigation directions. The BudBud database (PostGreSQL) contains 144 strains & 60 dispensaries in San Francisco and Oakland, populated through web scraping (Leafly.com.) Registered users can personalize their cannabis experiences with private journals, as well as share public adventure stories in "Bud Journal" (powered by jQuery, SQLAlchemy.) "Party Bud" the enlightened bud bot algorithmically recommends new strains to users, based on journal entries and search history. BudBud is constructed in Python and prettified with Bootstrap. Maps are rendered by Google API.

![alt text](./static/img/screenshots/main.jpg)
![alt text](./static/img/screenshots/journal.jpg)
![alt text](./static/img/screenshots/main-results.jpg)

## Built With
* Languages: Python, SQL (PostGRES), JavaScript, HTML, CSS
* Frameworks: Flask, Jinja
* Technologies: [Postman](https://www.getpostman.com/)
* Libraries:
  * [jQuery](https://jquery.com/)
  * [SQLAlchemy](https://www.sqlalchemy.org/)
  * [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
  * [Bootstrap](https://getbootstrap.com/)
* APIs:
  * Google Maps
* Websites Scraped:
  * Leafly.com

## Getting Started

    $ git clone https://github.com/shxxu0212/BudBud.git
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ createdb budbud
    $ python seed.py
    $ python server.py

## File structure

    .
    ├── model.py                 # Flask-SQLAlchemy classes for the data model
    ├── requirements.txt         # Defines requirements
    ├── server.py                # Flask routes
    ├── tests.py                 # Integration tests (uses testdb)
    ├── seed.py                  # Populate & manipulate database
    ├── dispensaries_helper.py   # Helper functions
    ├── todo.txt                 # To-Do list for 2.0 & 3.0 features
    │
    ├── static
    │   ├── img
    │   ├── js
    │   │    ├── journal.js
    │   │    ├── map.js
    │   │    └── strains.js
    │   └── css
    │        ├── journal.css
    │        ├── strain-modal.css
    │        ├── strain-tabs.css
    │        └── style.css
    │
    ├── seed_data
    │   ├── dispensaries.json
    │   ├── hybrids.json
    │   ├── indicas.json
    │   └── sativas.json
    │
    └── templates
        ├── base.html            # Template
        ├── homepage.html        # Homepage
        ├── journal_home.html    # Bud Journal Main
        ├── map.html             # Renders map of dispensaries
        ├── registration.html    # Register new user
        └─- strains.html         # Generates random strains

## To-do:
  * Visualize data
  * Create algorithm to give predictive recommended strains based on journal data

## Author
* [Shirley Xiaolin Xu](https://www.linkedin.com/in/shxxu/)
* Artwork: [Priyanka Java](http://priyankajava.com)


BudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBud
