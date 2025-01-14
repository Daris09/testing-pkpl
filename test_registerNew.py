from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import logging
import re

# Konfigurasi logging
logging.getLogger('selenium').setLevel(logging.FATAL)

# Data registrasi untuk pengujian
register_data = [
    {"email": "user13@test.com", "password": "Has7r5s1", "password1": "Has7r5s1"},
    {"email": "user1@test.com", "password": "Test12345", "password1": "Test12345"},
    {"email": "user22@test.com", "password": "", "password1": "Different123"},
    {"email": "", "password": "Different123", "password1": "Different123"},
    {"email": "user22@test.com", "password": "Different123", "password1": ""},
    {"email": "user22@test.com", "password": "", "password1": ""},
    {"email": "", "password": "", "password1": ""},
    {"email": "user22@test.com", "password": "halo", "password1": "halo"},
    {"email": "user22@test.com", "password": "12345678", "password1": "12345678"},
    {"email": "user22@test.com", "password": "ABCDEFGH", "password1": "ABCDEFGH"},
    {"email": "user22@test.com", "password": "ABC12345", "password1": "ABC12345"},
    {"email": "user22@test.com", "password": "abcdefgh", "password1": "abcdefgh"},
    {"email": "user22@test.com", "password": "Test12345", "password1": "tesT23142"},
]

def validate_registration_data(data):
    """
    Memvalidasi data registrasi sebelum mengirim ke form
    """
    errors = []
    
    # Validasi email
    if not data["email"]:
        errors.append("Email tidak boleh kosong")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        errors.append("Format email tidak valid")
    
    # Validasi password
    if not data["password"]:
        errors.append("Password tidak boleh kosong")
    elif len(data["password"]) < 8:
        errors.append("Password minimal 8 karakter")
    
    # Validasi konfirmasi password
    if not data["password1"]:
        errors.append("Konfirmasi password tidak boleh kosong")
    elif data["password"] != data["password1"]:
        errors.append("Password dan konfirmasi password tidak sama")
    
    # Validasi kompleksitas password jika password tidak kosong
    if data["password"]:
        if not any(c.isupper() for c in data["password"]):
            errors.append("Password harus mengandung huruf kapital")
        if not any(c.islower() for c in data["password"]):
            errors.append("Password harus mengandung huruf kecil")
        if not any(c.isdigit() for c in data["password"]):
            errors.append("Password harus mengandung angka")
    
    return errors

def test_register(data):
    # Validasi data terlebih dahulu
    validation_errors = validate_registration_data(data)
    if validation_errors:
        print(f"\nTest case dengan data:")
        print(f"Email: {data['email']}")
        print(f"Password: {data['password']}")
        print(f"Konfirmasi Password: {data['password1']}")
        print("Gagal validasi dengan error:")
        for error in validation_errors:
            print(f"- {error}")
        return False

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
        # Buka halaman registrasi
        driver.get("http://pkpl.fwh.is/register.php")
        
        # Tunggu hingga elemen input tersedia
        username = wait.until(EC.presence_of_element_located((By.ID, "email")))
        password = wait.until(EC.presence_of_element_located((By.ID, "pass")))
        password1 = wait.until(EC.presence_of_element_located((By.ID, "pass1")))
        
        # Masukkan data registrasi
        username.send_keys(data["email"])
        password.send_keys(data["password"])
        password1.send_keys(data["password1"])
        
        # Klik tombol register
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button")))
        register_button.click()
        
        print(f"\nTest case dengan data:")
        print(f"Email: {data['email']}")
        print(f"Password: {data['password']}")
        print(f"Konfirmasi Password: {data['password1']}")
        
        # Tangani alert jika muncul
        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            
            # Cek apakah pesan alert mengindikasikan keberhasilan
            if "berhasil" in alert_text.lower():
                print(f"Status: Berhasil - {alert_text}")
                return True
            else:
                print(f"Status: Gagal - {alert_text}")
                return False
                
        except TimeoutException:
            # Tidak ada alert, cek apakah ada pesan error di halaman
            try:
                error_element = driver.find_element(By.CLASS_NAME, "error-message")
                print(f"Status: Gagal - {error_element.text}")
                return False
            except:
                # Jika tidak ada pesan error, anggap berhasil
                print("Status: Berhasil - Tidak ada pesan error")
                return True
                
    except Exception as e:
        print(f"Status: Error - {str(e)}")
        return False
    finally:
        driver.quit()

def run_tests():
    print("=== Memulai pengujian registrasi ===\n")
    total_tests = len(register_data)
    successful_tests = 0
    
    for i, data in enumerate(register_data, 1):
        print(f"Test case {i} dari {total_tests}")
        if test_register(data):
            successful_tests += 1
        print("-" * 50)
    
    print("\n=== Hasil pengujian ===")
    print(f"Total test case: {total_tests}")
    print(f"Berhasil: {successful_tests}")
    print(f"Gagal: {total_tests - successful_tests}")

if __name__ == "__main__":
    run_tests()