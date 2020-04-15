from bs4 import BeautifulSoup
import requests
import time
from tkinter import * 
import tkinter.font 
from PIL import Image, ImageTk

country = "Turkey"
refresh_time = 10 #dakika
data_check= []
worldmetersLink = "https://www.worldometers.info/coronavirus/"

win = tkinter.Tk() #win ile tk'yi cagirdigimizi belirttik.
resim = Image.open("/home/pi/Desktop/arkaplanv2.jpg")
arkaplan_image = ImageTk.PhotoImage(resim)

def data_cleanup(array): #Araya giren +,- gibi sembolleri temizlemekte
    L = []    #kullanacagimiz fonksiyon.
    for i in array:
        i = i.replace("+","")
        i = i.replace("-","")
        i = i.replace(",",".")
        if i == "":
            i = "0"
        L.append(i.strip())
    return L

win.geometry('800x480') #Uygulamamizin boyutlari.
win.attributes('-fullscreen', True) #Tam ekran moduna gecis.
win.configure(bg='black') #Arkaplan rengini siyah yapiyoruz.

while True:
    try:
        html_page = requests.get(worldmetersLink)
        #Istatistik sayfasina baglanmayi dene.
    except requests.exceptions.RequestException as e:
        print (e)
        continue
    bs = BeautifulSoup(html_page.content, 'html.parser')
    #bs isimli bir 'BeautifulSoup, nesnesi yarat ve sayfanin html kodlarini onunla ayristir.

    search = bs.select("div tbody tr td")
    #html kodlari arasinda 'div', 'tbody', 'tr' ve 'td' etiketleri icinde
    #arama yapilmasini soyluyoruz cunku istedigimiz veriler burada.
    start = -1
    for i in range(len(search)):
        if search[i].get_text().find(country) !=-1:
            #Once girdigimiz ulke ismini bu etiketlerde aratiyoruz.
            start = i
            break
    data = []            #Bulduktan sonra data isimli bir array yaratiyoruz.
    for i in range(1,8): #Bu array icine sirayla o html etiketi altinda yer alan verileri kaydediyoruz.
        try:
            data = data + [search[start+i].get_text()]
        except:
            data = data + ["0"]

    data= data_cleanup(data) # Araya giren sembolleri temizletiyoruz.

    if data_check != data: #Eger son olcumle yeni olcum arasinda bir fark varsa
        data_check = data #yarattigimiz degiskenleri bu verilerle dolduruyoruz.
        toplam_vaka=data[0]
        yeni_vaka=data[1]
        toplam_vefat = data[2]
        yeni_vefat= data[3]
        toplam_taburcu = data[4]
        #Asagida arkaplana resmimizi koyuyoruz.
        #Etiketlerin uzerinde olmasi icin once resmi koymaliyiz.
        canv = Canvas(win, width=810,height=490, background="black")
        canv.create_image(400, 240, image = arkaplan_image)
        canv.place(x=-3,y=-3)

        etiket1 = Label(win, text=(toplam_vaka),bg="white",fg="black", height=1, width=16,font = "Helvetica 30 bold italic")
        etiket1.place(x=348, y=185) 

        etiket2 = Label(win, text=(toplam_vefat),bg="white",fg="black", height=1, width=8, font = "Helvetica 20 bold italic")
        etiket2.place(x=380, y=345) 

        etiket3 = Label(win, text = (toplam_taburcu),bg="white",fg="black", height=1, width=6, font = "Helvetica 20 bold italic")
        etiket3.place(x=640, y=345)
        
        etiket4 = Label(win, text = (yeni_vaka),bg="white",fg="black", height=1, width=8, font = "Helvetica 22 bold italic")
        etiket4.place(x=470, y=245)
            
        etiket5 = Label(win, text = (yeni_vefat),bg="white",fg="black", height=1, width=5, font = "Helvetica 16 bold italic")
        etiket5.place(x=405, y=390)

        win.mainloop() #Penceremizi yaratiyoruz.
    else:
        time.sleep(refresh_time*60) #1 saat sonra tekrar deneyecegiz.
        continue

