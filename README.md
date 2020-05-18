# Third milestone project — "Doc docs - clinic appointment scheduler"

This project website is an appointment scheduling application designed for use in general practitioner's clinic.  The primary purpose of the
application is to allow the clinic administrators to schedule appointments for the various doctors who work in the clinic, and to allow 
the doctors to view their appointments.  

To schedule an appointment, the app user must first choose a doctor


The site comprises 3 web pages and can be viewed in desktop, tablet and mobile devices.


## UX

The purpose of this site is to enable a clinic administrator to schedule or remove an appointment for the selected doctor, and to allow the doctor
to view those same appointments.

At the beginning of the project I listed the features that were a must for the site, and features that were nice to have. The core features
I wanted were
 1. Option to add and remove appointments for a particular doctor
 2. Option to easily switch the selected doctor
 3. A datepicker to select the date for which appointments are made and displayed.
The availability of POST rating option was the main factor in my decision to use The Movie Database API, as it was the only API i could find that had this service available.

I had also considered

After selecting the API I wrote some basic proof of concept code to verify the API was giving me what i wanted, and that there were no major issues with it. I then
went about designing the basic layout of the site, and writing the wire frames. The use of a carousel on the home page was a suggestion from my project mentor during our
first project meeting. I'd considered a carousel on the search-results screen also, but decided against it for the following reasons:
 1. If there are many results returned its easier to find what you're looking for in a list as opposed to a carousel.
 2. I wanted there to be a clear distinction in layout on each screen, partly for variety, and also so that a user knows exactly where they are on the site.
Note that the search-results page in the wire frames shows a scroll able list of movies.  I changed this to a grid of cards after a suggestion from my project mentor during our second meeting.

Note also that there is a minor issue with the movies returned by the GET Upcoming API call.  Many of the movies in this response have release dates that are in the past, which of course isn't what
you'd expect for a Coming Soon movie.  I had considered filtering these movies out of the carousel, but I discussed it my mentor, and we agreed that i should leave it as is, as in some cases the filtered
list could result very small list, or possibly no 'Coming Soon movies' at all.

Wire frames can be found in root directory of the project repository.


## Features

### Existing Features — All screens
- **Home icon** - This is a font awesome icon displayed on the left of the header that links to the homepage when clicked
- **Search bar** - An input box with placeholder text prompting users to Search Movies
- **The Footer** - the footer section contains Follow Us text and social media links.

### Existing Features — Home screen
- **In Theaters carousel** - A Slick js carousel that displays movie posters and ratings returned from the Get Now Playing API call.
- **Coming Soon carousel** - A Slick js carousel that displays movie posters from the Get Upcoming API call.

### Existing Features — Search results screen
- **Search results** - A grid of cards displaying the movie poster, movie rating, title and release year that are returned from the Get Search Movies API call.

### Existing Features — Movie details screen
- **Movie info and poster** - Movie info and poster retrieved from the Get Details and Get Credits API calls.
- **Submit rating** - A component that allows users to submit a rating for the movie by selecting a number of stars and clicking the Submit button. The user must
 choose at least 1 star. The confirmation message will either confirm the rating submission or inform the user that they have already
 rated that particular movie.  The rating is submitted using the POST Rate Movie API call which takes the guest session id and rating value
 as parameters.


## Technologies Used

