import requests
import psycopg2
import psycopg2.extras
import xmltodict
import json

# 도로명 주소 변환기
def main():
    conn = psycopg2.connect("host=localhost dbname=bread_mapper_dev user=postgres password=skansmfqh@515")
    keywords = getKeywords(conn)
    doSearch(keywords)

def getKeywords(conn):
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM store where sido_name IS NULL LIMIT 10")
    result = cur

    return result

def doSearch(keywords):
    for row in keywords: 
        keyword = getKeyword(row['doro_post_number'])
        print(keyword)
        
        url = "https://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDIyMDEyMDExMjAyMTExMjE1NzA=&currentPage=1&countPerPage=999&keyword=" + keyword

        response = requests.get(url)

        print(json.dumps(xmltodict.parse(response.text), indent=4))

def getKeyword (address):
    splitedAddress = address.split(' ')
    print(splitedAddress[2][-1])

    if splitedAddress[2][-1] == '로':
        return splitedAddress[2] + " " + splitedAddress[3]
    elif splitedAddress[3][-1] == '로':
        return splitedAddress[3] + " " + splitedAddress[4]
    else:
        return ""

main()
