from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, g, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import func

from model import (User, Strain, Dispensary, Bud_Journal, Journal_Entry,
                   Trip_Report, User_Search, Anon_Search, db,
                   update_search_db, connect_to_db, make_autocomplete)

from datetime import datetime

from helpers import *

app = Flask(__name__)
app.secret_key = 'supertopsecret'
app.jinja_env.undefined = StrictUndefined

#-----------------------------------------------------------------------------#

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

    # user will either input strain name or select by ID
    usr_input = request.args.get("strain")
    if not usr_input:
        usr_input = request.args.get("id")

    # helper function
    strain = check_strain(usr_input)

    print strain

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
        auto_strains = make_autocomplete()
        journals = Bud_Journal.query.filter_by(user_id=logged_in).all()
        stories = Trip_Report.query.order_by(func.random()).limit(5).all()
        strains = Strain.query.order_by(func.random()).limit(3).all()
        strains2 = Strain.query.order_by(func.random()).limit(3).all()
        return render_template('journal_home.html', user=current_user.fname,
                                                    journals=journals,
                                                    stories=stories,
                                                    auto_strains=auto_strains,
                                                    strains=strains,
                                                    strains2=strains2)
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
    print 'I am creating a new journal'

    new_journal = Bud_Journal(user_id=user_id,
                               journal_label=journal_label)
    db.session.add(new_journal)
    db.session.commit()

    return redirect('/journal')


@app.route("/journal/remove", methods=["POST"])
def remove_journal():
    """Remove journal from database"""
    journal_id = request.form.get('journal')
    journal = Bud_Journal.query.get(journal_id)
    entries = Journal_Entry.query.filter_by(journal_id=journal.journal_id).all()
    for entry in entries:
        print "I am removing all entries."
        db.session.delete(entry)
    print "I'm removing this journal."
    db.session.delete(journal)
    db.session.commit()

    return "I deleted {}!".format(journal.journal_label)


@app.route("/journal/update", methods=["POST"])
def new_entry():
    """Modify Existing Bud Journal."""
    print "I'm inside the route"
    user_id = session['current_user']
    journal_id = request.form.get('journal')
    usr_input = request.form.get('strain')
    rating = request.form.get('user_rating')
    notes = request.form.get('notes')
    dosage = request.form.get('dosage')
    story_input = request.form.get('story')
    # Need to hardcode story_id if no submission by user
    story_id = None

    # find strain in the database
    strain = Strain.query.filter_by(s_name=usr_input).first()

    # if user has a story, add it to database first
    if story_input:
        print "I am adding a new story."
        new_story = Trip_Report(user_id=user_id,
                              strain_id=strain.strain_id,
                              dosage=dosage,
                              story=story_input,
                              timestamp=datetime.now())

        db.session.add(new_story)
        db.session.commit()
        print "I added a new story"
        story_id = new_story.story_id

    # Add new entry to journal
    print "I am adding an entry"
    entry = Journal_Entry(journal_id=journal_id,
                            user_id=user_id,
                            strain_id=strain.strain_id,
                            user_rating=rating,
                            notes=notes,
                            story_id=story_id,
                            )

    db.session.add(entry)
    db.session.commit()
    print "I added an entry"

    return "I updated {}!".format(entry)


@app.route("/journal/remove_strain.json", methods=["POST"])
def remove_strain():
    """Remove strain from journal & database"""
    log_id = request.form.get('entry')
    entry = Journal_Entry.query.get(log_id)
    db.session.delete(entry)
    print "I am removing this journal entry."
    db.session.flush()
    # import pdb; pdb.set_trace()
    print "I deleted entry {} from {}!".format(entry, entry.journal.journal_label)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/strains')
def display_goodies():
    """Display registration landing page"""
    h = Strain.query.filter_by(s_type='Hybrid').order_by(Strain.s_name).all()
    i = Strain.query.filter_by(s_type='Indica').order_by(Strain.s_name).all()
    s = Strain.query.filter_by(s_type='Sativa').order_by(Strain.s_name).all()
    return render_template("strains.html", hybrids=h, indicas=i, sativas=s)


@app.route('/check_strain')
def strain_in_db():
    """checks if strain is in database"""
    user_input = request.args.get('strain')
    if check_strain(user_input) != "":
        return "success"
    else:
        return check_strain(user_input)

#-----------------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')