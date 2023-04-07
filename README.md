## Description
A repo for the X Gov Hackathon that took place over Wednesday 29th March - 31st Friday.

### What Problem does this try to solve?


## Setup
A repo for the X Gov Hackathon that took place over Wednesday 29th March - 31st Friday.

### For flask
```
pip install poetry
poetry shell
poetry install
flask --app flask_app/app run
curl -X POST http://127.0.0.1:5000/score -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com\"}"

curl -X POST https://flask-service.enes6h8hrh0rm.eu-west-2.cs.amazonlightsail.com/score -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com\"}"
curl -X POST https://flask-service.enes6h8hrh0rm.eu-west-2.cs.amazonlightsail.com/score -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com\"}"

curl -X POST https://gone-phishin-w7qq.onrender.com/score -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com\"}"

CORS:
curl -X OPTIONS 'https://localhost:5000' -H "Origin: https://gone-phishin-zmahmood98.vercel.app/" -H "Access-Control-Request-Method: GET" -v -o /dev/null
```

### For AWS hosting of text service
```
scp -i "C:\Users\User\Downloads\Text_Service.pem" "C:\Users\User\OneDrive\Documents\Hackathon\gone-phishin-xgov-hackathon" ec2-user@ec2-52-90-75-117.compute-1.amazonaws.com:/home/ec2-user/Text_Service

scp -i "C:\Users\User\Downloads\Text_Service.pem" "C:\Users\User\OneDrive\Documents\Hackathon\gone-phishin-xgov-hackathon/main.py" ec2-user@ec2-3-86-89-252.compute-1.amazonaws.com:/home/ec2-user/Text_Service/gone-phishin-xgov-hackathon/main.py
```

```
pip install -r requirements.txt
```

## Running

To run the service, run either
* main.py in the terminal using `python main.py` (_this will run until you quit or interrupt the code using `ctrl + c`_)
* notify_sandbox.ipynb in jupyter lab

## Data

## Miscellaneous

## Others

