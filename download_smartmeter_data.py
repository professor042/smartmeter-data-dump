import os, shutil
from selenium import webdriver
from datetime import datetime, timedelta, date
#import datetime #not sure wtf the problem is with these imports, seem to need both

# Log into Firefox and export file
#   Automatically goes to Downloads folder
#   Does not allow automatic login with password for some reason

browser = webdriver.Firefox()

browser.get('http://smartmetertexas.com')
browser.find_element_by_id('username').send_keys('wbplayer042')
browser.find_element_by_id('txtPassword').send_keys('wbplayer069')

#usernameElem = browser.find_element_by_id('username')
#usernameElem.send_keys('wbplayer042')

#passwordElem = browser.find_element_by_id('txtPassword')
#passwordElem.send_keys('wbplayer069')

#passwordElem.submit()


# check dates - data should be from previous day
startdate_str = browser.find_element_by_name('viewUsage_startDate').get_attribute('value')
startdt = datetime.strptime(startdate_str, "%m/%d/%Y")
enddate_str = browser.find_element_by_name('viewUsage_endDate').get_attribute('value')
enddt = datetime.strptime(enddate_str, "%m/%d/%Y")
import datetime #not sure wtf the problem is with these imports, seem to need this
todayd = datetime.date.today()
todaysdt = datetime.datetime(todayd.year, todayd.month, todayd.day)
yesterdaysdt = todaysdt - timedelta(days=1)

if startdt != enddt:
	print("start_date (" + startdate_str + ") != end_date (" + enddate_str +")")
	print("Program terminated.")
	
if startdt != yesterdaysdt:
	print("start_date (" + startdate_str + ") is not yesterday.")
	print("Program terminated.")
	
browser.find_element_by_name('tag_dp_export').click()
#exportButton = browser.find_element_by_name('tag_dp_export')
#exportButton.click()

# Copy file from source to backup folder for history
#    Assumes newest file is correct one to transfer
source_path = 'C:\\Users\\JLZ\\Downloads\\FireFox_Downloads\\'
backup_path = 'C:\\Users\\JLZ\\Documents\\Electricity Data\\Raw Data\\'
active_path = 'C:\\Users\\JLZ\\Documents\\Electricity Data\\Current File\\'

os.chdir(source_path)

newest_filename = max([f for f in os.listdir('.') if f.lower().endswith('.csv')], key=os.path.getctime)

source_full_filename = source_path + newest_filename

#yesterdaydt_str = yesterdaysdt.strftime('%Y-%m-%d')
backup_full_filename = backup_path + newest_filename.replace('.csv', '')
backup_full_filename += '-' + yesterdaysdt.strftime('%Y-%m-%d') + '.csv'

shutil.copy(source_full_filename, backup_full_filename)

# Copy current file from history folder to active folder for Excel usage
#     Current file in this folder can be deleted/overwritten

active_filename = 'IntervalUsage60343509_current.csv'

active_full_filename = active_path + active_filename

shutil.copy(backup_full_filename, active_full_filename)
