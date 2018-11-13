from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests, smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

# Look at contacts.txt and get names, emails
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

names, emails = get_contacts('contacts.txt')
message_template = read_template('body.txt')

# To 
to_file = open('contacts.txt','r')
to_text = to_file.read().strip()
to_file.close()
to = to_text

first_url = 'https://www.nasdaq.com/symbol/fb'
second_url = 'https://www.nasdaq.com/symbol/klac'

# FB
# Open connection and grab pages
fb_stock = uReq(first_url)
fb_page = fb_stock.read()
fb_stock.close()

page_soup = soup(fb_page, "html.parser")

# Closing price
fb_prices = page_soup.find("div",{"id":"qwidget_lastsale"})
facebook_price = fb_prices.get_text()

# Dollar change
fb_dollars = page_soup.find("div",{"id":"qwidget_netchange"})
facebook_dollars = fb_dollars.get_text()

# Percent change
fb_percent = page_soup.find("div",{"id":"qwidget_percent"})
facebook_percent = fb_percent.get_text()

#Gain/Loss
fb_p_m = page_soup.find("div", {"id":"qwidget-arrow"})
f_arrow = fb_p_m.div['class']
color_ = f_arrow[1]
f_gain = 'green' in color_
if f_gain:
    print('GAIN')
    f_ar = '+'
else:
    print('LOSS')
    f_ar = '-'

# ------------------------------------------------------------------ #
# ------------------------------------------------------------------ #

# KLAC
# Open connection and grab pages
klac_stock = uReq(second_url)
klac_page = klac_stock.read()
klac_stock.close()

k_soup = soup(klac_page, "html.parser")

# Last sale price
klac_prices = k_soup.find("div",{"id":"qwidget_lastsale"})
tencor_price = klac_prices.get_text()

# Dollar change
klac_dollars = k_soup.find("div",{"id":"qwidget_netchange"})
tencor_dollars = klac_dollars.get_text()

# Percent change
klac_percent = k_soup.find("div",{"id":"qwidget_percent"})
tencor_percent = klac_percent.get_text()

#Gain/Loss
klac_p_m = k_soup.find("div", {"id":"qwidget-arrow"})
k_arrow = klac_p_m.div['class']
k_color = k_arrow[1]
k_gain = 'green' in k_color
if k_gain:
    print('GAIN')
    k_ar = '+'
else:
    print('LOSS')
    k_ar = '-'


# ------------------- E-Mail --------------------------------
from_address = "XXXXXXX@XXXXXXXX.com"

# For each contact, send the email:
for name, email in zip(names, emails):
    conn = smtplib.SMTP('smtp.gmail.com', 587) # SMTP address and port
    conn.ehlo() # Start connection
    conn.starttls()
    conn.login(from_address, 'XXXXXXXXXXXXXXXX')
    msg = MIMEMultipart()
    # add in the actual person name to the message template
    message = message_template.substitute(CONTACT_NAME=name.title(),FB_LP=facebook_price,
    F_P_M=f_ar,FB_D=facebook_dollars,FB_PERC=facebook_percent,T_LP=tencor_price,
    K_P_M=k_ar,T_D=tencor_dollars,T_PERC=tencor_percent)
        
    msg['From'] = from_address
    msg['To'] = email
    msg['Subject'] = "Stock Market Closing Results"

    msg.attach(MIMEText(message, 'plain'))
    conn.sendmail(from_address, email, msg.as_string())
    print('Sent notification emails to the following recipient:\n')
    print(email)
conn.quit()
