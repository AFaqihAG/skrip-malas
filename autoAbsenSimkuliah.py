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
NIM = "NIM"
PASS = "PASS"
MAX_WAIT_TIME = 20 # waktu tunggu maksimal dalam seconds

# Fungsi untuk mengklik elemen by CSS SELECTOR setelah menunggu
def click_by_css(css_selector, label):
    try:
        WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        ).click()
        print(f"Tombol '{label}' di klik")
    except TimeoutException:
        print(f"Tombol '{label}' tidak ditemukan atau tidak dapat diklik.")
        exit_program("Terjadi kesalahan!")

# Fungsi untuk mengisi teks pada kolom berdasarkan atribut name dan nilainya 
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

# Fungsi untuk mencetak teks dari elemen dengan selector CSS
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

# Fungsi untuk mencetak teks dari elemen dengan selector CSS
def get_text_by_css(css_selector):
    try:
        elemen = WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        text = elemen.text
        return text
    except TimeoutException:
        return None

# Fungsi untuk membuka atau pindah url baru
def go_to_url(url):
    # opening the target website in the browser 
    driver.get(url)
    #printing the target website url and title
    print(f"Membuka '{driver.current_url}' ")

# Fungsi untuk keluar program
def exit_program(message):
    print(message, "Exiting..")
    driver.close()
    exit()

# Fungsi untuk memeriksa koneksi internet
def is_internet_available(url="https://google.com"):
    try:
        # Cobalah menghubungi server Google
        response = requests.get(url, timeout=10000)
        return True
    except requests.ConnectionError:
        return False

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

if is_internet_available():
    # using Firefox headless webdriver to secure connection to Firefox 
    # with webdriver.Firefox(options=options) as driver:

    go_to_url(URL_LOGIN)  # pergi ke halaman login
    # Mengisi username, password and signin elements
    fill_text_by_name("username", NIM)
    fill_text_by_name("password", PASS)
    
    # Flow click tombol
    # Flow Login
    click_by_css(LOGIN_SELECTOR, "Login") 
    # Jika berhasil masuk
    nama = get_text_by_css(NAMA_AKUN_SELECTOR)
    if nama:
        length = 6 + len(nama)
        print("Login Berhasil!")
        print('='* math.ceil((length-6)/2) ,"INFO", '='* math.ceil((length-6)/2) )
        print("Nama:",nama)
        print("NIM:",NIM)
        print('='*(length+1))
        
        # Flow pergi ke halaman absensi 
        go_to_url(URL_ABSENSI)  # pergi ke halaman absensi
        check = get_text_by_css(CHECK_ABSEN_SELECTOR)    # Mendapatkan teks jika absen belum tersedia
        
        # Jika absen belum tersedia maka program berhenti
        if "sudah" in check.lower():
            exit_program(check)    
        else:
            mataKuliah = get_text_by_css(MK_SEKARANG_SELECTOR)     # Dapatkan mata kuliah yang sedang berlangsung
            info_absensi_check = get_text_by_css(INFO_ABSENSI_SELECTOR)  # dapatkan teks anda sudah absen atau belum

            if mataKuliah and info_absensi_check:
                print("Mata Kuliah:", mataKuliah)

                # dapatkan kata kedua yaitu belum atau sudah dari info_absensi_check
                info_c = info_absensi_check.split()
                if (info_c[1].lower() == "belum"):
                    print(info_absensi_check)
                    # click_by_css(konfirmasi_kehadiran, "konfirmasi kehadiran")
                    # click_by_css(konfirmasi, "konfirmasi absen")
                    time.sleep(3.0)
                    driver.find_element(By.CSS_SELECTOR, KONFIRMASI_KEHADIRAN_SELECTOR).click()
                    time.sleep(3.0)
                    driver.find_element(By.CSS_SELECTOR, KONFIRMASI_SELECTOR).click()

                    go_to_url(URL_ABSENSI)  # pergi ke halaman absensi
                    info_absensi_check = get_text_by_css(INFO_ABSENSI_SELECTOR)  # dapatkan teks anda sudah absen atau belum
                    info_c = info_absensi_check.split()
                    if (info_c[1].lower() == "sudah"):
                        exit_program(f"Absensi {mataKuliah}\nberhasil!")
                    else:
                        exit_program(info_absensi_check)
                # jika selain belum
                else:
                    exit_program(info_absensi_check)

            else:
                exit_program("Gagal mengindeks MK dan Info_absen")

    else:
        # Menampilkan kesalahan jika username atau pass salah
        if NIM and PASS:    
            error_alert = get_text_by_css(VALID_ALERT_SELECTOR)
            exit_program(error_alert)
        else:
            exit_program("NIM/Password kosong!")

        exit_program("Gagal login!")
else:
    gagal = "Gagal Terhubung. Coba lagi nanti."
    exit_program(gagal)
