from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, g, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import func

from model import (User, Strain, Dispensary, Bud_Journal, Journal_Entry,
                   Trip_Report, User_Search, Anon_Search, db,
                   update_search_db, connect_to_db, make_autocomplete)

from helpers import *

app = Flask(__name__)
app.secret_key = 'supertopsecret'
app.jinja_env.undefined = StrictUndefined

#------------------------------------------------------------------------------#

# @app.before_request
# def add_test():
#     g.jasmine_tests=JS_TESTING_MODE

@app.route("/")
def index():
    """Search Homepage."""
    auto_strains = make_autocomplete()
    return render_template("homepage.html", auto_strains=auto_strains)


@app.route("/map.json")
def disp_info():
    """Get user input strain, check if in db.
       If strain is in db, call Leafly web scraper for strain availability page,
       Extract lat, long, address from each dispensary returned.
       Compiles strain information for strain page modals."""

    usr_input = request.args.get("strain")
    if not usr_input:
        usr_input = request.args.get("id")


    strain = Strain.query.filter(func.lower(Strain.s_name)==func.lower(usr_input)).first()
    if not strain:
        try:
            strain = Strain.query.get(usr_input)
        except:
            return ""

    print "I am checking if {} is in the database.".format(usr_input)

    update_search_db(strain, session.get('current_user'))
    url = strain.leafly_url
    print strain, url, 'found in db!'

    dispensaries = get_locations(url)
    description = get_strain_info(url)
    results = { 'dispensaries': dispensaries,
                'count': len(dispensaries),
                'strain': usr_input,
                'pos': strain.pos_effects,
                'type': strain.s_type,
                'name': strain.s_name,
                'desc': description,
                'url': url
                }
    return jsonify(results)


@app.route('/login', methods=['POST'])
def login():
    """Log In User, allow access to bud journal"""

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()

    if user:
        if password == user.password:
            session['current_user'] = user.user_id
            flash('Successfully logged in as {}'.format(email))
            return redirect("/")
        else:
            flash("Begone imposter!!")
    else:
        flash("User not found")
    return redirect("/")


@app.route("/logout")
def logout():
    """Log Out user."""

    del session['current_user']
    flash('Successfully logged out')

    return redirect("/")


@app.route('/register')
def registration_page():
    """Display registration landing page"""
    return render_template("registration.html")


@app.route('/registration', methods=['POST'])
def create_new_user():
    """Register new user"""
    # import pdb; pdb.set_trace()
    fname, lname, zipcode, user_type, age, preferred_type, email, password = [
        request.form[item]
        for item in [
        'fname', 'lname', 'zipcode', 'user_type', 'age',
        'preferred_type', 'email', 'password' ]
        ]

    if db.session.query(User.email).filter_by(email=email).first():
        flash("You've already signed up!")
    else:
        db.session.add(User(preferred_type=preferred_type,
                            age=int(age),
                            zipcode=int(zipcode),
                            user_type=user_type,
                            lname=lname,
                            fname=fname,
                            password=password,
                            email=email))
        db.session.commit()
        flash("Successfully registered!")

    return redirect("/")


@app.route("/journal")
def show_journal():
    """Shows Bud Journal Home."""
    logged_in = session.get('current_user')
    if logged_in:
        current_user = User.query.get(logged_in)
        return render_template('journal_home.html', user=current_user.fname)
    else:
        flash("Please log in to access journal")
        return redirect("/")

# functions:
# Add journal entry
# View entries

@app.route("/journal/new", methods=["POST"])
def new_journal():
    """Create New Bud Journal."""
    journal_label = request.form.get('journal_label')
    user_id = session['current_user']

    db.session.add(Bud_Journal(user_id=user_id,
                               journal_label=journal_label))
    db.session.commit()
    return redirect("/journal")

@app.route("/strains.json")
def strain_info():
    """Returns json file of strain information"""
    strains = Strain.query.order_by(func.random()).limit(5).all()
    s = {'strains' : 'strains'}

@app.route('/strains')
def display_goodies():
    """Display registration landing page"""
    h = Strain.query.filter_by(s_type='Hybrid').all()
    i = Strain.query.filter_by(s_type='Indica').all()
    s = Strain.query.filter_by(s_type='Sativa').all()
    return render_template("strains.html", hybrids=h, indicas=i, sativas=s)


# @app.route('/strains.json')
# def get_strain_info():
#     """Creates JSON file of strain info to display for modal on click."""
#     print "I am preparing this strain's information from the db!"
#     s_id = request.args.get('id')
#     results = { 'name': strain.s_name,
#                 'pos': strain.pos_effects }
#     print results
#     return jsonify(results)

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')