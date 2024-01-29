# Google-Cloud-Password-Sprayer
The Google Cloud Password Sprayer is an improvement upon my GCP V2 password sprayer where this one implements a few new items:

- Uses SeleniumBase's Undetected Chromedriver
- Allows the user to either select a random user agent, or the tool will do it for them
- Implements headless mode so that Chrome does not pop-up
- Implements Incognito mode
- Runs on all various operating systems

## Previous Sprayer Description

> GCP PW Spray is a rude and crude password spraying tool using Selenium Webdriver and Undetected_Chromedriver. Currently, only Chrome browser is supported, due to limitations with Google accounts browser security.
> GCP PW Spray is designed to run on Kali Linux. It will auto detect the file you give it with the -u flag with emails on new lines

## Setup

1. ```pip3 install -r requirements.txt```
2. Go!

## Usage
```python3 sprayer.py [--email <SINGULAR EMAIL>] [--file <FILE OF EMAILS>] --password 'Password' [--useragent <USER AGENT STRING>]```

## Further Tasks

[] Add Captcha Response
[] Implement Fireprox
[] Create GCP Enumeration
