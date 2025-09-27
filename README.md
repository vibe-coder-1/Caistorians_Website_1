Next steps at the bottom of this:

Go into cmd, run: cd "(your file path to base folder)"
py -m venv .venv
(that will need to use your machine's name for python, py, python py -3.10, python3 - it's different on every pc it seems.)
.\.venv\Scripts\activate
(activates the virtual environment)
py (or python etc) manage.py runserver
Follow the localhost link

Just have a look around. 
Backend: open to suggestions, whatever you feel needs to be added or changed. One thing off the top of my head is adding notifications in more places (see notifications.utils)
Frontend: i don't even know, just make it look pretty. Main/styles/Main/style.css. Affects the whole site, so add classes to stuff. 

This is part of a larger project than just the caistorians. This can be scaled up to schools across the country. It is possible to create a custom homepage for each school, youll have to understand django to do that though. 




Next steps:
-Chat rooms for members of a school year group (visibility?)
-Paywall
-Oauth
-Email marketing?
-Display contact info on profile toggle
-Email and/or whatsapp campaigns, for meetups etc? Use twilio api to automatically set up WA communities for people? 
-Donation Page
