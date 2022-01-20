import requests
import psycopg2
import psycopg2.extras

# 도로명 주소 변환기
def main():
    conn = psycopg2.connect("host=localhost dbname=bread_mapper_dev user=postgres password=skansmfqh@515")
    keywords = getKeywords(conn)
    
    for row in keywords:
        print(row)
    doSearch(keywords)

def getKeywords(conn):
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM store where sido_name IS NULL LIMIT 10")
    result = cur

    return result

def doSearch(keywords):
    for keyword in keywords: 
        url = "https://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDIyMDEyMDExMjAyMTExMjE1NzA=&currentPage=1&countPerPage=999&keyword=" + keyword

        requests.get(url)

        print(url)

main()
