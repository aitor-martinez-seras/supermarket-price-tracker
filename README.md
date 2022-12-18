# Supermarket-price-follower

## Requirements

- pandas
- numpy
- request-html

## Troubleshooting
request-html have problems in raspberry pi, as it installs a chromium x64 version by deafault.
To solve this issue, install via apt-get the chromium-browser (``` sudo apt-get chrome-browser```).
Some errors may arise, but is not too complicated to solve.

Then, go to ```/home/pi/.local/share/pyppeteer/local-chromium/588429/chrome-linux/```, where the 
chrome in searched by the pyppeteer library (used by request-html). Create a symbol link inside that folder
of chrome pointing to the installed chromium-browser, probably under ``/usr/bin/chromium-browser``: 
``ln -sv /usr/bin/chromium-browser chrome ``