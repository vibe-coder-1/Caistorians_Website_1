try:
    from django.shortcuts import render, redirect, get_object_or_404
    from django.db.models import Q
    from .models import School
    from .forms import SchoolForm, HistoricalImageFormSet, AlumniHighlightFormSet, EditSchoolForm
    from Accounts.models import User  # Only for alumni directory
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

# --- Create School ---
def create_school_view(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        historical_formset = HistoricalImageFormSet(request.POST, request.FILES, queryset=School.objects.none())
        alumni_formset = AlumniHighlightFormSet(request.POST, request.FILES, queryset=School.objects.none())

        if form.is_valid() and historical_formset.is_valid() and alumni_formset.is_valid():
            school = form.save()
            # Save historical images
            for hform in historical_formset:
                if hform.cleaned_data and not hform.cleaned_data.get('DELETE', False):
                    hist = hform.save(commit=False)
                    hist.school = school
                    hist.save()
            # Save alumni highlights
            for aform in alumni_formset:
                if aform.cleaned_data and not aform.cleaned_data.get('DELETE', False):
                    alum = aform.save(commit=False)
                    alum.school = school
                    alum.save()
            return redirect('Main:homepage')
    else:
        form = SchoolForm()
        historical_formset = HistoricalImageFormSet(queryset=School.objects.none())
        alumni_formset = AlumniHighlightFormSet(queryset=School.objects.none())

    return render(request, 'schools/create_school.html', {
        'form': form,
        'historical_formset': historical_formset,
        'alumni_formset': alumni_formset,
    })


# --- School List (with search by name) ---
def school_list_view(request):
    query = request.GET.get("q", "")
    schools = School.objects.all().order_by("name")
    if query:
        schools = schools.filter(name__icontains=query)

    return render(request, "schools/school_list.html", {"schools": schools})


# --- School Profile / Detail ---
def school_profile_view(request, school_name):
    school = get_object_or_404(School, name=school_name)
    return render(request, 'schools/school_profile.html', {'school': school})


# --- Edit School ---
def edit_school_view(request, school_id):
    school = get_object_or_404(School, id=school_id)

    if request.method == "POST":
        form = EditSchoolForm(request.POST, request.FILES, instance=school)
        historical_formset = HistoricalImageFormSet(request.POST, request.FILES, instance=school)
        alumni_formset = AlumniHighlightFormSet(request.POST, request.FILES, instance=school)

        if form.is_valid() and historical_formset.is_valid() and alumni_formset.is_valid():
            form.save()
            historical_formset.save()
            alumni_formset.save()
            return redirect('Main:homepage')
    else:
        form = EditSchoolForm(instance=school)
        historical_formset = HistoricalImageFormSet(instance=school)
        alumni_formset = AlumniHighlightFormSet(instance=school)

    context = {
        'form': form,
        'historical_formset': historical_formset,
        'alumni_formset': alumni_formset,
        'school': school
    }
    return render(request, 'schools/edit_school.html', context)
