from selenium import webdriver 
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import requests
import time

# Akun USK untuk Login
NIM = "0000"
PASS = "0000"
MAX_WAIT_TIME = 20 # waktu tunggu maksimal dalam seconds

# the target website 
URL_LOGIN = "https://simkuliah.usk.ac.id/index.php/login" 
URL_ABSENSI = "https://simkuliah.usk.ac.id/index.php/absensi"

# the interface for turning on headless mode 
options = Options() 
options.add_argument("-headless") 
driver = webdriver.Firefox(options=options)

# Inisialisasi Elemen
# cara : inspect element web pages, get the button or text field, right click, copy, choose css selector or xpath or whatever you want.
LOGIN_SELECTOR = "div.row:nth-child(5) > div:nth-child(1) > button:nth-child(1)" 
KONFIRMASI_KEHADIRAN_SELECTOR = "#konfirmasi-kehadiran"
KONFIRMASI_SELECTOR = "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"
NAMA_AKUN_SELECTOR = "#pcoded > div.pcoded-container.navbar-wrapper > nav > div > div.navbar-container.container-fluid > div > ul.nav-right > li.user-profile.header-notification > a > span"
CHECK_ABSEN_SELECTOR = "#pcoded > div.pcoded-container.navbar-wrapper > div > div > div.pcoded-content > div > div > div > div.page-body > div > div > div > div > div:nth-child(1) > div > div > p"
VALID_ALERT_SELECTOR = "body > section > div > div > div > div.login-card.card-block.auth-body > form > div.auth-box > div.alert.alert-danger.icons-alert"
MK_SEKARANG_SELECTOR = "#pcoded > div.pcoded-container.navbar-wrapper > div > div > div.pcoded-content > div > div > div > div.page-body > div > div > div > div.card-header > h5"
INFO_ABSENSI_SELECTOR = "#pcoded > div.pcoded-container.navbar-wrapper > div > div > div.pcoded-content > div > div > div > div.page-body > div > div > div > div.card-block > div > div:nth-child(1) > div > p"

def click_by_css(css_selector, label):
    try:
        WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        ).click()
        print(f"Tombol '{label}' di klik")
    except TimeoutException:
        print(f"Tombol '{label}' tidak ditemukan atau tidak dapat diklik.")
        exit_program("Terjadi kesalahan!")

def fill_text_by_name(value_of_name, text_to_fill):
    try:
        elemen = WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, value_of_name))
        )
        elemen.clear()
        elemen.send_keys(text_to_fill)
    except TimeoutException:
        print(f"Elemen dengan atribut 'NAME'='{value_of_name}' tidak ditemukan atau tidak dapat diisi.")
        exit_program("Terjadi kesalahan!")

def print_text_by_css(css_selector, message=""):
    try:
        elemen = WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        teks_elemen = elemen.text
        print(f"{message}{teks_elemen}")
    except TimeoutException:
        print(f"'{css_selector}' tidak ditemukan.")
        exit_program("Terjadi kesalahan!")

def get_text_by_css(css_selector):
    try:
        elemen = WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        text = elemen.text
        return text
    except TimeoutException:
        return None

def go_to_url(url): 
    driver.get(url)
    print(f"Membuka '{driver.current_url}' ")

def exit_program(message):
    print(message, "Exiting..")
    driver.close()
    exit()

def is_internet_available(url="https://google.com"):
    try:
        response = requests.get(url, timeout=10000)
        return True
    except requests.ConnectionError:
        return False
    
def print_login_info(nama, NIM):
    length = 6 + len(nama)
    print("Login Berhasil!")
    print('=' * math.ceil((length - 6) / 2), "INFO", '=' * math.ceil((length - 6) / 2))
    print("Nama:", nama)
    print("NIM:", NIM)
    print('=' * (length + 1))

def check_sudah_absensi(info_check, mataKuliah): 
    if (info_check == "sudah"):
        exit_program(f"Absensi {mataKuliah} berhasil!")
    else:
        exit_program(f"Absensi {mataKuliah} tidak berhasil")

def login_and_get_nama(username, password):
    go_to_url(URL_LOGIN)
    fill_text_by_name("username", username)
    fill_text_by_name("password", password)
    click_by_css(LOGIN_SELECTOR, "Login")
    nama = get_text_by_css(NAMA_AKUN_SELECTOR)
    return nama

def handle_absensi():
    go_to_url(URL_ABSENSI)
    check_absen = get_text_by_css(CHECK_ABSEN_SELECTOR)
    
    if "sudah" in check_absen.lower():
        exit_program(check_absen)    
    else:
        mata_kuliah = get_text_by_css(MK_SEKARANG_SELECTOR)
        info_absensi_check = get_text_by_css(INFO_ABSENSI_SELECTOR)

        if mata_kuliah:
            print("Mata Kuliah:", mata_kuliah)

            info_check = info_absensi_check.split()
            if info_check[1].lower() == "belum":
                print(info_absensi_check)
                confirm_attendance(mata_kuliah)
            else:
                exit_program(info_absensi_check)
        else:
            exit_program(info_absensi_check)

def confirm_attendance(mata_kuliah):
    time.sleep(3.0)
    driver.find_element(By.CSS_SELECTOR, KONFIRMASI_KEHADIRAN_SELECTOR).click()
    time.sleep(3.0)
    driver.find_element(By.CSS_SELECTOR, KONFIRMASI_SELECTOR).click()

    go_to_url(URL_ABSENSI)
    info_absensi_check = get_text_by_css(INFO_ABSENSI_SELECTOR)
    info_check = info_absensi_check.split()

    check_sudah_absensi(info_check[1].lower(), mata_kuliah)

def main():
    if is_internet_available():
        nama = login_and_get_nama(NIM, PASS)
        if nama is not None:
            print_login_info(nama, NIM)
            handle_absensi()
        else:
            exit_program("Gagal login!, Periksa NIM/Password!")
    else:
        gagal = "Gagal Terhubung. Coba lagi nanti."
        exit_program(gagal)

main()
