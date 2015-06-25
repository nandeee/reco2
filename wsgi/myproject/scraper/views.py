from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
# import shutil
# import requests
import json
import os
import sqlite3
# import traceback, os.path
# import bs4
# import re
# import urllib2
# from bs4 import BeautifulSoup
# import xlsxwriter
from pprint import pprint

DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
LOG_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'txt')

def getItems(request):
    #raw_input("Press Enter")
    conn=sqlite3.connect('database.db');
    c=conn.cursor()
    c.execute("select * from item")
    conn.close()
    #res = {"param1": "one", "param2": "two"}
    return HttpResponse(json.dumps(res), content_type='application/json')

def index(request):
    template = loader.get_template("scraper/index.html")
    return HttpResponse(template.render())

def reco(request):
    template = loader.get_template("scraper/reco.html")
    return HttpResponse(template.render())

def getLinks(request, city, category):
    tot = 0
    fileTot = os.path.join(LOG_ROOT, "zomTot-" + city + "-" + category + ".txt")
    fileLinks = os.path.join(LOG_ROOT, "zomLinks-" + city + "-" + category + ".txt")
    fileStart = os.path.join(LOG_ROOT, "pos-" + city + "-" + category + ".txt")
    fileErr = os.path.join(LOG_ROOT, "zomErr-" + city + "-" + category + ".txt")
    with open(fileStart, "w") as f:
        f.write(str(0))
    with open(fileErr, "w") as f:
        f.write(str(0))
    if os.path.exists(fileLinks):
        file(fileLinks, "w").close()
    if category == "pb":
        baseUrl = "https://www.zomato.com/" + city + "/restaurants?bar=1&page="
        response = urllib2.urlopen(baseUrl + "1")
        html = response.read()
        soup = BeautifulSoup(html)
        numPages = int(soup.select(".pagination-number div")[0].get_text().split(" ")[3])
        for x in xrange(1, numPages + 1):
            url = baseUrl + str(x)
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html)
            items = soup.select(".resZS")
            for item in items:
                link = item.select("h3 a")[0].get("href").encode("utf-8")
                with open(fileLinks, "a") as f:
                    f.write(link + "\n")
                tot += 1
                with open(fileTot, "w") as f:
                    f.write(str(tot))
    else:
        baseUrl = "http://www.justdial.com/Bangalore/Liquor-Retailers/ct-82591/page-"
        i = 1
        while True:
            url = baseUrl + str(i)
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html)
            items = soup.findAll("section", id=lambda x: x and x.startswith('bcard'))
            print len(items)
            print "abhishek"
            if len(items):
                for item in items:
                    link = item.select(".jcn a")[0].get("href")
                    with open(fileLinks, "a") as f:
                        f.write(link + "\n")
                    tot += 1
                    with open(fileTot, "w") as f:
                        f.write(str(tot))
                i += 1
            else:
                break
    if os.path.exists(fileTot):
        with open(fileTot) as f:
            retTot = int(f.readline())
    else:
        retTot = 0
    res = {"fileName": "zomLinks-" + city + "-" + category + ".txt", "retTot": retTot}
    return HttpResponse(json.dumps(res), content_type='application/json')

def genExcel(request, city, category):
    workbook = xlsxwriter.Workbook(os.path.join(LOG_ROOT, "zomExcel-" + city + "-" + category + ".xlsx"))
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    if category == "pb":
        labels = ["Name", "Address", "Geotag", "Wi-Fi", "Price", "Card accepted", "Delivery", "Timings", "Phone number", "Rating", "Votes", "Cuisines", "Establishment type", "Happy hours"]
    else:
        labels = ["Name", "Address", "Geotag", "Timings", "Phone number", "Card accepted", "Rating"]
    for x in xrange(0, len(labels)):
        worksheet.write(0, x, labels[x], bold)
    row = 2
    fileDetails = os.path.join(LOG_ROOT, "zomDetails-" + city + "-" + category + ".txt")
    with open(fileDetails) as f:
        for line in f:
            listOfParts = line.rstrip().split(" ]|[ ")
            for i, part in enumerate(listOfParts):
                worksheet.write(row, i, part.decode("utf-8"))
            row += 1
    workbook.close()
    res = {"fileName": "zomExcel-" + city + "-" + category + ".xlsx"}
    return HttpResponse(json.dumps(res), content_type='application/json')

