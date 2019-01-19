import requests, smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def get_stocks(filename):
    stocks = []
    with open(filename, mode='r', encoding='utf-8') as stocks_file:
        for a_stock in stocks_file:
            stocks.append(a_stock.split()[0])
    return stocks

from_addr = '---- YOUR EMAIL THAT WILL SEND MESSAGE ----'
names, emails = get_contacts('contacts.txt')
stocks = get_stocks('stocks.txt')
text_file = 'textfile.txt'

with open(text_file, "w") as my_file:
        my_file.write('')

for stock in stocks:

    req = requests.get('https://www.nasdaq.com/symbol/' + str(stock))
    site = req.text
    html = BeautifulSoup(site, "html.parser")

    symbol = html.title.get_text().split()

    gl = html.find("div", {"id":"qwidget-arrow"})
    arrow = gl.div['class']
    color = arrow[1]
    gain = 'green' in color
    if gain:
        ar = '+'
    else:
        ar = '-'

    find_price = html.find("div",{"id":"qwidget_lastsale"})
    price = find_price.get_text()

    find_dollar_change = html.find("div",{"id":"qwidget_netchange"})
    dollars = find_dollar_change.get_text()

    find_perc = html.find("div",{"id":"qwidget_percent"})
    perc_change = find_perc.get_text()
    
    with open(text_file, "a") as my_file:
        my_file.write(str(symbol[0]) + ':\n')
        my_file.write(str(price) + '\n')
        my_file.write(str(ar) + '$' + str(dollars) + '\n')
        my_file.write(str(ar + perc_change) + '\n')
        my_file.write('\n')

txt_open = open(text_file, "r")
content = txt_open.read()

for name, email in zip(names, emails):
    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login(from_addr, '---- GMAIL ONE-TIME PASSWORD ----')
    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = email
    msg['Subject'] = 'Stock Market Closing Results'
    message = str(content)

    msg.attach(MIMEText(message, 'plain'))
    conn.sendmail(from_addr, email, msg.as_string())

    print('\nSent emails to: \n' + email)
conn.quit()

print('\nDone')
