import bs4
from selenium import webdriver
import getopt
import sys
import time
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

def printLogo():
    print("""
  ________        __  .__                  
 /  _____/_____ _/  |_|  |__   ___________ 
/   \  ___\__  \\\    _\  |  \_/ __ \_  __ \\
\    \_\  \/ __ \|  | |   |  \  ___/|  | \/
 \______  (____  /__| |___|  /\___  >__|   
        \/     \/          \/     \/       
        by Ben Heald
        https://healdb.tech
        https://github.com/Healdb/Gather
        https://twitter.com/heald_ben
        """)
    print("URL Screenshot Utility\n")
def checkURL(potentialUrl, driver, disallowed):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
   }
   driver.get(potentialUrl)
   html = driver.page_source
   soup = bs4.BeautifulSoup(html,features="lxml")
   #Catch chrome error pages
   chromeErrorDivs = soup.findAll("div", {"class": "error-code"})
   if( any(ele in html for ele in disallowed) or len(chromeErrorDivs) >0):
       return False
   return len(html)>10
def assembleHTML(name):
    urls = open(name+"/"+name+".txt", "r").readlines()
    outHTML = open(name+"/"+name+".html","w")
    outHTML.write("<html><center>")
    outText = ""
    i=0
    for url in urls:
        outText = outText+"<h3><a href='"+url+"' target='_blank'>"+url+"</a></h3><img src='"+os.getcwd()+"/"+name+"/screenshots/"+str(i)+"_screenshot.png'><br>\n"
        i+=1
    outHTML.write(outText)
    outHTML.write("</center></html>")
    outHTML.close()
def gatherScreenshots(driver, urlFile, name, disallowed, ports):
    i=0
    total = len(urlFile)
    try:
       os.mkdir(name)
    except FileExistsError:
       pass
    try:
       os.mkdir(name+"/screenshots/")
    except FileExistsError:
       pass
    outputFile = open(name+"/"+name+".txt", "w")
    for url in urlFile:
        url= url.strip()
        try:
           for port in ports:
               if port == "80":
                   if checkURL("http://"+url.strip(),driver, disallowed):
                       print("http://"+url)
                       driver.save_screenshot(os.getcwd()+ "/"+ name+"/screenshots/"+str(i)+"_screenshot.png")
                       outputFile.write('http://'+url.strip()+"\n")
                       i+=1
               elif port == "443":
                   if checkURL("https://"+url.strip(),driver, disallowed):
                       print("https://"+url)
                       driver.save_screenshot(os.getcwd()+ "/"+name+"/screenshots/"+str(i)+"_screenshot.png")
                       outputFile.write('https://'+url.strip()+"\n")
                       i+=1
               else:
                    if checkURL("http://"+url.strip()+":"+port,driver, disallowed):
                       print("http://"+url+":"+port)
                       driver.save_screenshot(os.getcwd()+ "/"+name+"/screenshots/"+str(i)+"_screenshot.png")
                       outputFile.write('https://'+url.strip()+":"+port+"\n")
                       i+=1
        except Exception as e:
            print(e)
            pass
    outputFile.close()
    driver.close()
def gather(argv):
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities['acceptInsecureCerts'] = True
    fileName = ""
    outDirName = ""
    chromeDriver = ""
    verbose = False
    disallowed = []
    ports = ["80","443"]
    
    try:
        (opts, args) = getopt.getopt(argv, 'h:f:c:d:p:')
    except getopt.GetoptError:
        print('gather.py -f <url_file> -c <Chrome Driver Path> -d <Disallowed Words> -p <Ports to scan>')
        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            print('gather.py -f <url_file> -c <Chrome Driver Path> -d <Disallowed Words> -p <Ports to scan>')
            sys.exit()
        elif opt in '-f':
            fileName = arg
            outDirName = (os.path.split(fileName)[1]).split(".")[0]
        elif opt in '-c':
            chromeDriver = arg
        elif opt in '-d':
            if arg != "":
                for word in arg.split(","):
                    disallowed.append(word)
        elif opt in '-p':
            if arg == "":
                arg = "80,443"
            for port in arg.split(","):
                ports = []
                ports.append(port)
        elif opt in '-v':
            verbose = True
    try:
        urlFile = open(fileName,"r").readlines()
    except:
        raise Exception("No file provided in the -f flag")
    options = Options()
    #options.headless = True
    driver = webdriver.Chrome(executable_path=chromeDriver,options=options,desired_capabilities=desired_capabilities, service_args=["--headless","--allow-running-insecure-content","--test-type","--ignore-certificate-errors","--ignore-ssl-errors=true", "--ssl-protocol=any"])
    driver.set_page_load_timeout(8)
    
    gatherScreenshots(driver,urlFile, outDirName, disallowed, ports)
    assembleHTML(outDirName)
if __name__ == '__main__':
    printLogo()
    gather(sys.argv[1:])

