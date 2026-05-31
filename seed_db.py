import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'security_demo.settings')
django.setup()

from notes_app.models import CustomUser, Note, SecurityLog
from django.contrib.auth.hashers import make_password

def seed():
    print("Flushing database...")
    CustomUser.objects.all().delete()
    Note.objects.all().delete()
    SecurityLog.objects.all().delete()

    print("Seeding users...")
    # -------------------------------------------------------------------------
    # FLAW 2: A02 - Cryptographic Failures (Seed Passwords)
    # Context: The sandbox database is seeded with plaintext passwords. 
    # In the remediated version, passwords must be securely hashed.
    # -------------------------------------------------------------------------
    users_data = [
        {"username": "admin1", "password": "adminpass", "is_admin": True},
        {"username": "user1", "password": "user1pass", "is_admin": False},
        {"username": "user2", "password": "user2pass", "is_admin": False},
        {"username": "user3", "password": "user3pass", "is_admin": False},
        {"username": "user4", "password": "user4pass", "is_admin": False},
    ]

    users = []
    for u in users_data:
        # [INCORRECT CODE - ACTIVE]
        # Passwords stored in plaintext
        user = CustomUser.objects.create(
            username=u["username"],
            password=u["password"],
            is_admin=u["is_admin"]
        )
        # [CORRECT CODE - COMMENTED]
        # # Passwords stored with secure hashing
        """ user = CustomUser.objects.create(
           username=u["username"],
           password=make_password(u["password"]),  # Securely hashes seeded user passwords (A02)
           is_admin=u["is_admin"]
        ) """
        # -------------------------------------------------------------------------
        users.append(user)
        print(f"Created user: {user.username} (Admin: {user.is_admin})")

    print("Seeding sample notes...")
    notes_data = [
        {"username": "admin1", "content": "Grocery shopping list:\n- Milk and eggs\n- Whole wheat bread\n- Apples"},
        {"username": "admin1", "content": "Places to visit in Helsinki:\n- Helsinki Cathedral\n- Suomenlinna Fortress\n- Market Square"},
        {"username": "user1", "content": "Remember to do math homework for Tuesday afternoon."},
        {"username": "user2", "content": "Gift ideas for mom's birthday (flowers, scarf, or a book)."},
        {"username": "user3", "content": "To-do list:\n- Wash the car\n- Mow the lawn\n- Pay the water bill"},
        {"username": "user4", "content": "Workout routine:\n- Run 5km in the morning\n- 30 push-ups"},
    ]

    for n in notes_data:
        user = CustomUser.objects.get(username=n["username"])
        note = Note.objects.create(user=user, content=n["content"])
        print(f"Created note for user: {user.username}")

    print("\nDatabase seeded successfully!")
    print("Available test accounts:")
    print(" - admin1 / adminpass (Administrator)")
    print(" - user1 / user1pass (Regular User)")
    print(" - user2 / user2pass (Regular User)")
    print(" - user3 / user3pass (Regular User)")
    print(" - user4 / user4pass (Regular User)")

if __name__ == "__main__":
    seed()
