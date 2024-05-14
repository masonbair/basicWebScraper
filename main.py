import time
from bs4 import BeautifulSoup
import requests

print("Put some skills, separated by commas, that you are not familiar with")
unfamiliar_skills = input('>')
print(f"Filtering out: {unfamiliar_skills}")
unfamiliar_skills = unfamiliar_skills.replace(',', '').split()
currentPage = 1

f = open('posts/jobs.txt', 'w')

def loop_pages(page):
    web = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=python&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&pDate=I&sequence={page}&startPage={page}#'
    page += 1
    html_text = requests.get(web).text
    soup = BeautifulSoup(html_text, 'lxml')
    error = soup.find('span', class_='error-msg dflt-msg')
    while error is None:
        find_jobs(soup)
        loop_pages(page)


#Pulls webpage that we give it
def find_jobs(soup):
    # Find vs find_all: find only takes the first instance, find_all takes all the instances
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for job in jobs:
        number_of_skills = 0
        ## This is the first line in the for loop becuase we need to check if a job was posted a specific time ago
        date = job.find('span', class_='sim-posted').span.text
        if 'few' in date:
            requirements = job.find('span', class_='srp-skills').text.replace(' ', '')
            for unfamiliar_skill in unfamiliar_skills:
                if unfamiliar_skill not in requirements:
                    number_of_skills += 1
            if number_of_skills == len(unfamiliar_skills):
                company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
                more_info = job.header.h2.a['href']
                f.write(f"Company Name: {company_name.strip()}\n")
                f.write(f"Required Skills: {requirements.strip()}\n")
                f.write(f"More Info: {more_info}\n\n")
                print('File data saved')


if __name__ == '__main__':
    loop_pages(currentPage)