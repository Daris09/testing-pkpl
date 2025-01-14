from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Konfigurasi logging
logging.getLogger('selenium').setLevel(logging.FATAL)

# Data pencarian untuk pengujian
search_data = [
    {"search_term": "John Carmen"},
    {"search_term": "Carmen"},
    {"search_term": "Clay"},
    {"search_term": "Clayman"},
    {"search_term": "Maou"},
    {"search_term": "Rimuru"},
    {"search_term": "Refaldi"},
]

def test_search(data):
    # Konfigurasi Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Inisialisasi driver dengan options
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Buka halaman biodata
        driver.get("http://pkpl.fwh.is/list.php")
        
        # Tunggu hingga elemen input tersedia
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.input[placeholder='Search....']")))
        
        # Masukkan data pencarian
        search_input.clear()  # Hapus nilai yang ada
        search_input.send_keys(data["search_term"])  # Masukkan kata kunci pencarian
        time.sleep(2)  # Tunggu sebentar agar filter pencarian mengupdate hasil

        # Verifikasi apakah baris data yang relevan muncul dalam tabel
        rows = driver.find_elements(By.XPATH, "//table[@class='list']//tr[@class='data']")
        found = False

        for row in rows:
            # Cek apakah nama yang dicari muncul pada kolom NAMA
            nama_cell = row.find_element(By.XPATH, "./td[2]")  # Mengakses kolom Nama di setiap baris
            if data["search_term"] in nama_cell.text:  # Cek apakah nama yang dicari ada
                found = True
                break

        if found:
            print(f"Pencarian berhasil ditemukan untuk '{data['search_term']}'")
        else:
            print(f"Pencarian tidak ditemukan untuk '{data['search_term']}'")

    except Exception as e:
        print(f"Terjadi kesalahan saat menguji pencarian '{data['search_term']}': {e}")

    finally:
        driver.quit()

# Uji setiap data pencarian
print("\nMemulai pengujian pencarian...")
print("-" * 50)
for data in search_data:
    test_search(data)
    print("-" * 50)
