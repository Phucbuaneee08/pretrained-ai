import requests
from bs4 import BeautifulSoup
import json

# URL của trang web bạn muốn crawl
url = 'https://www.vinmec.com/vi/bai-viet/tim-kiem/?q=s%C6%A1+c%E1%BB%A9u&page=5'

# Sử dụng thư viện requests để tải nội dung của trang web
response = requests.get(url)

# Kiểm tra xem trang web đã được tải thành công hay chưa
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích nội dung HTML của trang
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tìm tất cả các thẻ h1 và p trên trang web
    h1_tags = soup.find_all('article')
    for a in h1_tags:
        print(a.find('h3'))
    # p_tags = soup.find_all('p')

    # # Tạo một danh sách để lưu trữ dữ liệu crawl
    # data = []

    # # Lặp qua danh sách các thẻ h1 và p và lấy nội dung của chúng
    # for h1 in h1_tags:
    #     data.append({
    #         'patterns': h1.text,
    #         'responses': ''  # Đặt responses là chuỗi trống vì bạn không đưa ra thông tin về responses
    #     })

    # for p in p_tags:
    #     data.append({
    #         'patterns': '',
    #         'responses': p.text
    #     })

    # # Lưu dữ liệu vào tệp JSON
    # with open('data.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(data, json_file, ensure_ascii=False, indent=4)

    # print("Dữ liệu đã được lưu vào tệp data.json.")
else:
    print("Không thể tải trang web.")

