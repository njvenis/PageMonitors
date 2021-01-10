import requests
import os
from bs4 import BeautifulSoup
import re
import smtplib
import time

#Created by Nicholas Venis 05/09/19

gmailUser = ""
gmailPass = ""


def pull():
    try:
        page = requests.get("https://uk.burberry.com//")
        data = page.content

        soup = BeautifulSoup(data, "html.parser")
        data = soup.find("script", text=re.compile("var pageData"))
        data = data.text

        id = re.findall(r"\"productID\": \"(.*?)\"",data)
        product = re.findall(r"\"productTitle\": \"(.*?)\"", data)

        if os.path.isfile("id.log" or "items.log"):
            i = open("id.log","r")
            p = open('items.log','r')


            inpID = i.readline()
            inpProduct = p.readline()

            liID = str.split(inpID,",")
            diffID = list(set(liID)^set(id))

            liProduct = str.split(inpProduct,",")
            diffProduct = list(set(liProduct)^set(product))

            if diffID == []:
                with open("id.log", "w") as out:
                    out.write(",".join(id))
                    out.close()
                with open("items.log", "w") as out:
                    out.write(",".join(product))
                    out.close()
                with open("log.log", "a") as out:
                    tm = time.asctime(time.localtime(time.time())) + ": "
                    string = tm + "Nothing new added.\n"
                    out.write(string)
                    out.close()
            else:
                link = []

                for idx, val in enumerate(diffID):
                    temp = diffProduct[idx].replace(" and ","")
                    temp = temp.replace(" ","-")
                    link.append("https://uk.burberry.com/"+temp+"-p"+val)
                    print(link)

                to = []
                subject = 'New products in sale!'
                text = "New items added to sale, see below \n\n"
                ids = "New product ID's: "+ ", ".join(diffID) + '\n'
                products = "New Products: " + ", ".join(diffProduct) + '\n'
                links = "Product links: " + ", ".join(link) + '\n'
                body = text + ids + products + links
                sentFrom = gmailUser

                emailtext = "Subject: {}\n\n{}".format(subject,body)



                try:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmailUser,gmailPass)
                    server.sendmail(sentFrom,to,emailtext)
                    server.close()

                except Exception as e:
                    print(e)

                with open("id.log", "w") as out:
                    out.write(",".join(id))
                    out.close()
                with open("items.log", "w") as out:
                    out.write(",".join(product))
                    out.close()

                with open("log.log", "a") as out:
                    tm = time.asctime(time.localtime(time.time())) + ": "
                    sum = len(diffID)
                    string = tm + str(sum) +" new products detected, email sent" "\n"
                    out.write(string)
                    out.close()

        else:
            with open("id.log", "w") as out:
                out.write(",".join(id))
                out.close()
            with open("items.log", "w") as out:
                out.write(",".join(product))
                out.close()
            with open("log.log","w") as out:
                tm = time.asctime( time.localtime(time.time())) + ": "
                string = tm + "Initial pull.\n"
                out.write(string)
                out.close()


    except requests.exceptions.RequestException as e:
        print("HTTP Error" + str(e))

pull()
