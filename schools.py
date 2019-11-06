# importing the libraries
import csv
import io
import os
import requests

from bs4 import BeautifulSoup, Comment
from datetime import date, timedelta
from os import path

#-------------------------------------------------------------------------------
def remove_tags(soup):
    import re

    # remove tags
    [s.extract() for s in soup(['footer','head','iframe','img','input','link','meta','noscript','script','style','svg'])]

    # remove comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    # remove attributes
    for tag in soup():
        for attribute in ['class','href','id','name','style','target']:
            del tag[attribute]

    # remove whitespace
    output = re.sub(' +', ' ', str(soup))

    # remove multiple line breaks
    output = re.sub(r'\n\s*\n', '\n\n', output)

    return output

#-------------------------------------------------------------------------------
def open_files(school, output):

    # TODO: add timezone ?
    filename1 = school + "_" + date.today().strftime("%Y%m%d") + ".html"
    with io.open(filename1, "w", encoding="utf-8") as file:
        file.write(output)
    file.close()

    yesterday = date.today() - timedelta(days=1)
    filename2 = school + "_" + yesterday.strftime("%Y%m%d") + ".html"

    twodaysago = date.today() - timedelta(days=2)
    filename3 = school + "_" + twodaysago.strftime("%Y%m%d") + ".html"
    if path.exists(filename3):
        os.remove(filename3)

    return filename1, filename2

#-------------------------------------------------------------------------------
def send_email(school):
    import smtplib
    from email.message import EmailMessage

    email_from = "jameslsherman@yahoo.com"
    email_to = "jameslsherman@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = school
    msg['From'] = email_from
    msg['To'] = email_to

    # Send the message via our own SMTP server.
    # s = smtplib.SMTP('127.0.0.1')
    # s.send_message(msg)
    # s.quit()

#-------------------------------------------------------------------------------
def read_schools():
    with open('schools.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        # skip header
        # next(reader, None)
        for row in reader:
            school = row['school']
            url = row['url']

            print(school)
            # print(url)

            # Make a GET request to fetch the raw HTML content
            response = requests.get(url)

            if response.status_code == 200:
                # Parse the html content
                soup = BeautifulSoup(response.text, "lxml")
                # print(soup.prettify()) # print the parsed data of html

                output = remove_tags(soup)
                filename1, filename2 = open_files(school, output)

                is_diff = False
                if path.exists(filename2):
                    with io.open(filename1, encoding="utf-8") as f1:
                       with io.open(filename2, encoding="utf-8") as f2:
                          if f1.read() != f2.read():
                              print(school, " diff")
                              is_diff = True

                if (is_diff):
                    send_email(school)

            else:
                print(school, response.status_code)

read_schools()
# Pull all text from the div
# cities = soup.find_all(class_="interior list-title")
# #
# # # Create for loop to print out all artists' names
# for idx, city in enumerate(cities):
#     print(idx, city.text)
# #    print(idx, row.prettify())
#
# tables = soup.find_all('table')
# for idx, table in enumerate(tables):
#     print(cities[idx])
#     for trs in table.find_all('tr'):
#         for tds in trs.find_all('td'):
#             print(idx, tds)
#             break
#
# years = soup.find_all("strong",text=re.compile("2019"))
# for year in years:
#     print(year)
