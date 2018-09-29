
# GrandPy Bot
GrandPy Bot is a web application which localizes the address of a place you are looking for and tells you an irrelevent information about the neighborhood of the address.

## Supported language
- French

This application only supports French at the moment, Queries in other language may return unexpected results.

## Prerequisits
- python 3.x
- Google Maps and Places API key

## Getting Started
1. **Install Python 3.x**

	If you don't have python yet, [download](https://www.python.org/downloads/) and install.

2. **Clone this repository.**

	If you have git installed, use following command
	```
	git clone https://github.com/hjung06/GrandPy-bot.git
	```

3. **Create a virtual environment.**

	Find out more about python [virtual environment](https://docs.python.org/3/tutorial/venv.html)

4. **Install required python modules for this app.**
	```
	pip install -r requirements.txt
	```

5. **Set your Google maps API key as an environment variable.**

	Linux/Mac OS:
	```
	export MAPS_API_KEY=*your api key*
	```
	Windows:
	```
	set MAPS_API_KEY=*your api key*
	```
	**Or you could set it directly in *grandPy/views.py* file.**

	Change the variable *key* from:
	```
	key = os.environ.get('MAPS_API_KEY')
	```
	To:
	```
	key = *'Your API Key'
	```
6. **run *run.py* in terminal.**
	```
	python run.py
	```

## Built with
- Python 3.6.5
- Flask 1.0.2
- Requests 2.19.1
- Google Maps API
- Google Places API
- Mediawiki API
- JavaScript ES6
- jQuery 3.3.1
- Bootstrap 4.1.3
- Font Awesome 5.3.1

## Deployment
You can try this application on [https://oc-grandpy-bot.herokuapp.com](https://oc-grandpy-bot.herokuapp.com/)

Click [here](https://devcenter.heroku.com/articles/getting-started-with-python) to find out more about deploying python application on Heroku.

## License
Grandpy Bot is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)
