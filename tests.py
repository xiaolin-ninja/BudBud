from unittest import TestCase
from model import *
from server import app
from flask import session


class FlaskTestsBasic(TestCase):
    """Basic Flask Route tests."""

    def setUp(self):
        """Stuff to do before every test."""
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")

    def test_index(self):
        """Test homepage page."""
        result = self.client.get("/")
        self.assertIn("Welcome", result.data)
        self.assertEqual(result.status_code, 200)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at the end of every test."""
        db.session.close()
        db.drop_all()

    def test_find_strain(self):
        """Test homepage page."""
        strain = Strain.query.filter(Strain.s_name=='HB Kush').first()
        self.assertEqual(strain.s_name, "HB Kush")
        self.assertEqual(strain.s_type, "Hybrid")


    def test_find_dispensary(self):
        """Test homepage page."""
        frf = Dispensary.query.filter(Dispensary.name=='Forbidden Random Forest').first()
        self.assertEqual(frf.name, "Forbidden Random Forest")


    def test_register(self):
        """Test registration page"""
        result = self.client.get("/register")
        self.assertIn("Fill Out Your User Profile", result.data)


    def test_new_registration(self):
        """Test registering new user"""
        new_user = self.client.post("/registration",
                data={'preferred_type': 'Indica',
                      'age': 25,
                      'zipcode': 94118,
                      'user_type': 'Both',
                      'lname': 'builder',
                      'fname': 'bob',
                      'password': 'password',
                      'email': 'bob@bob.com' },
                follow_redirects=True )
        self.assertIn("Successfully registered", new_user.data)


    def test_existing_user(self):
        """Test repeat registration"""
        existing_user = self.client.post("/registration",
                        data={'preferred_type': 'Sativa',
                              'age': 26,
                              'zipcode': 94118,
                              'user_type': 'Both',
                              'lname': 'anything',
                              'fname': 'here',
                              'password': 'password',
                              'email': 'anna@anna.com' },
                        follow_redirects=True )
        self.assertIn("already signed up!", existing_user.data)


    def test_strains_display(self):
        """Test strains page."""
        result = self.client.get("/strains")
        self.assertIn("What tickles your fancy?", result.data)
        self.assertEqual(result.status_code, 200)


    def test_search_error(self):
        """Test strains page."""
        result = self.client.get("/map", data = {'strain':'potatoes'})
        self.assertEqual(result.status_code, 302)


# class MockFlaskTests(TestCase):
#     """Create mock requests to test adding to db"""

#     def setUp(self):
#         """Stuff to do before every test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         connect_to_db(app, "postgresql:///testdb")

#         db.create_all()
#         example_data()

#         def _mock_get_dispensaries(strain):
#             return

#     def

class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at the end of every test."""
        db.session.close()
        db.drop_all()


    def test_login(self):
        """Test log in form."""
        with self.client as c:
            result = c.post('/login',
                            data={'email': 'anna@anna.com',
                                  'password': 'password'},
                            follow_redirects=True
                            )
            self.assertIn("Successfully logged in as", result.data)
            # why is this working?
            self.assertEqual(session['current_user'], 1)
            self.assertNotIn("Log In!", result.data)


    def test_wrong_password(self):
        """Test login with wrong password."""

        result = self.client.post('/login',
                        data={'email': 'anna@anna.com',
                              'password': 'wrong'},
                        follow_redirects=True
                        )
        self.assertIn("Begone imposter!!", result.data)
        self.assertNotIn("Successfully logged in as", result.data)


    def test_wrong_user(self):
        """Test login with wrong user."""

        result = self.client.post('/login',
                        data={'email': 'notanna@anna.com',
                              'password': 'password'},
                        follow_redirects=True
                        )
        self.assertIn("User not found", result.data)
        self.assertNotIn("Successfully logged in as", result.data)


    def test_logout(self):
        """Test logout route."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 1

            result = c.get('/logout', follow_redirects=True)

            self.assertNotIn('current_user', session)
            self.assertIn("Successfully logged out", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client.session_transaction() as sess:
            sess['current_user'] = User.query.first().user_id


    def tearDown(self):
        """Do at the end of every test."""
        # db.drop_all()
        db.session.close()


    def test_journal(self):
        """Test that user can't see journal page when logged out."""
        with self.client as c:
            result = c.get("/journal", follow_redirects=True)
            self.assertIn("Bud Journal", result.data)


    def test_logged_in(self):
        """Test that home page reflects login status."""

        result = self.client.get("/")
        self.assertNotIn("Log In!", result.data)
        self.assertIn("Log out", result.data)
        self.assertIn("Bud Journal", result.data)


    # def test_user_search(self):
    #     """Test strains page."""
    #     with self.client as c:
    #         page = c.get("/map", data = {'strain':'hb Kush'})
    #         self.assertEqual(page.status_code, 302)
    #         with c.session_transaction() as sess:
    #             result = User_Search.query.get(sess['current_user'])
    #             print 'current user', sess['current_user']
    #             self.assertTrue(result)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        self.client = app.test_client()


    def test_journal(self):
        """Test that user can't see journal page when logged out."""
        result = self.client.get("/journal", follow_redirects=True)
        self.assertIn("Please log in to access journal", result.data)

    # ***def test_anon_db(self):
    #     """Test that search results enter anonymous searches database"""
    #     ??????????

    def test_logged_out(self):
        """Test homepage page."""
        result = self.client.get("/")
        self.assertIn("Log In!", result.data)
        self.assertNotIn("Log Out", result.data)


# ----------------------------------------------------------------------#
import unittest

if __name__ == "__main__":
    unittest.main()