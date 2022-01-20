from re import L
import requests
import psycopg2
import psycopg2.extras
import xmltodict
import json

# 도로명 주소 변환기
def main():
    print('start ...')
    conn = psycopg2.connect("host=localhost dbname=bread_mapper_dev user=postgres password=skansmfqh@515")
    keywords = getKeywords(conn)
    doSearch(keywords, conn)

def getKeywords(conn):
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute("SELECT doro_post_address, id FROM store WHERE sido_name IS NULL")

    return cur.fetchall()

def getTotalLength(conn):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM store WHERE sido_name IS NULL")

    print(cur.fetchone())

def doSearch(keywords, conn):
    total = getTotalLength(conn)
    count = 0

    for row in keywords:
        count += 1 
        logging(count, total)
        keyword = getKeyword(row['doro_post_address'])
        id=row['id']
        
        url = "https://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDIyMDEyMDExMjAyMTExMjE1NzA=&currentPage=1&countPerPage=999&keyword=" + keyword

        response = requests.get(url)

        newJson = json.loads(json.dumps(xmltodict.parse(response.text), indent=4, ensure_ascii=False))
        
        json = None

        if newJson['results']:
            juso = newJson['results']['juso']
        
        if type(juso) is not list and json is not None:
            fullAddress = newJson['results']['juso']['jibunAddr']
        elif type(juso) is list:
            fullAddress = newJson['results']['juso'][0]['jibunAddr']

        insertData (id, fullAddress, conn)

def insertData (id, fullAddress, conn):
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("UPDATE store SET full_address = '" + fullAddress + "' where id = " + str(id))

def getKeyword (address):
    splitedAddress = address.split(' ')

    if splitedAddress[2][-1] == '로':
        return splitedAddress[2] + " " + splitedAddress[3]
    elif splitedAddress[3][-1] == '로':
        return splitedAddress[3] + " " + splitedAddress[4]
    else:
        return ""

def logging(idx, total):
    print("searching ..." + str(idx) + "/" + str(total))

main()