— [Bootstrap](https://getbootstrap.com/)
 — Bootstrap was used for the site layout and the datepicker sidebar.

— [JQuery](https://jquery.com)
 — Jquery is used throughout the project in conjunction with plain javascript for writing to the DOM and local
   storage.

— [Font Awesome](https://fontawesome.com/)
 — Font Awesome icons were used for the calendar toggle button, and for the modal form fields.

— [Flatpickr](https://flatpickr.js.org/)
 — The datepicker is from the free and open source Flatpickr library.

— [Select2](https://select2.org)
 — I used the Select2 libraries for the patient dropdown so as you can search the list by typing the
   name of the patient.


## Testing

The following tests were manually executed and passed in Chrome, Microsoft Edge, Firefox and on a Samsung mobile device.  The chrome dev tools device emulator
was used for responsive breakpoint testing.

**Entry page**
1. Go to the application root at http://doctor-docs.herokuapp.com/ and verify that the entry page is displayed.
2. Verify that the 'Select a doctor' heading is displayed at the top of the page.
3. Verify that two doctor profile cards are displayed, each with an image and doctor name.
4. Hover each card and verify that the pointer cursor is displayed, and the box-shadow increases slightly.
5. Gradually reduce the screenwidth down to 320px and verify that the cards are displayed in a vertical list.
6. Verify that there is adequate margin below each card element.
7. Increase the screensize back to desktop width, and verify that the cards are again displayed in a row.
8. Click on one of the doctor cards and verify that you are directed to the calendar page.
9. Check the doctor avatar and name that are displayed at the top left of the screen, and confirm that they match the doctor you selected
   on the entry page.
10. Check the doctor dropdown list at the right of the screen and verify that currently selected name matches the doctor you chose on the entry page.


**Calendar page - desktop view - change doctor**
1. Go to the application root at http://doctor-docs.herokuapp.com/ and verify that the entry page is displayed.
2. Select a doctor and verify that the calendar page is displayed for the selected doctor.
3. Select a different doctor using the dropdown list at the top right of the screen.
4. Verify that the page reloads and that doctor avatar and name now match that which you selected in previous step. 
5. Check the doctor dropdown list at the right of the screen and verify that currently selected name matches the doctor you just selected.

**Calendar page - desktop view - change date**
1. Go to the calendar page and check the currently selected date in the datepicker (highlighted in blue) matches the date displayed above the
   appointments table, which should be in the format DD-MM-YYYY.
2. Select a different date and verify that the page reloads and the date above appointments table matches the newly selected date.
3. Select a different doctor using the dropdown at the top right of the page. Verify that the page reloads, and that the date is still
   that which was selected in the previous step.
 
**Calendar page - desktop view - add appointment**
1. Go to the calendar page and click on any of the empty slots in the appointments table.
2. Verify that a modal is display listing the doctor name, the currently selected date, the start time of the slot you clicked, an end time that is
 15 minutes later than the start time, and a patient name is displayed.
3. Verify that the end time and patient fields are highlighted in a light grey color, and an arrow is displayed in each field indicating it is
   a dropdown list.
4. Click on the end time field and verify that a list of available times is displayed. Select any time from the list and verify it is displayed
    in the field.    
5. Click on the patient field and start typing the name of the patient you are looking for. Verify that the name you type is displayed in the
   field.
6. Click the Add Appointment button and verify that the modal closes, the page reloads, and the appointment has been added to the table.
7. Click on a slot that starts before the appointment you just created.
8. In the modal, click on the endtime field, and verify that the available end times list only contains times before the appointment you created
   in the previous steps.
9. Add the appointment and verify that it is displayed in the table.
10. Change the date and verify that the appointments table does not display the appointments you added in the previous steps.
11. Verify that you can add appointments for the same times slots as those you used in the previous steps without issue.
12. Change the date back and verify that the appointments you added earlier are still displayed.
13. Change the doctor and verify that the appointments you added in previous steps are not displayed for the newly selected doctor.
14. Change the doctor back and verify that the appointments you created are still displayed.

**Calendar page - desktop view - edit / delete appointment**
1. on any of the empty slots in the appointments table and add an appointment.
2. Click on the appointment you just added and verify that the Appointment details modal is displayed.
3. Verify that modal displays the correct doctor name, the currently selected date, the correct start and end time, and the correct patient name is displayed.
4. Click on the end time field and select a later time. Verify that the newly selected time is now displayed in the field.
5. Click on the patient field and select another patient. Verify that the newly selected patient is now displayed in the field.
6. Click the Update appointment button and verify that modal closes, the page reloads, and the updated appointment is now displayed in the
   appointment table.
7. ClickGo to the calendar page and click  on the updated appointment and verify that the modal displays the update end time and patient name.
8. Click the Delete appointment button and verify that the modal closes, the page reloads and the appointment is no longer displayed
   in the appointments table. 

**Calendar page - desktop view - responsive design**
1. Go to the calendar page and add one more appointments to the table.
2. Gradually reduce the screenwidth down to 320px and verify that the appointments table gradually narrow without any overlapping of other 
   elements or texts.
3. Verify that when the screenwidth reaches 798px and lower, that the datepicker is automatically hidden, and a calendar icon appears at the top
   left of the appointments table.
4. Click the calendar icon and verify that the datepicker is displayed, and that an overlay covers the rest of the page contents.
5. Verify that a Close button is now displayed at the bottom of the datepicker.
6. Click the close button and verify the datepicker and overlay are no longer displayed.
7. Open the datepicker again and select a different date. Verify the datepicker closes and the newly selected date is displayed at the top
   of the appointments table.
8. Open the datepicker again and click anywhere else on the screen. Verify the datepicker closes.
9. Open the datepicker again and refresh the screen. Verify the datepicker closes.  
10. Increase the screenwidth to > than 798px and verify that the datepicker opens automatically and that the calendar icon is now longer displayed.
      

## Deployment

This website was deployed an Heroku server with the following steps.  The version deployed on Heroku is the final version.
1. Go to https://www.heroku.com/ where you'll be presented with a page where you can log in or sign up.
2. Click sign up and complete the form and sign up for the free account
3. Complete the email verification and password steps
4. Login to Heroku and choose the option to create a new app.
5. Give the app a name, select a region and create.
6. If you dont already have Heroku installed locally, you can install using the steps here - https://devcenter.heroku.com/articles/heroku-cli#download-and-install
7. Once Heroku is installed, open your IDE terminal and run 'heroku login', and fill out the required fields.
8. Go back to the Heroku dashboard in your browser, and click on the Settings link for your app. From here
   you can get the Heroku git URL. e.g. https://git.heroku.com/doctor-docs.git
9. Go back to the IDE terminal and run 'git add remote heroku https://git.heroku.com/doctor-docs.git'.
10. Next, install Gunicorn which will be used to as part of the deployment. You can install with the
    following command 'pip3 install gunicorn' 
11. Next create a requirements.txt file with the following command 'pip3 freeze --local > requirements.txt'
12. Commit the requirements.txt file to your local git repository.
13. Add a Procfile with the following command 'echo web: gunicorn app:app > Procfile'
14. Push the application to Heroku with 'push -u origin master' 
15. Run the application with heroku ps:scale web=1
16. Check the application is running at http://doctor-docs.herokuapp.com/
16. If there are any issues with the deployment you can check files and logs with following commands:
    heroku run bash -a doctor-docs
    heroku logs -n 200
    heroku logs --tail   
   

If you want to run the site locally you need to download the site files from Github and host it on a Python server.
1. To download the site files, go to https://philiph80.github.io/third-milestone-project/, then click the Clone or Download button and select Download Zip.
2. Extract the downloaded zip and run the app.py file from your python server e.g. If you dont already have a Python server installed there are clear and easy
  steps to install a Python server here https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server

## Credits

### Content
— The doctor profile images were found through a google image search and are hosted locally.

### Acknowledgments

— The box shadow CSS used for the doctor cards on the entry page was taken from an example on the w3schools site. I liked
 the way it looked, and didn't see any reason to change it, so I left it as is. 
  https://www.w3schools.com/howto/howto_css_cards.asp
— The datepicker sidebar was implemented using steps from this site - https://bootstrapious.com/p/bootstrap-sidebar
- All other work is my own.