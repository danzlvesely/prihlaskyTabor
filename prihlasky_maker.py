import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os, shutil
from tabordata import *

def gen_dite(ditefolder, dite):
    print(ditefolder)
    try:
        os.mkdir(ditefolder)
    except FileExistsError:
        pass
    with open("{0}souhlas.tex".format(ditefolder), "x") as f:
        f.write(tm1.render(dite=dite))
    os.system(f"pdfcsplain -output-directory={ditefolder} {ditefolder}souhlas.tex >> /dev/null")
    
    with open("{0}formulare.tex".format(ditefolder), "x") as f:
        f.write(tm3.render(dite=dite))
    os.system(f"pdfcsplain -output-directory={ditefolder} {ditefolder}formulare.tex  >> /dev/null")
    
    with open("{0}prihlaska.tex".format(ditefolder), "x") as f:
        f.write(tm2.render(dite=dite))
    os.system(f"pdfcsplain -output-directory={ditefolder} {ditefolder}prihlaska.tex >> /dev/null")



#source data
excel_file = SOURCEFILE 
data = pd.read_excel(excel_file)

lidi = [{} for _ in range(len(data))]

for udaj in data:
    for i, polozka in enumerate(data[udaj]):
        lidi[i][udaj] = str(polozka).replace(",",". ") if str(polozka) != "nan" else ""


for i in range(len(lidi)):
    if lidi[i]["category"] == "Skaut":
        lidi[i]["taborstart"] = TSKAUTSTART
        lidi[i]["price"] = SKAUTPRICE
    else:
        lidi[i]["taborstart"] = TVLCESTART
        lidi[i]["price"] = VLCEPRICE
    lidi[i]["birth"] = str(lidi[i]["birth"])
    lidi[i]["taborend"] = TEND
    lidi[i]["fatherphone"] = lidi[i]["fatherphone"][:9]
    lidi[i]["motherphone"] = lidi[i]["motherphone"][:9]
    lidi[i]["vs"] = str(10) + ("0" if i < 10 else "" )+ str(i)
print(lidi)

file_loader = FileSystemLoader('')
env = Environment(loader=file_loader)
tm1 = env.get_template("template/souhlas_o_poskytovani_informaci.tex")
tm2 = env.get_template("template/zavazna-prihlaska-na-letni-tabor-skaut.tex")
tm3 = env.get_template("template/formulare-na-tabor.tex")

shutil.rmtree("generated")
folder = "generated/"

os.mkdir(folder)

#prazdnejvlce
dite = {}
dite["category"] = "Vlče"
dite["taborstart"] = TVLCESTART
dite["taborend"] = TEND
dite["price"] = VLCEPRICE
dite["vs"] = "10...."
ditefolder = "{0}{1}/".format(folder, "EMPTYVLCE")
gen_dite(ditefolder, dite)

#prazdnejskaut
dite = {}
dite["category"] = "Skaut"
dite["taborstart"] = TSKAUTSTART
dite["taborend"] = TEND
dite["price"] = VLCEPRICE
dite["vs"] = "10...."
ditefolder = "{0}{1}/".format(folder, "EMPTYSKAUT")
gen_dite(ditefolder, dite)

l = []

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_mail(recipients, path):
    pass
    sender_email = "desitka@skaut.cz"
    msg = MIMEMultipart()
    msg['Subject'] = 'Informace ke skautskému táboru 2023'
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)

    filename = "data/email.txt"
    msg.attach(MIMEText(open(filename).read()))

    attachments = ["formulare.pdf", "prihlaska.pdf", "souhlas.pdf"]
    for a in attachments:
        pdf = MIMEApplication(open(f"{path}/{a}", 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename="formulare.pdf")
        msg.attach(pdf)

    raise NotImplementedError
    try:
        with smtplib.SMTP('yoda.eideo.cz', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("ouolim@eideo.cz", "###REDACTED###")
            smtpObj.sendmail(sender_email, recipients, msg.as_string())
    except Exception as e:
        print(e)


print("This is going to send emails to parents! Are you sure? Comment this line than")
exit(0)

for dite in lidi:
    l.append(str(dite["fullname"]) + " - " + str(dite["vs"]))
    ditefolder = "{0}{1}/".format(folder, dite["fullname"].replace(" ",""))
    string_encode = ditefolder.encode("ascii", "ignore")
    ditefolder = string_encode.decode()
    gen_dite(ditefolder, dite)

    mothermail = dite["mothermail"]
    mail = [mothermail, "danzl.vesely@gmail.com", "ouolim@eideo.cz"]

#    send_mail(mail, ditefolder)
    print(f"Would send mail to {mail} with files in {ditefolder}")

# VS
print("\n")
for i in l:
    print(i)
