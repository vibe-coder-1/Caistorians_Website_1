from django.contrib.auth import get_user_model
User = get_user_model()

# Replace 'yourusername' with your actual username
user = User.objects.get(username='yashva')

# Check the email
print(user.email)
