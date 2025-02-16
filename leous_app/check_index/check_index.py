# import os
# import json
# import time
# import requests
# import pandas as pd
# from datetime import datetime, timedelta
# import sys
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from collections import OrderedDict

# # 🔹 Cấu hình mặc định
# DEFAULT_CREDITS = 2500
# CREDITS_FILE = "credits.json"
# API_KEY_FILE = "api_key.txt"
# SERPER_SEARCH_URL = "https://google.serper.dev/search"

# # 🔹 Xác định thư mục Downloads của hệ thống
# DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
# RESULT_FILE = os.path.join(DOWNLOADS_FOLDER, "google_index_results.csv")

# # 🔹 Đọc danh sách URL từ file urls.txt và đảm bảo thứ tự
# with open("urls.txt", "r", encoding="utf-8") as file:
#     urls = [line.strip() for line in file.readlines() if line.strip()]

# # 🔹 Dictionary để lưu kết quả theo đúng thứ tự ban đầu
# results = OrderedDict((url, "Pending") for url in urls)

# # 🔹 Kiểm tra và tải API keys từ file
# def get_api_keys():
#     if os.path.exists(API_KEY_FILE):
#         with open(API_KEY_FILE, "r") as f:
#             keys = [line.strip() for line in f.readlines() if line.strip()]
#             return list(set(keys))  # Loại bỏ trùng lặp
#     return []

# api_keys = get_api_keys()
# current_api_index = 0  # Bắt đầu từ API đầu tiên

# # 🔹 Kiểm tra và tải credits từ file JSON
# def get_credits():
#     if os.path.exists(CREDITS_FILE):
#         with open(CREDITS_FILE, "r") as f:
#             try:
#                 return json.load(f)
#             except json.JSONDecodeError:
#                 return {}
#     return {}

# credits_data = get_credits()

# # 🔹 Đảm bảo mỗi API có credits riêng
# for api in api_keys:
#     if api not in credits_data:
#         credits_data[api] = DEFAULT_CREDITS

# # 🔹 Lưu số credits vào file JSON
# def save_credits():
#     with open(CREDITS_FILE, "w") as f:
#         json.dump(credits_data, f)

# # 🔹 Hiển thị danh sách API Keys và số credits, yêu cầu xác nhận trước khi chạy
# def show_api_status():
#     # Tính tổng credits, chỉ cộng những API có credits > 0
#     total_credits = sum(credits for api, credits in credits_data.items() if credits > 0)

#     print(f"\n🔥 **Tổng credits khả dụng: {total_credits}** 🔥\n")

#     for i, api in enumerate(api_keys, start=1):
#         status = f"{credits_data.get(api, 0)} credits"
#         if credits_data.get(api, 0) <= 0:
#             status += " (⚠ Hết credits)"
#         print(f"{i}/ {api} hiện đang còn {status}")

#     if total_credits == 0:
#         print("\n❌ Tất cả API Keys đều đã hết credits! Hãy thêm API mới.")

#     while True:
#         choice = input("\n🔹 Nhấn 'Enter' để tiếp tục kiểm tra index hoặc nhập 'n' để thoát: ").strip().lower()
#         if choice == "":
#             break
#         elif choice == "n":
#             sys.exit("🚪 Thoát chương trình.")

# show_api_status()  # Gọi hàm hiển thị và chờ người dùng xác nhận trước khi chạy


# # 🔹 Nhập số giờ chạy từ người dùng (tính theo giờ)
# while True:
#     try:
#         run_hours = int(input("⏳ Nhập số giờ chạy chương trình: "))
#         break
#     except ValueError:
#         print("⚠ Vui lòng nhập số nguyên hợp lệ.")

# # 🔹 Nhập số lớp kiểm tra từ người dùng
# while True:
#     try:
#         check_layers = input("🔍 Nhập số lớp kiểm tra index (1: site:url, 2: site:url + \"url\", 3: site:url + \"url\" + cache:url) [Mặc định: 1]: ").strip()
#         if check_layers == "":
#             check_layers = 1
#         else:
#             check_layers = int(check_layers)
#             if check_layers not in [1, 2, 3]:
#                 raise ValueError
#         break
#     except ValueError:
#         print("⚠ Vui lòng nhập 1, 2 hoặc 3.")

# # 🔹 Tính toán thời gian kết thúc
# start_time = datetime.now()
# end_time = start_time + timedelta(hours=run_hours)

# # 🔹 Kiểm tra API key có thể gửi request không
# def test_api_key(api_key):
#     headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
#     payload = {"q": "test", "gl": "VN", "hl": "vi", "num": 1}
#     try:
#         response = requests.post(SERPER_SEARCH_URL, json=payload, headers=headers, timeout=10)
#         return response.status_code == 200
#     except requests.exceptions.RequestException:
#         return False

