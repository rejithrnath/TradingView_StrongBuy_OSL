# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 03:28:11 2021

@author: Rejith Reghunathan 
@email: rejithrnath@gmail.com
"""
import numpy as np
import datetime
import os, pandas
import shutil
import time
import email, smtplib, ssl
import schedule
import temp.config
import requests
from bs4 import BeautifulSoup

from os import system
system("title " + "TV Webscrapping")

if not os.path.exists('results'):
        os.makedirs('results')

save_path = 'results/'
filename_results = datetime.datetime.now().strftime("%Y%m%d")
completeName = os.path.join(save_path, filename_results+".txt")

    
def delete_results():
    shutil.rmtree('results')
    os.makedirs('results')
    save_path = 'results/'
    filename_results = datetime.datetime.now().strftime("%Y%m%d")
    completeName = os.path.join(save_path, filename_results+".txt") 



def webscrapping_tv():
    symbol_dir = []
    signal_dir = []
    des_dir = []
    quote ={}
    url = 'https://www.tradingview.com/markets/stocks-norway/market-movers-large-cap/'
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("a", {"class" : "tv-screener__symbol"})
    for t in tabl:
      temp_dir = t.get_text()
      symbol_dir.append(temp_dir)

    symbol_dir = [v for i, v in enumerate(symbol_dir) if i % 2 == 0]



    tabl2 = soup.find_all("span", {"class" : "tv-screener-table__signal"})
    for t in tabl2:
      temp_dir_2 = t.get_text()
      signal_dir.append(temp_dir_2)


    tabl3 = soup.find_all("span", {"class" : "tv-screener__description"})
    for t in tabl3:
      temp_dir_3 = t.get_text().strip(" ")
      des_dir .append(temp_dir_3)


    for x, y,z in zip(symbol_dir, signal_dir, des_dir):
      if (y =='Strong Buy'):
        f = open(completeName, "a")
        print (x +" -> "+ y +" -> " + z , file=f)
        print (x +" -> "+ y +" -> " + z)
        f.close()    

            
            
def email_export():
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    subject = "Trading View Webscrapping Results "+ str(datetime.datetime.now())
    body = "Email with attachment "
    
    sender_email = temp.config.sender_email
    receiver_email = temp.config.receiver_email
    password = temp.config.password

        
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = sender_email
    message["Subject"] = subject
    message["Bcc"] = ", ".join(receiver_email)  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    
    # Open PDF file in binary mode
    with open(completeName, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {completeName}",
    )
    
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        print("Emailed!")
        delete_results()
            

def download_and_email():
    
   
    f = open(completeName, "a")
    print ("Start Largest companies by market cap — Norwegian Stock Market -> %s \n" % time.ctime(), file=f) 
    print ("*******************************************************************" , file=f)
    f.close()
    webscrapping_tv()
    f = open(completeName, "a")
    print ("*******************************************************************" , file=f)
    f.close()
    print("End!")
    email_export()    
    
def main():
    
    print("Largest companies by market cap — Norwegian Stock Market!!")
    #download_and_email()
    trading_time = ["09","10","11","12","13","14","15","16"]
    for x in trading_time:
      
        schedule.every().monday.at(str(x)+":16").do(download_and_email)
        schedule.every().tuesday.at(str(x)+":16").do(download_and_email)
        schedule.every().wednesday.at(str(x)+":16").do(download_and_email)
        schedule.every().thursday.at(str(x)+":16").do(download_and_email)
        schedule.every().friday.at(str(x)+":16").do(download_and_email)
 
    while True:
        schedule.run_pending()
        time.sleep(1)    
    
if __name__ == "__main__":
    main()