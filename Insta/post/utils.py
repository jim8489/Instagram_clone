from .models import Stream

def get_stream(user):
    # Include posts by the user and followed users
    return Stream.objects.filter(user=user).order_by('-date')
