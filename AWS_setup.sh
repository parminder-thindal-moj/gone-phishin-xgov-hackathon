#!/bin/bash

python3 -m ensurepip --upgrade
pip3 install -r requirements.txt
sudo cp ./Continuous_Text_Service.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable Continuous_Text_Service.service
sudo systemctl start Continuous_Text_Service.service  
sudo systemctl status Continuous_Text_Service.service 