# # 🔹 Tìm API Key hợp lệ
# def get_valid_api_key():
#     global current_api_index

#     while True:
#         api_keys[:] = get_api_keys()

#         if not api_keys:
#             print("❌ Không có API Key nào hợp lệ! Hãy nhập API mới.")
#             new_keys = input("🔑 Nhập API keys (cách nhau bằng dấu phẩy) hoặc bấm 'n' để thoát: ").strip()
#             if new_keys.lower() == "n":
#                 sys.exit("🚪 Thoát chương trình.")
#             else:
#                 new_keys_list = [key.strip() for key in new_keys.split(",")]
#                 api_keys.extend(new_keys_list)
#                 for key in new_keys_list:
#                     credits_data[key] = DEFAULT_CREDITS
#                 save_credits()

#         api_key = api_keys[current_api_index]
#         if credits_data[api_key] > 0 and test_api_key(api_key):
#             return api_key

#         current_api_index = (current_api_index + 1) % len(api_keys)

# SERPER_API_KEY = get_valid_api_key()

# # 🔹 Hàm gọi API Serper.dev để tìm kiếm trên Google
# def search_google(query):
#     global SERPER_API_KEY

#     if credits_data[SERPER_API_KEY] <= 0:
#         print(f"❌ API Key {SERPER_API_KEY} đã hết credits. Chuyển API...")
#         SERPER_API_KEY = get_valid_api_key()

#     headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
#     payload = {"q": query, "gl": "VN", "hl": "vi", "num": 10}

#     try:
#         response = requests.post(SERPER_SEARCH_URL, json=payload, headers=headers, timeout=10)
#         data = response.json()
#         credits_data[SERPER_API_KEY] -= 1
#         save_credits()
#         print(f"🔹 Credits còn lại ({SERPER_API_KEY}): {credits_data[SERPER_API_KEY]}")

#         if "organic" in data and len(data["organic"]) > 0:
#             return [result["link"] for result in data["organic"]]
#         else:
#             return []
#     except requests.exceptions.RequestException:
#         return []

# # 🔹 Hàm kiểm tra index theo số lớp người dùng chọn
# def check_google_index(url):
#     # Bước 1: Kiểm tra bằng site:url
#     query1 = f"site:{url}"
#     result1 = search_google(query1)
#     if check_layers >= 1 and any(url in res for res in [result1]):
#         return url, "Indexed"

#     # Bước 2: Kiểm tra bằng URL trích dẫn (nếu chọn >= 2)
#     if check_layers >= 2:
#         query2 = f'"{url}"'
#         result2 = search_google(query2)
#         if any(url in res for res in [result2]):
#             return url, "Indexed"

#     # Bước 3: Kiểm tra cache của Google (nếu chọn = 3)
#     if check_layers == 3:
#         query3 = f"cache:{url}"
#         result3 = search_google(query3)
#         if any(url in res for res in [result3]):
#             return url, "Indexed"

#     return url, "Not Indexed"

# # 🔹 Chạy chương trình
# try:
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         future_to_index = {executor.submit(check_google_index, url): i for i, url in enumerate(urls)}

#         for future in as_completed(future_to_index):
#             url, status = future.result()
#             results[urls[future_to_index[future]]] = status
#             print(f"{future_to_index[future]+1}/{len(urls)} - {url}: {status}")

#             pd.DataFrame(results.items(), columns=["URL", "Index Status"]).to_csv(RESULT_FILE, index=False)

# except KeyboardInterrupt:
#     print("\n⏹️ Chương trình bị dừng.")
# finally:
#     print(f"\n✅ Kết quả đã được lưu vào: {RESULT_FILE}")


import os
import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import OrderedDict
from urllib.parse import urlparse

# 🔹 Cấu hình mặc định
DEFAULT_CREDITS = 2500
CREDITS_FILE = "credits.json"
API_KEY_FILE = "api_key.txt"
SERPER_SEARCH_URL = "https://google.serper.dev/search"

# 🔹 Xác định thư mục lưu kết quả
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
RESULT_FILE = os.path.join(DOWNLOADS_FOLDER, "google_index_results.csv")

