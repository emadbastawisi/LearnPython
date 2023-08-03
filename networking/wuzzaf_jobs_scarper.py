import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# add user agent to avoid 403 error *optional*
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
# url has to have a page number at the end to be able to loop through all the pages

url = input('Enter wuzzaf search url like this: https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=python&start=0 \n your url : ')


# read the html from the url
req = urllib.request.Request(url, headers)
html = urllib.request.urlopen(url, context=ctx).read()
# parse the html
soup = BeautifulSoup(html, 'lxml')
# find the number of pages
pages = soup.find('li', class_='css-8neukt').text
# extract the number of pages using regex , the number of jobs in a page is 15
pagesNumber = int(re.findall('\d+', pages)[-1])/15
# find all the jobs in a page
jobs = soup.find_all('div', class_='css-1gatmva e1v1l3u10')
# a number to count the jobs while outputting to a txt file
job_number = 1

# loop through all the pages
for i in range(0, int(pagesNumber)+1):
    # loop through all the jobs in a page
    for job in jobs:
        # find the job title, company, location, skills, posted date, and link
        job_title = job.find('h2', class_='css-m604qf').text
        job_company = job.find('a', class_='css-17s97q8').text
        job_location = job.find('span', class_='css-5wys0k').text
        job_skills = job.find('div', class_='css-y4udm8').text
        # some jobs have a different class name for the posted date
        try:
            job_posted = job.find('div', class_='css-4c4ojb').text
        except:
            job_posted = job.find('div', class_='css-do6t5g').text
        job_link = job.find('a', class_='css-o171kl')['href']    
        # write the job info to a txt file
        with open('wuzzaf_jobs.txt', 'a',encoding="utf-8") as f:
            f.write(f"{job_number}-{job_title}\n{job_company}\n{job_location}\n{job_skills}\n{job_posted}\nhttps://wuzzuf.net{job_link}\n\n")
        # increment the job number
        job_number += 1
        # go to the next page by changing the page number at the end of the url
        url = url[:-1] + str(i)
        # read the html from the next page
        html = urllib.request.urlopen(url, context=ctx).read()
        # parse the html
        soup = BeautifulSoup(html, 'lxml')
        # find all the jobs in the page
        jobs = soup.find_all('div', class_='css-1gatmva e1v1l3u10')




    
