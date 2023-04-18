## Description
A repo for the X Gov Hackathon that took place over Wednesday 29th March - 31st Friday.  There are 3 main products:
- A Flask API wrapped around an XGBoost model which when given a link will return a probability it is phishing (hosted on AWS Lighsail)
- A Python script which interfaces with Gov Notify API which when a link is sent to a phone number will reply with whether or not it is spam (hosted on AWS EC2)
- A React website (https://github.com/zmahmood98/gone_phishin) which has a UI for users to enter their own link and score it

See our [presentation](https://docs.google.com/presentation/d/1NXpR3yQgyVBeTWgSFr2RmfoAdWdlrzNxJHmsF0s-YSI/edit?usp=share_link) for a summary of our results.

Note, the website interacts with the Flask API but the Python Script contains a copy of the scoring code within it.

Also note, you will need to specify a constant ```GOV_API_KEY``` which can be found in our gov data science slack channel.

## Flask API

### To run the flask app locally:
```
pip install poetry
poetry shell
poetry install
flask --app flask_app/app run

# To test locally:
curl -X POST http://127.0.0.1:5000/score -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com\"}"
```

### To deploy the flask app on AWS Lighsail:
To deploy the app follow this [guidance](https://aws.amazon.com/getting-started/hands-on/serve-a-flask-app/).  The basic steps are:
1. Build the docker image
2. Create a container service on AWS
3. Push your image onto the container service

Note, the following may need tweaking on your machine
```
cd flask_app
docker build -t flask-container .
aws lightsail create-container-service --service-name flask-service --power small --scale 1
aws lightsail push-container-image --service-name flask-service --label flask-container --image flask-container
aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json

# To test on the server:
curl -X POST https://flask-service.enes6h8hrh0rm.eu-west-2.cs.amazonlightsail.com/score -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com\"}"
```

## Text Service

### To run the text service locally:
```
cd gone-phishin-xgov-hackathon
pip install poetry
poetry install
python main.py
```
(_this will run until you quit or interrupt the code using `ctrl + c`_)

### For AWS hosting of text service
These are the steps for hosting the text service on EC2.  First read [this](https://towardsdatascience.com/how-to-run-your-python-scripts-in-amazon-ec2-instances-demo-8e56e76a6d24) if your unfamiliar with hosting Python scripts on EC2.
1. Create a t2.medium AL EC2 instance with an 8gb attached volume
2. Git clone this repo in the session manager terminal and run it's AWS_setup.bash

The AWS_setup.bash will:
1. Install all dependencies
2. Copy a the service file to services folder
3. Start the ```Continuous_Text_Service``` which will keep main.py running even when you close the terminal

To test the service send a text to the appropriate gov.uk number (check the presentation).

## Website
The website is located on github [here](https://github.com/zmahmood98/gone_phishin).  You can access it at [https://gone-phishin.vercel.app/](https://gone-phishin.vercel.app/).