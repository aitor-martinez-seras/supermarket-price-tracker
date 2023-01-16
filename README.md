# Supermarket-price-tracker

![Tests](https://github.com/aitor-martinez-seras/supermarket-price-tracker/actions/workflows/tests.yml/badge.svg)

## Requirements

- pandas
- numpy
- request-html

## Troubleshooting

### request-html
request-html have problems in raspberry pi, as it installs a chromium x64 version by deafault.
To solve this issue, install via apt-get the chromium-browser (``` sudo apt-get chrome-browser```).
Some errors may arise, but is not too complicated to solve.

Then, go to ```/home/pi/.local/share/pyppeteer/local-chromium/588429/chrome-linux/```, where the 
chrome in searched by the pyppeteer library (used by request-html). Create a symbol link inside that folder
of chrome pointing to the installed chromium-browser, probably under ``/usr/bin/chromium-browser``: 
``ln -sv /usr/bin/chromium-browser chrome ``.

After this, it still shows a warning error but does not seem to have impact on the actual output, is just a 
warning.

### Selenium on RPi

1. Install selenium in the virtual environment by ```pip install selenium```
2. Download chrome-browser using ``` sudo apt-get chrome-browser```. Then, you have 2 options:

    A. Use the driver downloaded with the step 2, that is located in ```/usr/lib/chromium-browser/chromedriver```

    B. Search for the chromium driver version corresponding to the installed chrome-browser version
in https://launchpad.net/ubuntu/bionic/arm64/chromium-chromedriver , download the .deb file with wget and install it
using ```dpkg -i name_of_the_downloaded_file_of_chromium_driver.deb``` . The driver will be located in 
````/usr/bin/chromedriver````

Now, when calling selenium from the scripts, this must be included:

````python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


service = Service(executable_path="/path/to/chromiumdriver")
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=service, options=options)
````
where the ````/path/to/chromiumdriver```` is ```/usr/lib/chromium-browser/chromedriver``` if used option A, and
````/usr/bin/chromedriver```` if used option B. Of course, more options can be included to the Options object, 
like headless or enable-javascript.