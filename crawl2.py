import requests
from bs4 import BeautifulSoup
import re
import json
import threading
import os
prefix = ['thi-truong','du-an','quy-hoach','chu-dau-tu']
def add_http(url):
    # Kiểm tra xem đường dẫn đã có "http://" hoặc "https://" chưa
    if not re.match('(?:http|https)://', url):
        # Nếu không có, thêm "http://" vào đầu đường dẫn
          url = 'https://www.vinmec.com/vi' + url
    return url
def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()
def process_page(page):
    results = []
    res = requests.get('https://www.vinmec.com/vi/bai-viet/tim-kiem/?q=s%C6%A1+c%E1%BB%A9u&page='+str(page))
    soup = BeautifulSoup(res.content, 'html.parser')
    elements = soup.find_all('article')
    if not elements:
        return results  

    for element in elements:
        try:
            div = element.find('h3')
            question = div.find('a')
            link_answer = add_http(question['href'])
            print(link_answer)
            res2 = requests.get(link_answer)
          
            soup2 = BeautifulSoup(res2.content, 'html.parser')
            ans = soup2.select('div[class*="streamfield"]')            
            ans = str(ans)
            ans = remove_html_tags(ans)
            ans = ans.replace("\n", "")
            ans = ans.replace("  ", "")
            ans = ans.replace("\r", "")
            results.append({'category':'','question': question.text, 'answer': ans})
        except:
            print(question['href'])
      

     
    
    return results

def main():
    threads = []
    num_pages = 10
    num_threads = 4  # Số luồng mong muốn

    # Tạo một Lock để đồng bộ hóa việc ghi file
    file_lock = threading.Lock()
    
    for i in range(1, 55):  # Bắt đầu từ trang thứ 41
        thread = threading.Thread(target=lambda page=i: save_page_results(page, file_lock))
        thread.start()
        threads.append(thread)

        # Điều chỉnh số lượng luồng nếu vượt quá giới hạn
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    print("Crawling completed.")

def save_page_results(page, file_lock):
  
    results = process_page(page)
    directory = "C:/Users/Laptop cua Phuc/Documents/Socapcuu24h/Data"
    
    file_name = os.path.join(directory, f'data_page{page}.json')
    with open(file_name, 'w', encoding='utf-8') as file:
        # Sử dụng Lock để đảm bảo chỉ có một luồng ghi file tại một thời điểm
        file_lock.acquire()
        json.dump(results, file, ensure_ascii=False, indent=4)
        file_lock.release()
    print("Crawl page "+str(page)+"Successfully!")


if __name__ == "__main__":
    main()
