import requests
import psycopg2

# 도로명 주소 변환기
def main():
    conn = psycopg2.connect("host=localhost dbname=bread_mapper_dev user=postgres password=skansmfqh@515")
    keywords = getKeywords(conn)
    print(keywords)
    doSearch(keywords)

def getKeywords(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM store where sido_name IS NULL")
    result = [r[0] for r in cur.fetchall()]

    return result

def doSearch(keywords):
    for keyword in keywords: 
        url = "https://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey=U01TX0FVVEgyMDIyMDEyMDExMjAyMTExMjE1NzA=&currentPage=1&countPerPage=999&keyword=" + keyword

        requests.get(url)

        print(url)

main()
