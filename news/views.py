try:
    from django.shortcuts import render, redirect
    from .forms import Births_Deaths_and_MarriagesForm
    from .models import Births_Deaths_and_Marriages
    from schools.models import School
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")
# Create your views here.
def updates(request):
    updates = Births_Deaths_and_Marriages.objects.filter(school=request.user.school).order_by('-created_at')
    context = {'updates': updates}
    return render(request, 'news/updates.html', context)

def births_deaths_and_marriages(request):
    form = Births_Deaths_and_MarriagesForm()
    if request.method == 'POST':
        form = Births_Deaths_and_MarriagesForm(request.POST, request.FILES)
        form.school = request.user.school
        if form.is_valid():
            update = form.save(commit=False)
            update.school = request.user.school
            update.save()
            return redirect('news:updates') 
    context = {'form': form}
    return render(request, 'news/create_update.html', context)