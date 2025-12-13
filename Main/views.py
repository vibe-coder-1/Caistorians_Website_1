from django.shortcuts import render, redirect
from community.models import Story

def homepage(request):
    if request.user.is_authenticated:
        if request.user.school:
            # Redirect or render the user's school homepage
            magazines = Story.objects.filter(school_id=request.user.school.id, is_magazine=True)
            return render(request, 'schools/school_home.html', {'school': request.user.school, 'magazines': magazines})
        else:
            # User is logged in but has no school assigned
            return render(request, 'Main/homepage.html', {'message': 'You are not assigned to a school yet.'})
    else:
        return render(request, 'Main/homepage.html')
def site_home(request):
    return render(request, 'Main/homepage.html')