# BudBud

**BudBud: A Buddy for your Bud!**    

*"Bud Search"* allows users to query cannabis dispensaries by strains on the menu, and renders an interactive map with navigation directions. The BudBud database contains 144 strains & 60 dispensaries in the San Francisco bay area, populated through web scraping (Leafly.com).  

Registered users can document, analyze, and visualize their cannabis experiences with the dynamic *"Bud Journal"*, powered by React.js, jQuery, PyChart, and D3.  

*"Party Bud"*, the enlightened bud bot, utilizes a regression algorithm to recommend users new strains based on *Bud Journal* data.  
BudBud is constructed in Python and prettified with JavaScript and Bootstrap. Maps are rendered by Google.

## Built With
* Languages: Python, SQL (PostGRES), JavaScript, HTML, CSS
* Frameworks: Flask, Jinja, React.js
* Technologies: [Postman](https://www.getpostman.com/)
* Libraries:
  * [jQuery](https://jquery.com/)
  * [SQLAlchemy](https://www.sqlalchemy.org/)
  * [React.js](https://reactjs.org/)
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
    $ createdb testdb
    $ npm install --save react-router-dom
    $ python seed.py
    $ python model.py

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
    │   ├── js
    │   │    ├── map.js
    │   │    └── strains.js
    │   └── css
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

* Fix formatting of pos_effects, neg_effects to remove brackets & quotes
* Create Bud Journal
  * Allow user to input:
    * dosage (input integer)
    * date taken (Calendar selector)
    * rating (drop-down or radio selector)
    * comments (string input)
  * Visualize data
  * Create algorithm to give predictive recommended strains based on journal data

## Author
* [Shirley Xiaolin Xu](https://www.linkedin.com/in/shxxu/)
* [@shxxu0212](https://github.com/Shxxu0212) — Full-stack software engineer, former business development consultant


BudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBudBud
