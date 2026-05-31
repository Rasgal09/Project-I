### What is this project?
This project is a simple, custom-built Django web application called Project-I. At its core, it is a personal Notes App where users can sign up, log in, write notes, and manage them on a dashboard.

The project was created to show how authentication, database interactions, and user roles work in Django. It also highlights security issues—for example, it contains deliberate flaws (like storing passwords in plaintext or using custom login checks instead of Django's built-in, secure ones) to show where web applications often go wrong and how to fix them.

### What does Project-I do and how does it work?
#### What is it for?
Setting up a database from scratch can be tedious. The `seed_db.py` script is a helper tool that sets up the database, wipes out any old information, and fills it with sample users and notes. This gives you a fully functional app to play around with immediately, without having to manually register new accounts.

#### How it works:
1. **Connects to Django:** Django usually runs on a web server, but this script needs to speak to the database directly from your command line. It starts by telling Python where the app settings are and initializes the Django system.
2. **Cleans the Database:** To make sure there is no overlapping or leftover data, it clears out any existing users, notes, and security logs.
3. **Creates Test Users and Notes:** It creates a handful of fake users and populates their accounts with sample notes (like grocery lists or homework reminders).
4. **Highlights a Security Flaw:** By default, it saves the seeded user passwords as plain text to demonstrate a security vulnerability (A02: Cryptographic Failures), but it also contains commented-out code showing how to securely hash them using Django's `make_password`.

#### How to run it:
Open your terminal at the project root directory and run:


```
python seed_db.py
```

And this is used every time you change between versions, if its in the version with error you will have to run the command after changing the code to the version without error, end viceversa 

### Testing Accounts (Log in to see how it works)
After seeding the database, start your Django server using `python manage.py runserver` and head over to your browser. You can log in using any of the accounts below to see how the app behaves under different user roles, check out their notes, and try out the admin features:

- **Administrator Account (Accesses the admin dashboard):**
    - **Username:** `admin1`
    - **Password:** `adminpass`
- **Regular User Accounts:**
    - **Username:** `user1` | **Password:** `user1pass`
    - **Username:** `user2` | **Password:** `user2pass`
    - **Username:** `user3` | **Password:** `user3pass`
    - **Username:** `user4` | **Password:** `user4pass`