# 🔹 Đọc danh sách URL từ file urls.txt
with open("urls.txt", "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file.readlines() if line.strip()]

# 🔹 Dictionary để lưu kết quả theo đúng thứ tự ban đầu
results = OrderedDict((url, "Pending") for url in urls)

# 🔹 Đọc danh sách API Keys từ file
def get_api_keys():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            keys = [line.strip() for line in f.readlines() if line.strip()]
            return list(set(keys))  # Loại bỏ trùng lặp
    return []

api_keys = get_api_keys()
current_api_index = 0

# 🔹 Tải số credits từ file JSON
def get_credits():
    if os.path.exists(CREDITS_FILE):
        with open(CREDITS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

credits_data = get_credits()

# 🔹 Đảm bảo mỗi API có credits riêng
for api in api_keys:
    if api not in credits_data:
        credits_data[api] = DEFAULT_CREDITS

# 🔹 Lưu số credits vào file JSON
def save_credits():
    with open(CREDITS_FILE, "w") as f:
        json.dump(credits_data, f)

# 🔹 Hiển thị danh sách API Keys và số credits
def show_api_status():
    total_credits = sum(credits_data.get(api, 0) for api in api_keys if credits_data.get(api, 0) > 0)
    
    print(f"\n🔥 **Tổng credits khả dụng: {total_credits}** 🔥\n")
    for i, api in enumerate(api_keys, start=1):
        status = f"{credits_data.get(api, 0)} credits"
        if credits_data.get(api, 0) <= 0:
            status += " (⚠ Hết credits)"
        print(f"{i}/ {api} hiện đang còn {status}")

    while True:
        choice = input("\n🔹 Nhấn 'Enter' để tiếp tục kiểm tra index hoặc nhập 'n' để thoát: ").strip().lower()
        if choice == "n":
            sys.exit("🚪 Thoát chương trình.")
        elif choice == "":
            break

show_api_status()  

# 🔹 Nhập số lớp kiểm tra
while True:
    try:
        check_layers = input("🔍 Nhập số lớp kiểm tra (1: site:url, 2: 'url' + site:url, 3: 'url' + site:url + cache) [Mặc định: 1]: ").strip()
        if check_layers == "":
            check_layers = 1
        else:
            check_layers = int(check_layers)
            if check_layers not in [1, 2, 3]:
                raise ValueError
        break
    except ValueError:
        print("⚠ Vui lòng nhập 1, 2 hoặc 3.")

# 🔹 Tìm API Key hợp lệ
def get_valid_api_key():
    global current_api_index

    while True:
        valid_api_keys = [api for api in api_keys if credits_data.get(api, 0) > 0]

        if not valid_api_keys:
            print("\n❌ Không có API Key nào còn credits! Hãy nhập API mới.")
            new_keys = input("🔑 Nhập API keys mới (cách nhau bằng dấu phẩy) hoặc bấm 'n' để thoát: ").strip()
            if new_keys.lower() == "n":
                sys.exit("🚪 Thoát chương trình.")
            else:
                new_keys_list = [key.strip() for key in new_keys.split(",")]
                api_keys.extend(new_keys_list)
                for key in new_keys_list:
                    credits_data[key] = DEFAULT_CREDITS
                save_credits()
                continue

        api_key = valid_api_keys[current_api_index % len(valid_api_keys)]
        return api_key

SERPER_API_KEY = get_valid_api_key()

# 🔹 Chuẩn hóa URL để kiểm tra chính xác hơn
def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

# 🔹 Gửi yêu cầu API Serper.dev
def search_google(query):
    global SERPER_API_KEY

    if credits_data[SERPER_API_KEY] <= 0:
        print(f"❌ API Key {SERPER_API_KEY} đã hết credits. Chuyển API...")
        SERPER_API_KEY = get_valid_api_key()

    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "gl": "VN", "hl": "vi", "num": 10}

    try:
        response = requests.post(SERPER_SEARCH_URL, json=payload, headers=headers, timeout=10)
        data = response.json()
        credits_data[SERPER_API_KEY] -= 1
        save_credits()
        return [normalize_url(result["link"]) for result in data.get("organic", [])]
    except requests.exceptions.RequestException:
        return []

# 🔹 Kiểm tra index theo số lớp đã chọn
def check_google_index(url):
    norm_url = normalize_url(url)

    if check_layers >= 2:
        query_url = f'"{url}"'
        result_url = search_google(query_url)
        if norm_url in result_url:
            return url, "Indexed"

    if check_layers >= 1:
        query_site = f"site:{url}"
        result_site = search_google(query_site)
        if norm_url in result_site:
            return url, "Indexed"

    if check_layers == 3:
        query_cache = f"cache:{url}"
        result_cache = search_google(query_cache)
        if norm_url in result_cache:
            return url, "Indexed"

    return url, "Not Indexed"

# 🔹 Chạy chương trình
try:
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(check_google_index, url): i for i, url in enumerate(urls)}

        for future in as_completed(future_to_index):
            url, status = future.result()
            results[urls[future_to_index[future]]] = status
            print(f"{future_to_index[future]+1}/{len(urls)} - {url}: {status}")

            pd.DataFrame(results.items(), columns=["URL", "Index Status"]).to_csv(RESULT_FILE, index=False)

except KeyboardInterrupt:
    print("\n⏹️ Chương trình bị dừng.")
finally:
    print(f"\n✅ Kết quả đã được lưu vào: {RESULT_FILE}")
