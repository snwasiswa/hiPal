from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


# Create your views here.
@login_required
def chat(request, pk):
    """Chat room for the lesson"""
    try:
        # Retrieve lesson using its id
        lesson = request.user.lessons_joined.get(id=pk)
    except:
        # raise an exception if user is not authenticated
        raise PermissionDenied("You need to be enrolled in to get access.")
    return render(request, 'message/chat.html', {'lesson': lesson})
