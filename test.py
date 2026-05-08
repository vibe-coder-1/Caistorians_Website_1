try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Replace 'yourusername' with your actual username
    user = User.objects.get(username='yashva')

    # Check the email
    print(user.email)
except ImportError as e:
    print(f"""\n Error: Django is not installed. {e}
     Please install Django using: pip install django\n""")
except Exception as e:
    print(f"""\n Error: Could not retrieve user. {e}
     Make sure the user exists in the database.\n""")