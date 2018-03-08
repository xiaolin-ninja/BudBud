from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

db = SQLAlchemy()

##############################################################################

class User(db.Model):
    """User of BudBud website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname =  db.Column(db.String(64), nullable=False)
    lname =  db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.String(20), nullable=True)
    # 4 choices: Sativa, Indica, Hybrid, Nada
    preferred_type = db.Column(db.String(15), nullable=False)

## another table for favorites later.

    # def add_favorite(self, strain):
    #     # when clicked, add strain to favorites

    # def suggest_strain(self, ??):
    #     # using data from journal logs, recommend for this user top 5 most searched strains
    #     # filtered by preferred_type, sorted by location.

    def __repr__(self):
        """print info in useful form"""
        return "<User {} {}, id={}>".format(self.fname, self.lname,
                                            self.user_id, self.email)

# class Dispensaries(db.Model):
#     """Popular dispensaries"""
#     dispensary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name =  db.Column(db.String(64), unique=True, nullable=False)
#     location =  db.Column(db.String(64), nullable=False)

class Strain(db.Model):
    """Popular strains"""

    __tablename__ = "strains"

    strain_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name =  db.Column(db.String(64), unique=True, nullable=False)
    s_type =  db.Column(db.String(64), nullable=False)
    pos_effects = db.Column(db.String(64), nullable=False)
    neg_effects = db.Column(db.String(64), nullable=False)
    leafly_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """print info in useful form"""

        return "<Strain {} name={} type={}>".format(self.strain_id,
                self.s_name, self.s_type)


class Dispensary(db.Model):
    """Popular strains"""

    __tablename__ = "dispensaries"

    dispensary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name =  db.Column(db.String(64), nullable=False)
    disp_lat =  db.Column(db.Float, nullable=False)
    disp_lng = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        """print info in useful form"""
        return "<Dispensary name={}>".format(self.name)


class Bud_Journal(db.Model):
    """Journal Log History"""

    __tablename__ = "journals"

    journal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    journal_label =  db.Column(db.String(100), nullable=False)

    user = db.relationship("User", backref=db.backref("log",
                                                      order_by=Strain.strain_id))

    def __repr__(self):
        """print info in useful form"""
        return "<Journal id={} user_id={}>".format(
                                                self.journal_id, self.user_id)


class Journal_Entry(db.Model):
    """Journal Log History"""

    __tablename__ = "entries"

    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    journal_id = db.Column(db.Integer, db.ForeignKey("journals.journal_id"), nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    strain_id =  db.Column(db.Integer, db.ForeignKey("strains.strain_id"), nullable=False)
    user_rating =  db.Column(db.Integer, nullable=False)
    notes =  db.Column(db.Text, nullable=True)
    story_id = db.Column(db.Integer, db.ForeignKey("stories.story_id"), nullable=True)

    user = db.relationship("User", backref=db.backref("entires",
                                                      order_by=strain_id))
    journal = db.relationship("Bud_Journal", backref=db.backref("entries",
                                                      order_by=strain_id))
    # CHECK IF THIS WORKS LATER, HOW TO SORT BY 2?
    strain = db.relationship("Strain", backref=db.backref("entries"))
    story = db.relationship("Trip_Report", backref=db.backref("entries"))

    def __repr__(self):
        """print info in useful form"""
        return "<Entry id={}, strain={} in journal={} by user={}>".format(
                                                self.log_id,
                                                self.strain.s_name,
                                                self.journal.journal_label,
                                                self.user_id)


class Trip_Report(db.Model):
    """Journal Log History"""

    __tablename__ = "stories"

    story_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    strain_id =  db.Column(db.Integer, db.ForeignKey("strains.strain_id"), nullable=False)
    # ## USE A DATE PICKER for date-taken
    # use_date = db.Column(db.DateTime, nullable=True)
    dosage =  db.Column(db.Integer, nullable=True)
    ## auto-generated from page, time of addition of this post
    timestamp = db.Column(db.DateTime, nullable=True)
    story =  db.Column(db.Text, nullable=False)
    dankness = db.Column(db.Integer, default=random.randint(1,50),
       nullable=False)

    user = db.relationship("User", backref=db.backref("stories",
                                                      order_by=strain_id))
    strain = db.relationship("Strain", backref=db.backref("stories",
                                                        order_by=user_id))

    def __repr__(self):
        """print info in useful form"""
        return "<Journal Log id={} in journal={} by user={}>".format(
                                                self.log_id, self.journal_id, self.user_id, self.strain_id)


class User_Search(db.Model):
    """Record of user searches, for data collection & recommendation AI"""

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    strain_id =  db.Column(db.Integer, db.ForeignKey("strains.strain_id"), nullable=False)
    date_searched =  db.Column(db.DateTime, nullable=False)
    ## default to zipcode unless user agrees to location services & makes a search based on that
    # user_lat =  db.Column(db.Float, nullable=False)
    # user_lng = db.Column(db.Float, nullable=False)
    user = db.relationship("User", backref=db.backref("searches"))
    strain = db.relationship("Strain", backref="searches")

    def __repr__(self):
        """print info in useful form"""
        return "<Search Log id={} user_id={} strain_id={}>".format(self.id, self.user_id,
                                                            self.strain_id, self.location)


class Anon_Search(db.Model):
    """Record of anonymous searches, for data collection of popular strains by area"""

    __tablename__ = "anon_searches"

    anon_search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    strain_id =  db.Column(db.Integer, db.ForeignKey("strains.strain_id"), nullable=False)
    date_searched =  db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """print info in useful form"""
        return "<Anon Search Log id={} strain_id={}>".format(
                                                self.id, self.strain_id, self.location)

##############################################################################

def update_search_db(strain, logged_in):
    """Update search database"""
    if logged_in:
        print 'I am updating user searches!'
        user = User.query.get(logged_in)
        db.session.add(User_Search(
                        user_id=user.user_id,
                        strain_id=strain.strain_id,
                        date_searched=datetime.now(),
                        ))
        db.session.commit()
    else:
        print "I am updating anon seaches!"
        db.session.add(Anon_Search(
                        strain_id=strain.strain_id,
                        date_searched=datetime.now(),
                    ))
        db.session.commit()


def make_autocomplete():
    """make list of strains for autocomplete"""
    result = [s[0] for s in db.session.query(Strain.s_name).all()]
    return result


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data

    Trip_Report.query.delete()
    Journal_Entry.query.delete()
    Bud_Journal.query.delete()
    Dispensary.query.delete()
    Strain.query.delete()
    User.query.delete()

    # Add sample employees and departments
    anna = User(preferred_type='Sativa',
                        age=21,
                        zipcode=94118,
                        user_type='Medical',
                        lname='banana',
                        fname='anna',
                        password='password',
                        email='anna@anna.com')

    hb_kush = Strain(s_name='HB Kush',
                        s_type='Hybrid',
                        pos_effects='{happiness, euphoria, love}',
                        neg_effects='{dry eyes, headache, couchlock}',
                        leafly_url='hybrid/hb-kush')

    ballonicorn = Strain(s_name='Ballonicorn',
                        s_type='Indica',
                        pos_effects='{cuteness, pinkness, lightness}',
                        neg_effects='{emptiness, bloated}',
                        leafly_url='indica/balloonicorn')

    ubermelon = Strain(s_name='Ubermelon',
                        s_type='Sativa',
                        pos_effects='{happiness, euphoria, love}',
                        neg_effects='{Mel, melonmania}',
                        leafly_url='sativa/ubermelon')

    frf = Dispensary(name='Forbidden Random Forest',
                                disp_lat=37.7995971,
                                disp_lng=-122.327749,
                                address='1234 123 street, SF, CA')

    db.session.add_all([anna, hb_kush, ubermelon, frf, ballonicorn])
    db.session.commit()

    j = Bud_Journal(user_id=anna.user_id,
                          journal_label='Making Art')

    k = Bud_Journal(user_id=anna.user_id,
                          journal_label='Eating')

    db.session.add_all([j, k])
    db.session.commit()

    # creation should be mocked...?
    entry = Journal_Entry(user_id=anna.user_id,
                          journal_id=j.journal_id,
                          strain_id=ubermelon.strain_id,
                          user_rating=5,
                          # timestamp=??,
                          notes="Don't smoke too much, don't cross with alcohol.")

    story = Trip_Report(journal_id=k.journal_id,
                          user_id=anna.user_id,
                          strain_id=ballonicorn.strain_id,
                          dosage=15,
                          story="I was smoking Ubermelon with my friends while eating \
                                 a watermelon we ordered from Ubermelon and it was amazing! \
                                 My friend Balloonicorn had the best idea ever for painting \
                                 with the watermelon rinds and we made great art! haha",
                          dankness=0)

    db.session.add_all([story, entry])
    db.session.commit()


    entry2 = Journal_Entry(user_id=anna.user_id,
                      journal_id=k.journal_id,
                      strain_id=ballonicorn.strain_id,
                      user_rating=4,
                      story_id=story.story_id,
                      # timestamp=??,
                      notes="I feel like a balloon!")

    db.session.add(entry2)
    db.session.commit()

##############################################################################

def connect_to_db(app, db_uri="postgresql:///budbud"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


# if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

from server import app
connect_to_db(app)
print "Connected to DB."
