# Gather
https://healdb.tech/blog/gather.html

Gather is a simple python script that uses the Selenium Python module to take screenshots of a provided list of URLs. Headless solutions such as [Aquatone](https://github.com/michenriksen/aquatone) provide the same service and are much faster, but in my experience may miss some live hosts. Gather is a non-headless method that simply requests the given domain at whatever ports specified, ensuring a very good false negative rate.

# Requirements:

Install requirements with the command `pip install -r requirements.txt`

You will also need to download a chromium driver from here - 
https://chromedriver.chromium.org/downloads

I have tested this only on Windows, but should work on Linux as well.

# Usage:

`gather.py -f <domain_file> -c <Chrome Driver Path> -d <Disallowed Words> -p <Ports to scan> -o <Output directory path>`

`-f`  File containing domain names to scan seperated by a newline character.

`-c`  Path to the chromium driver for selenium

`-d`  If any of the words are found in the HTML of the webpage, the page will be ignored and not included in the report. Useful if the domains commonly redirect to a particular page.

`-p`  Ports to scan, default is `80,443`.

`-o`  Output directory to write the report and screenshots to.

Sample use: 

`python gather.py -f "uber-domains.txt" -c "chromedriver.exe" -d uber.com,onelogin -p 80,443,8080 -o "C:\Documents\reports"`






