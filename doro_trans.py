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

    cur.execute("SELECT doro_post_address, id FROM store WHERE full_address IS NULL")

    return cur.fetchall()

def getTotalLength(conn):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM store WHERE full_address IS NULL")
    result = cur.fetchone()
    
    return result[0]

def doSearch(keywords, conn):
    total = getTotalLength(conn)
    count = 0

    for row in keywords:
        count += 1 
        keyword = getKeyword(row['doro_post_address'])
        id=row['id']
        
        url = "https://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDIyMDEyMDExMjAyMTExMjE1NzA=&currentPage=1&countPerPage=999&keyword=" + keyword

        response = requests.get(url)

        jsonData = json.loads(json.dumps(xmltodict.parse(response.text), indent=4, ensure_ascii=False))
        
        print(keyword)
        fullAddress = processGetFullAddress(jsonData)
        processInsertDataWithFullAddress(fullAddress, count, total, id, conn)

def processGetFullAddress(jsonData):
    try:
        return getFullAddress(jsonData)
    except:
        print('skip...')
        return None

def getFullAddress(jsonData):
    juso = getJusoData(jsonData)
    fullAddress = getFullAddressWithJuso(juso)

    return fullAddress

def processInsertDataWithFullAddress(fullAddress, count, total, id, conn):
    try:
        insertDataWithFullAddress (fullAddress, count, total, id, conn)
    except:
        print('err processInsertDataWithFullAddress...')
        print(fullAddress)


def insertDataWithFullAddress (fullAddress, count, total, id, conn):
    if fullAddress is not None:
        logging(count, total, fullAddress, id)
        insertData (id, fullAddress, conn)

def getFullAddressWithJuso (juso):
    fullAddress = None
    
    if type(juso) is not list and juso is not None:
        fullAddress = juso['jibunAddr']
    elif type(juso) is list:
        fullAddress = juso[0]['jibunAddr']

    return fullAddress

def getJusoData(jsonData):
    juso = None

    if jsonData['results']:
        juso = jsonData['results']['juso']

    return juso

def insertData (id, fullAddress, conn):
    print("excute query... " + "UPDATE store SET full_address = '" + fullAddress + "' where id = " + str(id))
    cur = conn.cursor()
    cur.execute("UPDATE store SET full_address = '" + fullAddress + "' where id = " + str(id))
    conn.commit()

def getKeyword (address):
    splitedAddress = address.split(' ')

    if splitedAddress[2][-1] == '로':
        return splitedAddress[2] + " " + splitedAddress[3]
    elif splitedAddress[3][-1] == '로':
        return splitedAddress[3] + " " + splitedAddress[4]
    else:
        return ""

def logging(idx, total,fullAddress,id):
    print(str(id) + ". searching ...:" + fullAddress + "   " + str(idx) + "/" + str(total))

main()
