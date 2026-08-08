from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def error_handling_home(request):
    return render(request, 'error_handling/error_page.html', {
        'error_code': 'HOME',
        'title': 'Error handling is ready',
        'message': 'This space is now set up for custom error pages and future handling improvements.',
    })


def error_page(request, error_code):
    code = str(error_code).upper()

    if code == '404':
        title = 'Page not found'
        message = 'The page you were looking for may have moved, been removed, or never existed.'
    elif code == '500':
        title = 'Server error'
        message = 'Something went wrong on our side. Please try again shortly or return to the homepage.'
    else:
        title = 'Unexpected error'
        message = 'A problem occurred while handling this request. Please try again or return home.'

    return render(request, 'error_handling/error_page.html', {
        'error_code': code,
        'title': title,
        'message': message,
    })


def custom_404_handler(request, exception=None):
    return HttpResponseRedirect(reverse('error_handling:error_page', kwargs={'error_code': '404'}))


def custom_500_handler(request):
    return HttpResponseRedirect(reverse('error_handling:error_page', kwargs={'error_code': '500'}))
