from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import logging

# Konfigurasi logging
logging.getLogger('selenium').setLevel(logging.FATAL)

# Data login untuk pengujian
login_data = [
    {"email": "user@gmail.com", "password": "Admin12345"},
    {"email": "user@gmail.com", "password": "salahbro123"},
    {"email": "usesasr@gmail.com", "password": "Admin12345"},
    {"email": "", "password": ""},
    {"email": "user@gmail.com", "password": ""},
    {"email": "", "password": "Admin12345"},
]

def test_login(data):
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
        # Buka halaman login
        driver.get("http://pkpl.fwh.is/login.php")
        
        # Tunggu hingga elemen input tersedia
        username = wait.until(EC.presence_of_element_located((By.ID, "email")))
        password = wait.until(EC.presence_of_element_located((By.ID, "pass")))
        
        # Masukkan data login
        username.send_keys(data["email"])
        password.send_keys(data["password"])
        
        # Klik tombol login
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button")))
        login_button.click()
        
        # Tangani alert jika muncul
        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            
            # Pengecekan data kosong yang diperbaiki
            if data['email'] == "" and data['password'] == "":
                print(f"Login gagal dengan email: {data['email']} password: {data['password']} - Email dan Password harus diisi")
            elif data['email'] == "":
                print(f"Login gagal dengan email: {data['email']} password: {data['password']} - Email tidak boleh kosong")
            elif data['password'] == "":
                print(f"Login gagal dengan email: {data['email']} password: {data['password']}- Password tidak boleh kosong")
            else:
                print(f"Login gagal dengan email: {data['email']} password: {data['password']} - Alert message: {alert_text}")
            return False
            
        except TimeoutException:
            # Tidak ada alert, cek halaman sukses
            try:
                success_element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'PROGRAM MANAJEMEN DATA MAHASISWA')]")
                ))
                print(f"Login berhasil dengan email: {data['email']} password: {data['password']}")
                return True
            except TimeoutException:
                print(f"Login gagal dengan email: {data['email']} password: {data['password']} - Timeout menunggu halaman sukses")
                return False
                
    except Exception as e:
        print(f"Terjadi kesalahan saat menguji data {data}: {e}")
        return False
    finally:
        driver.quit()

# Uji setiap data login
print("\nMemulai pengujian login...")
print("-" * 50)
for data in login_data:
    test_login(data)
    print("-" * 50)