
# GrandPy Bot
This application finds the address of a place and returns brief history about the street name of the place. Just like my grandpa who use to tell a random stroies about anything.

It's simple web application which uses stopwords to parse natural language and make couple APIs call to retreive approprate information.

## Supported language
- English

## Requirements
- python 3.x
- Flask
- Google Maps and Places API key

## Getting started

1. This application uses Google APIs. **Set following environment variables before running.**
	```
	# For front-end API
	MAPS_API_KEY=your_api_key

	# For back-end API
	PLACE_API_KEY=your_api_key
	```

2.  run *run.py*
	```
	python3 run.py
	```

## Deployment
 https://oc-grandpy-bot.herokuapp.com/

## License
The MIT License (MIT)