def delAll(request):
    shutil.rmtree(LOG_ROOT)
    os.makedirs(LOG_ROOT)
    open(os.path.join(LOG_ROOT, "asdf.xyz"), 'w').close()
    res = {"status": "Done"}
    return HttpResponse(json.dumps(res), content_type='application/json')

def check(request):
    res = {"status": "Done"}
    url = "http://www.justdial.com/"
    res = requests.get(url).content
    soup = BeautifulSoup(res)
    pprint(soup)
    return HttpResponse(json.dumps(res), content_type='application/json')

def getPos(request, city, category):
    fileStart = os.path.join(LOG_ROOT, "pos-" + city + "-" + category + ".txt")
    fileErr = os.path.join(LOG_ROOT, "zomErr-" + city + "-" + category + ".txt")
    with open(fileStart) as f:
        start = int(f.readline())
    with open(fileErr) as f:
        retErr = int(f.readline())
    res = {"pos": start, "retErr": retErr}
    return HttpResponse(json.dumps(res), content_type='application/json')

def testSend(request, A, B):
    print A
    print B
    res = {"A": A, "B": B}
    return HttpResponse(json.dumps(res), content_type='application/json')

def processFile(request, city, category):
    err = 0
    start = 0
    fileLinks = os.path.join(LOG_ROOT, "zomLinks-" + city + "-" + category + ".txt")
    fileStart = os.path.join(LOG_ROOT, "pos-" + city + "-" + category + ".txt")
    fileErr = os.path.join(LOG_ROOT, "zomErr-" + city + "-" + category + ".txt")
    fileDetails = os.path.join(LOG_ROOT, "zomDetails-" + city + "-" + category + ".txt")
    errorLog = os.path.join(LOG_ROOT, "zomErrors-" + city + "-" + category + ".txt")
    if os.path.exists(fileDetails):
        file(fileDetails, "w").close()
    fp = open(fileLinks)
    for i, line in enumerate(fp):
        if i < start:
            continue
        if category == "pb":
            try:
                link = line.strip()
                response = urllib2.urlopen(link)
                html = response.read()
                soup = BeautifulSoup(html)
                name = soup.select(".res-name a span")[0].get_text()
                addressTag = soup.select(".res-main-address")[0]
                address = addressTag.select(".res-main-subzone-links a")[0].get_text() + addressTag.select(".res-main-subzone-links span")[0].get_text() + " " + addressTag.select(".res-main-address-text")[0].get_text().strip().replace("India", "")
                latitude = soup.find_all("meta", attrs={"property": "place:location:latitude"})[0].get("content")
                longitude = soup.find_all("meta", attrs={"property": "place:location:longitude"})[0].get("content")
                geoTag = latitude + ", " + longitude
                wifi = "No" if soup.find(text="Wifi Available") == None else "Yes"
                price = soup.find_all("span", attrs={"itemprop": "priceRange"})[0].get_text().strip() if len(soup.find_all("span", attrs={"itemprop": "priceRange"})) else ""
                acceptsCard = "No" if soup.find(text="Cards accepted") == None else "Yes"
                delivery = "Yes" if len(soup.select(".order-now-banner")) else "No"
                timings = soup.select(".res-info-timings .clearfix")[0].select("div span")[0].get_text() if len(soup.select(".res-info-timings .clearfix")) else ""
                numbers = []
                numbersList = soup.select("#phoneNoString span span span")
                for num in numbersList:
                    numbers.append(num.get_text())
                numbersString = ", ".join(numbers)
                rating = soup.find_all("div", attrs={"itemprop": "ratingValue"})[0].get_text().strip() if len(soup.find_all("div", attrs={"itemprop": "ratingValue"})) else ""
                ratingVotes = soup.select(".rating-info .rating-votes-div span span")[0].get_text() if len(soup.select(".rating-info .rating-votes-div span span")) else ""
                desc = soup.select(".res-info-cuisines")
                cuisines = desc[0].select("a")
                est = soup.select(".res-info-cuisines") if len(soup.select(".res-info-cuisines")) else []
                cuisinesList = []
                estList = []
                for val in cuisines:
                    cuisinesList.append(val.get_text())
                for val in est:
                    estList.append(val.get_text())
                cuisinesString = ", ".join(cuisinesList)
                estString = ", ".join(estList)
                happyHours = "Yes" if len(soup.select(".happy-hours-resinfo-qv")) else "No"
                if happyHours == "Yes":
                    hHTimings = soup.select(".happy-hours-resinfo-qv")[0].get_text().replace("Happy Hours:", "").strip()
                    happyHours = ", ".join(["Yes", hHTimings])
                resCondensed = " ]|[ ".join([name, address, geoTag, wifi, price, acceptsCard, delivery, timings, numbersString, rating, ratingVotes, cuisinesString, estString, happyHours])
                with open(fileDetails, "a") as f:
                    f.write(resCondensed.encode("utf-8") + "\n")
            except Exception, e:
                err += 1
                top = traceback.extract_stack()[-1]
                error = ', '.join([e.message, type(e).__name__, os.path.basename(top[0]), str(top[1])])
                with open(errorLog, "a") as f:
                    f.write(error + "\n")
                    f.write(line)
                with open(fileErr, "w") as f:
                    f.write(str(err))
        else:
            try:
                link = line.strip()
                response = urllib2.urlopen(link)
                html = response.read()
                soup = BeautifulSoup(html)
                name = soup.select(".jcnlt span")[1].get_text().strip()
                address = soup.select(".jadlt")[0].get_text().replace("Map", "").strip()
                address = address.encode('ascii',errors='ignore').replace("\r", "").replace("\t", "").replace("\n", "").replace("|", "").strip()
                latitude = soup.select("#lat_b")[0].get("value")
                longitude = soup.select("#lng_b")[0].get("value")
                geoTag = latitude + ", " + longitude
                timings = soup.select(".reset td")[0].get_text().strip()
                numList = []
                numMob = soup.select(".continfo .jmob")
                if len(numMob):
                    for sibling in numMob[0].next_siblings:
                        if isinstance(sibling, bs4.element.Tag):
                            numList.append(sibling.get_text())
                        else:
                            continue
                numTel = soup.select(".continfo .jtel")
                if len(numTel):
                    for sibling in numTel[0].next_siblings:
                        if isinstance(sibling, bs4.element.Tag):
                            numList.append(sibling.get_text())
                        else:
                            continue
                numString = ", ".join(numList)
                payTag = soup.select(".fcont")
                for tag in payTag:
                    mop = tag.find(text="Modes of Payment")
                    if mop == None:
                        continue
                    else:
                        isCard = tag.find(text=re.compile('card', flags=re.IGNORECASE))
                        if isCard == None:
                            acceptsCard = "No"
                        else:
                            acceptsCard = "Yes"
                        break
                rating = soup.select(".rating span")[0].get("title")
                resCondensed = " ]|[ ".join([name, address, geoTag, timings, numString, acceptsCard, rating])
                with open(fileDetails, "a") as f:
                    f.write(resCondensed.encode("utf-8") + "\n")
            except Exception, e:
                err += 1
                top = traceback.extract_stack()[-1]
                error = ', '.join([e.message, type(e).__name__, os.path.basename(top[0]), str(top[1])])
                with open(errorLog, "a") as f:
                    f.write(error + "\n")
                    f.write(line)
                with open(fileErr, "w") as f:
                    f.write(str(err))
        start += 1
        with open(fileStart, "w") as f:
            f.write(str(start))
    res = {"fileName": "zomDetails-" + city + "-" + category + ".txt"}
    return HttpResponse(json.dumps(res), content_type='application/json')
