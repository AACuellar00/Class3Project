# Air Quality Forecast

This is a web application that saves a users location and shows the current air quality for said location according to the nearest monitoring station. The
user can also designate an air quality threshold should they so choose so as to know whether the air quality is above or below that also. Along with that it
also records an average air quality value for the location that is periodically updated so long as a user is linked to that location. A three day forecast 
for air quality is also included. Optionally a user can opt in to recieve a daily morning email about their area's air quality and whether or not it is above or below
their threshold.Note that this email will only be sent if the station near them has actually updated since the last email. As air quality monitoring stations
are not installed in all locations and they are not always up, the locations shown to a user may not actually be as close as one would like. 

User Story

As somebody who lives in California and with the ever increasing amount of wildfires across the globe, I thought it would be nice to have something that
could readily tell me the air quality near me, and even with an daily email too.

The live version is available at 

https://aq-forecast-31d76c74a953.herokuapp.com/ 

Note that it requires an account with a valid email to see anything however. After creating the account just click settings and either press the button
to geolocate yourself based on your ip or enter a set of coordinates to save your location. Optionally one can also change their air quality threshold from 
the default of 50 and can also check the box for whether or not you want to recieve daily emails.

Web application is done through python and flask and of course html/css/javascript. Html is in src/templates. API is accessed mainly in src/collect_data.py.

Data is retrieved through methodss in src/collect_data.py. The data is retrieved periodically through src/collector_script/collector_s.py, and is 
also retrieved whenever the user opens the home webpage or updates their settings. All data is saved in a postgresql database provided by heroku postgres.
When the script is launched it will collect data hourly. On the live website it is done through Cron go To Scheduler on Heroku. 


Data is analyzed through src/analyze_data.py with the same web page timings as user, and is also done through src/analyzer_script/analyzer_s.py 
 and is two fold. One analysis is whether the air quality is below or above a user's threshold and the other is averaging the air quality data for a given 
location. When the script is launched it will analyze the data for emailing purposes hourly. On the live website it is done through Cron To Go Scheduler on Heroku. 

Unit testing and Integration tests are in src/tests as unit_test.py and integration_test.py respectively. 

Continuous Integration is done with .github/workflows/deploy.yml to test all changes pushed to the main branch. 
Continuous delivery/deployment is done with Heroku's own automatic deployment. 

Data Persistence/Storage
All data is stored in a postgresql database provided by Heroku Postgres

Dependencies
Tested using python 3.10.5. 
Create the virtual environment first with: 

python -m venv venv

Start with the virtual environment with:

source venv/bin/activate

Install the requirements with: 

pip install -r requirements.txt

Test by installing dependencies and running ENV=local pytest. 

Running the app:

flask --app src/app run

flask --app src/collectorscript/collectorscript run -p 5001

flask --app src/analyzerscript/analyzerscript  run -p 5002



All AQ information is provided by the World Air Quality Index Project and all their EPA sources. Their site can be found at https://aqicn.org .
Images were designed by HadoNguyen from pngtree.com . https://pngtree.com/freepng/boy-air-quality_6845091.html .

