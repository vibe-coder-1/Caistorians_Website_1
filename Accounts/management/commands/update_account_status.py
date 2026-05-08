try:
    from django.core.management.base import BaseCommand
    from datetime import datetime
    from Accounts.models import User
except ImportError as e:
    print(f"\nError: Django or Accounts app not available.\n{e}")

class Command(BaseCommand):
    help = "Update user account statuses (student vs alumni) based on graduation year"

    def handle(self, *args, **kwargs):
        current_year = datetime.now().year
        updated_students = 0
        updated_alumni = 0

        for user in User.objects.all():
            if user.graduation_year:
                was_student = user.is_student_account
                user.is_student_account = current_year < user.graduation_year
                user.save(update_fields=["is_student_account"])
                if was_student and not user.is_student_account:
                    updated_alumni += 1
                elif not was_student and user.is_student_account:
                    updated_students += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Updated account statuses: {updated_students} marked as students, {updated_alumni} marked as alumni."
            )
        )
