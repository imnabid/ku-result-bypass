
To get started:
pip install -r requirements.txt


go to KU result page http://101.251.6.66/index.php
Hit Ctrl+Shift+I and got to Application
from cookies copy the PHPSESSID and paste into the COOKIE_CODE variable in main.py
enter the captcha code from the webpage to the CAPTCHA variable

place the registration number and other requirements
enter the start and end birthdate range and simply run main.py
if successful you will see a result.pdf in the working directory on an average time of 6 sec

You dont have to edit the COOKIE_CODE AND CAPTCHA for your next query until the session expires in like 30min 
and in that case you have follow the intitial steps

DISCLAIMER: This project is done solely for educational purpose.
