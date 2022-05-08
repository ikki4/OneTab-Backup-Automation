### Changes from the [original project](https://github.com/busyxiang/OneTab-Backup-Automation):

* Requires Python 3.6+
* **(new) Requires [pyautogui](https://pyautogui.readthedocs.io/en/latest/)**
  * Now the script notifies you when Chomedriver needs to be updated.
* Changed how the backup text file is made. It still updates the file `OneTab Backup (latest).txt` every time the script runs, but now a new backup file `OneTab Backup {date} {number_of_tabs}.txt` will also be created every time the script runs. This way, in case the script malfunctions or in case Chrome/OneTab crashes/updates and loses the current tab data, even if the script runs and `OneTab Backup (latest).txt` loses its data (by replacing its contents with a blank value), you'll have other saved backups to choose from.
  *   If you want to change the backup folder, open `Chrome_Selenium.py` in a text editor or IDE and edit the variable `BACKUP_PATH` (line 14).
  *   Currently the script keeps only the latest 30 backup files (the older ones get replaced by new ones). If you want to change this amount, open `utils.py` in a text editor or IDE and edit the variable `files_to_keep` (line 43).
* Changed most of the `os.path.join()` to `Path` (after importing Path from pathlib). It's another thing to import, but it provides better readability, and Path objects are usually a better solution.
  * I intend to eventually replace everything I can from `os` to `Path` (but I'm not in a hurry).


### Original project description:

---

# OneTab-Backup-Automation

The is **Python** automation script to backup your **OneTab** data

## Pre-requisite

- Python
- Selenium
- Windows & TaskScheduler (Not sure how other OS do it)

## Upcoming

I will work on this features when I feels like it and have time to do so

- [] Upload the backup file to your Google Drive
- [] User Input(Local/GoogleDrive)

## Notes

Took me a lot of time to figure out **OneTab** data is stored in the **Local Extension Settings** folder
