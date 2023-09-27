from selenium import webdriver 
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import math
import requests

# Akun USK untuk Login
NIM = 'NIM-Kamu'
PASS = 'PASS-Kamu'
MAX_WAIT_TIME = 20 # waktu tunggu maksimal dalam seconds

# Inisialisasi variabel status untuk flow dependency
status = True
# Fungsi untuk mengklik elemen by CSS SELECTOR setelah menunggu
def click_by_css(css_selector, label):
    global status # menggunakan variable status mejadi global
    try:
        WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        ).click()
        print(f"Tombol '{label}' di klik")
    except TimeoutException:
        print(f"Tombol '{label}' tidak ditemukan atau tidak dapat diklik.")
        status = False # Set status menjadi false jika tombol gagal di klik

# Fungsi untuk mengisi teks pada kolom berdasarkan atribut name dan nilainya 
def fill_text_by_name(value_of_name, text_to_fill):
    try:
        elemen = WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, value_of_name))
        )
        elemen.clear()
        elemen.send_keys(text_to_fill)
    except TimeoutException:
        print(f"Elemen dengan atribut '{atribut}'='{nilai}' tidak ditemukan atau tidak dapat diisi.")

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
def exit_program(message=""):
    print(message, "Exiting the program...")
    exit(1)

# Fungsi untuk memeriksa koneksi internet
def is_internet_available(url="https://google.com"):
    try:
        # Cobalah menghubungi server Google
        response = requests.get(url, timeout=10000)
        return True
    except requests.ConnectionError:
        return False

# the target website 
url_login = "https://simkuliah.usk.ac.id/index.php/login" 
url_absensi = "https://simkuliah.usk.ac.id/index.php/absensi"

# the interface for turning on headless mode 
options = Options() 
options.add_argument("-headless") 

# Inisialisasi Elemen
# cara : inspect element web pages, get the button or text field, right click, copy, choose css selector or xpath or whatever you want.
login = "div.row:nth-child(5) > div:nth-child(1) > button:nth-child(1)"  #css selector
# absensi = ".pcoded-item > li:nth-child(2) > a:nth-child(1) > span:nth-child(2)"   #css selector
absensi = "a[href='https://simkuliah.usk.ac.id/index.php/absensi']"
hadir = "#konfirmasi-kehadiran" #css selector
konfirmasi = ".confirm" #css selector
nama_akun = "#pcoded > div.pcoded-container.navbar-wrapper > nav > div > div.navbar-container.container-fluid > div > ul.nav-right > li.user-profile.header-notification > a > span"
check_absen = "#pcoded > div.pcoded-container.navbar-wrapper > div > div > div.pcoded-content > div > div > div > div.page-body > div > div > div > div > div:nth-child(1) > div > div > p"
valid_alert = "body > section > div > div > div > div.login-card.card-block.auth-body > form > div.auth-box > div.alert.alert-danger.icons-alert"
mk_sekarang = ""


try:
    # Check ketersediaan internet
    if is_internet_available():
        # using Firefox headless webdriver to secure connection to Firefox 
        with webdriver.Firefox(options=options) as driver:
        
            go_to_url(url_login)  # pergi ke halaman login
            # Mengisi username, password and signin elements
            fill_text_by_name("username", NIM)
            fill_text_by_name("password", PASS)
            
            # Flow click tombol
            # Flow Login
            if status:
                click_by_css(login, "Login") 
                # Jika berhasil masuk
                nama = get_text_by_css(nama_akun)
                if nama:
                    length = 6 + len(nama)
                    print("Login Berhasil!")
                    print('-'* math.ceil((length-6)/2) ,"INFO", '-'* math.ceil((length-6)/2) )
                    print("Nama:",nama)
                    print("NIM:",NIM)
                    print('-'*(length+1))
                    
                    # Flow pergi ke halaman absensi 
                    go_to_url(url_absensi)  # pergi ke halaman absensi
                    check = get_text_by_css(check_absen)    # Mendapatkan teks jika absen belum tersedia
    
                    # Jika absen belum tersedia maka program berhenti
                    if check:
                        print(check, "coba lagi nanti")
                        exit_program()    
                    else:
                        mataKuliah = get_text_by_css(mk_sekarang)     # Dapatkan mata kuliah yang sedang berlangsung
                        if mataKuliah:
                            print("Mata Kuliah:", mataKuliah)
    
                            # Flow untuk klik tombol hadir
                            # click_by_css(hadir, "Hadir")
                            # click_by_css(konfirmasi, "Konfirmasi")
    
                else:
                    # Menampilkan kesalahan jika username atau pass salah
                    if NIM and PASS:    
                        error_alert = get_text_by_css(valid_alert)
                        print(error_alert)

                    print("Gagal login, coba lagi!")
                    exit_program()
        
                driver.close()
    else:
        print("Gagal Terhubung. Coba lagi nanti.")
except WebDriverException as e:
    print("Terjadi kesalahan:", str(e))
