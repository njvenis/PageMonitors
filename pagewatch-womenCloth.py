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
        page = requests.get("https://uk.burberry.com/qwnytfsdjlf/")
        data = page.content

        soup = BeautifulSoup(data, "html.parser")
        data = soup.find("script", text=re.compile("var pageData"))
        data = data.text

        id = re.findall(r"\"productID\": \"(.*?)\"",data)
        product = re.findall(r"\"productTitle\": \"(.*?)\"", data)

        if os.path.isfile("idWomen.log" or "itemsWomen.log"):
            i = open("idWomen.log","r")
            p = open('itemsWomen.log','r')


            inpID = i.readline()
            inpProduct = p.readline()

            liID = str.split(inpID,",")
            diffID = list(set(liID)^set(id))


            liProduct = str.split(inpProduct,",")
            diffProduct = list(set(liProduct)^set(product))



            if diffID == [] or len(diffID) != len(diffProduct):
                with open("idWomen.log", "w") as out:
                    out.write(",".join(id))
                    out.close()
                with open("itemsWomen.log", "w") as out:
                    out.write(",".join(product))
                    out.close()
                with open("logWomen.log", "a") as out:
                    tm = time.asctime(time.localtime(time.time())) + ": "
                    string = tm + "Nothing new added.\n"
                    out.write(string)
                    out.close()
            else:
                link = []
                for idx, val in enumerate(diffID):
                    temp = diffProduct[idx]
                    if " and " in temp:
                        temp = temp.replace(" and ","")
                    temp = temp.replace(" ","-")
                    link.append("https://uk.burberry.com/"+temp+"-p"+val)

                to = ["katie.price@burberry.com"]
                subject = 'New Womens Accesories in sale!'
                text = "New items added to sale, see below \n\n"
                ids = "New product ID's: "+ ", ".join(diffID) + '\n'
                products = "New Products: " + ", ".join(diffProduct) + '\n'
                links = "Product links: " + "\n, ".join(link) + '\n'
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

                with open("idWomen.log", "w") as out:
                    out.write(",".join(id))
                    out.close()
                with open("itemsWomen.log", "w") as out:
                    out.write(",".join(product))
                    out.close()

                with open("logWomen.log", "a") as out:
                    tm = time.asctime(time.localtime(time.time())) + ": "
                    sum = len(diffID)
                    string = tm + str(sum) +" new products detected, email sent" "\n"
                    out.write(string)
                    out.close()

        else:
            with open("idWomen.log", "w") as out:
                out.write(",".join(id))
                out.close()
            with open("itemsWomen.log", "w") as out:
                out.write(",".join(product))
                out.close()
            with open("logWomen.log","w") as out:
                tm = time.asctime( time.localtime(time.time())) + ": "
                string = tm + "Initial pull.\n"
                out.write(string)
                out.close()


    except requests.exceptions.RequestException as e:
        print("HTTP Error" + str(e))
    except Exception as e:
        sentFrom = gmailUser
        to = "nicholasvenis@hotmail.com"
        subject = "Script Error"
        emailtext = "Subject: {}\n\n{}".format(subject, e)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmailUser, gmailPass)
            server.sendmail(sentFrom, to, emailtext)
            server.close()
            print(e)
        except Exception as e:
            print(e)

pull()