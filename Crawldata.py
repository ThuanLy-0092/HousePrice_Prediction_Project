import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

options = Options()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
# crawl data từ 1 link
def getPost(url):
    driver2 = webdriver.Chrome(options=options)
    driver2.get(url)
    time.sleep(4)
        
    try:
        price_tmp = driver2.find_element(By.CLASS_NAME, "meta") #Giá
        date_time = driver2.find_element(By.CLASS_NAME,"timeago") #Ngày đăng
        raw = driver2.find_elements(By.CSS_SELECTOR, "ul.uk-list li") #Dữ liệu thô chứa các list thông tin
        phone =driver2.find_element(By.CLASS_NAME,"more.phone") #Số điện thoại
        phone_num = phone.find_element(By.TAG_NAME, "a").get_attribute("href") #Số điện thoại
        description_elem = driver2.find_element(By.CLASS_NAME,"content") #Mô tả
        title_elem = driver2.find_element(By.CSS_SELECTOR,"h1.uk-panel-title") #Mô tả
        description=description_elem.text
        title=title_elem.text
        element_district = driver2.find_element(By.CSS_SELECTOR,"ul.uk-breadcrumb li:last-child") #Quận
        dis=element_district.text
        element_city= driver2.find_element(By.CSS_SELECTOR,"ul.uk-breadcrumb li:nth-child(3)") #Tỉnh/Thành phố
        city=element_city.text

        elements= []
        for element in raw:
            elements.append(element.text)

        important_info = []

        for result in elements:
            if result.startswith('Diện tích') or result.startswith('Phòng ngủ') or result.startswith('Phòng WC') or result.startswith('Mã tin'):
                match = re.search(r':\s*(\d+)', result)
                if match:
                    # Lấy số từ kết quả tìm thấy và chuyển đổi sang kiểu số nguyên
                    important_info.append(int(match.group(1)))
        n=len(important_info)                
        if (n!= 4):
            raise NoSuchElementException
        
    except NoSuchElementException:
        data_dict0 = {
        'Price': '',
        'Area': '',
        'Bedrooms': '',
        'Bathrooms': '',
        'Listing ID': '',
        'Date Posted': '',
        'Phone Number': '',
        'Address': '',
        'Title': '',
        'Amenities': '',
        'Floors': '',
        'NearSchool':'',
        'NearHospital':'',
        'Security':'',
        'legalclarity':'',
        'district':'',
        'city/province' :''
    }

        driver2.quit()
        return data_dict0
        
    full_text = f"{title}\n{description}\n Nhà này ở Quận: {dis},Tỉnh/Thành Phố: {city}"
    result = Create_More_Vars(full_text)
    if(result):
        dia_chi = result['DiaChi']
        tien_ich = result['TienIch']
        so_tang=result['SoTang']
        gan_truong=result['NearSchool']
        gan_bv=result['NearHospital']
        an_ninh=result['Security']
        legal_clarity=result['LegalClarity']
    else:
        dia_chi=''
        tien_ich=''
        so_tang=''
        gan_truong=''
        gan_bv=''
        an_ninh=''
        legal_clarity=''
          
    data_dict = {
        'Price': price_tmp.text,
        'Area': important_info[0],
        'Bedrooms': important_info[1],
        'Bathrooms': important_info[2],
        'Listing ID': important_info[3],
        'Date Posted': date_time.get_attribute("datetime"),
        'Phone Number': phone_num.replace("tel:", ""),
        'Address': dia_chi,
        'Title': title,
        'Amenities': tien_ich,
        'Floors': so_tang,
        'NearSchool':gan_truong,
        'NearHospital':gan_bv,
        'Security':an_ninh,
        'legalclarity':legal_clarity,
        'district': dis,
        'city/province' :city
    }
    
    driver2.quit()
    return data_dict

def crawlData(numPage):
    driver = webdriver.Chrome(options=options)
    if (numPage == 1):
        driver.get("https://batdongsan.vn/ban-nha"+str(''))
        time.sleep(2)
    else:
        driver.get("https://batdongsan.vn/ban-nha/p"+str(numPage))
        time.sleep(2)
    
    elems=driver.find_elements(By.CSS_SELECTOR, ".name [href]")

    urls = [elem.get_attribute('href') for elem in elems]
    urls = urls[:-5]

    with ThreadPoolExecutor(max_workers=5) as executor:
        listData = list(executor.map(getPost, urls))

    df = pd.DataFrame(listData)
        # Giả sử df là DataFrame của bạn
    df = pd.DataFrame(listData)  # Thay data bằng dữ liệu của bạn
    # Thay thế chuỗi rỗng bằng None trong cột "Title"
    df['Title'] = df['Title'].replace('', None)

    # Loại bỏ các mẫu có giá trị None trong cột "Title"s
    df = df.dropna(subset=['Title'])
    df = df.drop_duplicates(subset=['Title'])
    df.to_csv('data'+str(numPage)+'.csv', encoding='utf-8-sig')
    return df
    driver.quit()

