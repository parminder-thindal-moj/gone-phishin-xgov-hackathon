## Description
A repo for the X Gov Hackathon that took place over Wednesday 29th March - 31st Friday 2023.

### What Problem does this try to solve?
Aim - To prevent and reduce the number of fraud incidents, and increase awareness of phising.

Problem - Fraud costs approx £27 billion annually, with phishing accounting for around 83% of this. Anti-phising services are hard to access, or closed to a particular app/software.

Our Solution - An SMS service/Website that detects spam links and provides a near instant result of the link sent.

## Setup

### For flask
#### Not currently required to get the SMS service running. Will be required once the website is deployed.
```
pip install poetry
poetry shell
poetry install
flask --app flask_app/app run
curl -X POST http://127.0.0.1:5000/score -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}' 
````

```
pip install -r requirements.txt
```

In order to call the GOV.UK Notify API - you will also need to add a `constants.py` file to the root of the repo. Ask a team member for this file. This file should not be shared freely, and should not be uploaded to GitHub. The `.gitignore` should automatically take of this. If you are not sure ask one of the team.


## Running

To run the service:
* main.py in the terminal using `python main.py` in the root of the repo (_this will run until you quit or interrupt the code using `ctrl + c`_)

## Data

For this proof of concept, data has been sourced from [Phishtank](https://phishtank.org/) and  [GregaVrbancic](https://github.com/GregaVrbancic/Phishing-Dataset)

## Miscellaneous

THIS IS JUST A PROOF OF CONCEPT.

## Others

