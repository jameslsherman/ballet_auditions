# importing the libraries
from bs4 import BeautifulSoup
# import re
import requests
from datetime import date, timedelta
import os.path
from os import path

#-------------------------------------------------------------------------------
def send_email(school, email_from, email_to):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg['Subject'] = school
    msg['From'] = email_from
    msg['To'] = email_to

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

#-------------------------------------------------------------------------------
def sab():
    email_from = "from@example.com"
    email_to = "to@example.com"
    school = "sab"
    url = "https://www.sab.org/summer_programs/us_auditions/national_audition_tour.php"

    # Make a GET request to fetch the raw HTML content
    response = requests.get(url)

    # Parse the html content
    soup = BeautifulSoup(response.text, "lxml")
    # print(soup.prettify()) # print the parsed data of html

    filename1 = school + "_" + date.today().strftime("%Y%m%d") + ".html"
    with open(filename1, "w") as file:
        file.write(str(soup))
    file.close()

    yesterday = date.today() - timedelta(days=1)
    filename2 = school + "_" + yesterday.strftime("%Y%m%d") + ".html"

    is_diff = False
    if path.exists(filename2):
        with open(filename1) as f1:
           with open(filename2) as f2:
              if f1.read() != f2.read():
                  print("diff")
                  is_diff = True

    if (is_diff):
        send_email(school, email_from, email_to)

sab()
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
