# Home/pipeline.py

def set_user_as_not_staff(strategy, details, user=None, is_new=False, *args, **kwargs):
    """Ensure new social-auth users are not staff or superusers."""
    if user and is_new:
        user.is_staff = False
        user.is_superuser = False
        # Set name from Google details if available
        if details.get('first_name') and not user.first_name:
            user.first_name = details.get('first_name', '')
        if details.get('last_name') and not user.last_name:
            user.last_name = details.get('last_name', '')
        user.save()
