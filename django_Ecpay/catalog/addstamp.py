import  sys
import fitz
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os.path
from os.path import basename
from os import listdir
from os.path import isfile, join
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import pathlib
import shutil
# from .models import Order

import smtplib
def watermark(name,file,savepath,word,water): 
    img = Image.new('RGBA', (500,200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font_type = ImageFont.truetype("arial.ttf", 40)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((0, 0),word,(0,0,0,15),font=font_type)
    # img.putalpha(128)
    img.save(savepath+'sample-test.png')
    try:
        print('intry')
        doc = fitz.open(file)
        print('indoc')
        img2 = open(savepath+"sample-test.png", "rb").read()

        if water:
            for i in range(len(doc)):
                page=doc[i]
                w,h =page.MediaBoxSize
                rect1 = fitz.Rect(int(0.2*w), int(0.4*h), int(0.8*w), int(0.4*h+1.2/5*w))
                rect2 = fitz.Rect(int(0.2*w), int(0.1*h), int(0.8*w), int(0.1*h+1.2/5*w))
                rect3 = fitz.Rect(int(0.2*w), int(0.7*h), int(0.8*w), int(0.7*h+1.2/5*w))
                
                page.insertImage(rect1, stream = img2)
                page.insertImage(rect2, stream = img2)
                page.insertImage(rect3, stream = img2)
        doc.save(savepath+name)
    except:
        doc.close()
        print('except')
        shutil.copy(file,savepath)
    os.remove(savepath+'sample-test.png')

def addstamp(buyer,item_id,water):
    itempath = "./catalog/item_file/"+str(item_id)+"/"
    itemfiles = [f for f in listdir(itempath) if isfile(join(itempath, f))]
    mypath = "./catalog/mail_file/"+str(buyer)+"/"
    if not os.path.exists(mypath):
        os.mkdir(mypath)
    print('a')
    for f in itemfiles:
        watermark(f,os.path.join(itempath, f),mypath,buyer,bool(water))
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "【KnowledgePay】 您購買的產品來囉~"  #郵件標題
    content["from"] = "aicoinmaker@gmail.com"  #寄件者
    content["to"] = buyer #收件者
    content.attach(MIMEText("感謝您的購買，商品已在附件中，若有任何問題，請於三天內與我們聯絡。"))  #郵件內容
    for f in onlyfiles:  # add files to the message
        file_path = os.path.join(mypath, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        content.attach(attachment)
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("aicoinmaker@gmail.com", "jbgzynjayamqasfk")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
    shutil.rmtree(mypath)

# sendemail('joelin870423@gmail.com',2)
# def addstamp(buyer,item_id,water):
#     sendemail(buyer,item_id,water)