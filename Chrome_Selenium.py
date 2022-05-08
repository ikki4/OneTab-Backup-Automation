import time
import os
import difflib
import utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pathlib import Path
from datetime import datetime
import webbrowser
import pyautogui

EXTENSION_ID = "chphlpgkkbolifaimnlloiipkdnihall"
FILENAME = f"Onetab Backup {datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}" #backup file name 

USER_PROFILE = os.environ['USERPROFILE']
BACKUP_PATH = Path(r'.\Backups') #path to the desired backup/export folder
#change the folder path if you want to, but keep the r before the string
#example: BACKUP_PATH = Path(r'D:\Documents\Onetab Backup')
#original value: LOCAL_DESTINATION_FILE_PATH = os.path.join(USER_PROFILE, "Documents", "OneTab-Backup.txt")

CHROME_DIR = Path(USER_PROFILE, 'AppData', 'Local', 'Google', 'Chrome')
CHROME_USER_DATA_DIR = Path(CHROME_DIR, 'User Data')
DEFAULT_CHROME_USER_DATA_DIR = Path(CHROME_DIR, "User Data", "Default")

TEMP_DIR = Path(CHROME_DIR, 'temp',)
TEMP_CHROME_USER_DATA = Path(TEMP_DIR, "Default")


def check_need_to_update(filepath, latestData): 
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding="utf-8") as existingFile:
            diffResult = difflib.Differ().compare(existingFile.read(), latestData)
        # List Comprehension
        return [x for x in diffResult if x[0] in ('+', '-')]
    else:
        return True


def create_or_update_backup_file(latestData): 
    if check_need_to_update(Path(BACKUP_PATH, "OneTab Backup (latest).txt"), latestData):
        with open(Path(BACKUP_PATH, "OneTab Backup (latest).txt"), 'w', encoding="utf-8") as file:
            file.write(latestData)
        print("Backup Created/Updated")
    else:
        print("No new changes")
    os.utime(Path(BACKUP_PATH, "OneTab Backup (latest).txt")) #updates the file's access and modified times


def create_new_backup_file(latestData): #new
    '''Creates a new backup file and returns the ammount of tabs saved'''
    global FILENAME
    #creating backup folder is it doesn't exist
    if not BACKUP_PATH.is_dir():
        BACKUP_PATH.mkdir() 
    #getting number of tabs and updating FILENAME
    tabs_amount = len([line for line in latestData.split('\n') if len(line)>0])
    FILENAME += f' Tabs_{tabs_amount}.txt'
    #saving backup file
    with open(Path(BACKUP_PATH,FILENAME), mode='w', encoding='utf-8') as f:
        f.write(latestData)  
    #ending
    print(f'File "{FILENAME}" saved successfully in the directory "{str(BACKUP_PATH.resolve())}".')
    print(f'{tabs_amount} tabs were saved.')
    return tabs_amount


utils.remove_directory_if_exists(TEMP_DIR)

TEMP_LOCAL_EXTENSION_SETTINGS_EXTENSION_DIR = Path(TEMP_CHROME_USER_DATA, "Local Extension Settings", 
                                                   EXTENSION_ID)

chrome_options = ChromeOptions()
chrome_options.add_argument("user-data-dir={}".format(TEMP_DIR))
chrome_options.add_extension('./onetab.crx')

#==================== Generate a default blank profile ==============================
try:
    driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
except Exception as e:
    message="An error has occured. If this script used to work fine for you, then most likely Chrome has updated and your current chromedriver.exe is outdated. Please check your Chrome version, download the corresponding chromedriver.exe and replace the old one with the one you've downloaded." 
    button=pyautogui.confirm(text=message+'\n\nError message:\n\t'+str(e), title='Error - Onetab Backup Automation', buttons=['Download ChromeDriver', 'Quit'])
    if button=='Download ChromeDriver':
        webbrowser.open('https://chromedriver.chromium.org/downloads')
    quit()

time.sleep(1)  # Let the user actually see something!

driver.close()
driver.quit()

#===================== Copy OneTab Data =============================================
print('Start Copying OneTab Data')
utils.copy_all_files_in_directory(Path(CHROME_USER_DATA_DIR, "Default", "Local Extension Settings",
                                  EXTENSION_ID), TEMP_LOCAL_EXTENSION_SETTINGS_EXTENSION_DIR, ["LOCK"])
print('Complete Copied')

#===================== Backup OneTab Data =============================================
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

driver.get("chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/import-export.html")

time.sleep(1)  # Let the user actually see something!

contentArea = driver.find_element_by_id("contentAreaDiv")
export_box = driver.find_elements_by_tag_name("textarea")[1]

text = export_box.get_attribute("value")

create_or_update_backup_file(text)
tabs_amount = create_new_backup_file(text)
utils.remove_oldest_files_in_directory(BACKUP_PATH)

driver.close()
driver.quit()

utils.remove_directory_if_exists(TEMP_DIR)
