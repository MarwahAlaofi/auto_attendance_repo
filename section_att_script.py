
#############################
# Author: Marwah Alaofi
# Last modified: 12th of Nov 2020
#############################

from selenium import webdriver
from datetime import datetime
import pandas as pd
import time
import os
import glob
import sys

############################################
# Set the following parameters as required #
############################################

# minimum number of minutes to count the student present
MINIMUM_ACCEPTED_ATTENDANCE_DURATION = 55 # change as needed

# the threshold for high absence count
HIGH_ABSENCE_COUNT = 5 # change as needed

# Section/Course info
#####################
# a string value representing blackboard(bb) course id (i.e., section id);
# it can be taken from the url of your bb section page
#e.g. https://lms.taibahu.edu.sa/..../collabultra?course_id=[_1328373_1]
COURSE_ID = 'COURSE_ID'
# a string representing the section name as registered in the system
SECTION = 'SECTION_NAME'

# Instructor info
#####################
BB_USERNAME = 'BLACKBOARD_USERNAME'
BB_PASSWORD = 'BLACKBOARD_PASSWORD'

ES_USERNAME = 'E_ACADEMIC_SERVICES_USERNAME'
ES_PASSWORD = 'E_ACADEMIC_SERVICES_PASSWORD'

# Other data
MINUTE_ENTRY = 15 # change as needed
ARCHIVE_FOLDER_NAME = 'section_' + SECTION + '_attendance_archive' # change as needed

######### End of Parameters Section #######
###########################################

# read lecture date from terminal [today is the default]
if len(sys.argv) > 1:
    lecture_date = datetime.strptime(sys.argv[1],"%d-%m-%y").date()
else:
    lecture_date = datetime.today()



temp_directory_path = os.path.join(os.getcwd() , "atten_tmp")
path = os.path.join(temp_directory_path, r"*.csv") # temp file path
if not os.path.exists(temp_directory_path):
    os.mkdir(temp_directory_path)

# setting the browser's preferences to save to the current working directory
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : temp_directory_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)

print("Please wait .............")
print("openning blackboard ...")
driver.get('https://lms.taibahu.edu.sa')

# find the login elements
bb_cookie_accept = driver.find_element_by_xpath('//*[@id="agree_button"]')
bb_username = driver.find_element_by_xpath('//*[@id="user_id"]')
bb_password = driver.find_element_by_xpath('//*[@id="password"]')
bb_ok = driver.find_element_by_xpath('//*[@id="entry-login"]')

bb_cookie_accept.click()

print("logging into blackboard ...")

# fill in and submit login credintials
bb_username.send_keys(BB_USERNAME)
bb_password.send_keys(BB_PASSWORD)
bb_ok.click()

# go to the virtual classroom page
virtual_class_link = 'https://lms.taibahu.edu.sa/webapps/collab-ultra/tool/collabultra?course_id='+ COURSE_ID + '&mode=cpview'
driver.get(virtual_class_link)

# wait for the page to load
driver.implicitly_wait(20)

# switch to the iframe context where the dropdown button exists
frame = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(frame)

# choose session in range
driver.find_element_by_id("filter-toggle-27").click()
driver.find_element_by_xpath('//*[@id="select-range-filter-27"]/span').click()

# find date range elements
start_date = driver.find_element_by_xpath('//*[@id="startDate-27"]')
end_date = driver.find_element_by_xpath('//*[@id="endDate-27"]')

# clear the elements before entry
start_date.clear()
end_date.clear()

# fill in the range dates
start_date.send_keys(lecture_date.strftime("%m/%d/%y"))
end_date.send_keys(lecture_date.strftime("%m/%d/%y"))

session = driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/ul/li')

# click on session options button
session.find_elements_by_tag_name('button')[1].click()

#click on view report and go to view report 1s page
driver.find_element_by_xpath('//*[starts-with(@id,"session")]/ul/li[2]/button').click();

time.sleep(5)

#click on view report and go to report detailed page
driver.find_element_by_xpath('//*[starts-with(@id,"view-report")]').click();

print("downloading the csv attendance file ...")

# wait until the csv download link is clickable
time.sleep(5)

# download the csv attendance file
driver.find_element_by_xpath('//*[@id="session-report"]/div/div/div/aside/ul/li[2]/div/div/button').click()

# wait until the download is completed
#time.sleep(5)

try:
    print('openning the academic services website ...')
    driver.get('https://eas.taibahu.edu.sa/TaibahReg/teachers_login.jsp')
    username = driver.find_element_by_xpath('//*[@id="Table_01"]/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input')# removed input
    password = driver.find_element_by_xpath('//*[@id="Table_01"]/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/input')
    ok_button = driver.find_element_by_xpath('//*[@id="Table_01"]/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/form/table/tbody/tr[4]/td[2]/div/input[1]')

    print('logging into the academic services website ...')
    username.send_keys(ES_USERNAME)
    password.send_keys(ES_PASSWORD)
    ok_button.click()

    section_table_rows = driver.find_elements_by_xpath('//*[@id="Table_01"]/tbody/tr[2]/td/table/tbody/tr/td[1]/p[1]/table[2]/tbody/tr')
    for section_row in section_table_rows[1:len(section_table_rows)-1]:
        section_link = section_row.find_element_by_xpath('td[4]/a')
        if(section_link.get_attribute('innerText') == SECTION):
            section_link.click()
            break;
    #section_link = driver.find_element_by_xpath('//*[@id="Table_01"]/tbody/tr[2]/td/table/tbody/tr/td[1]/p[1]/table[2]/tbody/tr['+ str(SECTION_ROW_NO+1) +']/td[4]/a')
    #section_link.click()

    date = driver.find_element_by_xpath('//*[@id="Table_01"]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[2]/input')
    duration = driver.find_element_by_xpath('//*[@id="Table_01"]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[1]/span[1]/select')
    lecture_type = driver.find_element_by_xpath('//*[@id="Table_01"]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/select')

    print('entering lecture data ...')
    date.send_keys(lecture_date.strftime("%m/%d/%Y"))
    duration.send_keys(MINUTE_ENTRY)
    lecture_type.send_keys("محاضرة")

    # read the attendance csv file and create a dataframe
    # (Name	Username	Role	AttendeeType	First join	Last leave	Total time	Joins)
    print('reading the csv file ...')

    bb_attendance = pd.read_csv(glob.glob(path)[0])

    # delete the instructor row
    #bb_attendance.drop(bb_attendance[bb_attendance['Role'] == 'Moderator'].index, inplace = True)

    print('marking attendance ...')

    all_rows = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/table/tbody/tr')
    student_rows = all_rows[1:len(all_rows)-2] #ignoring header and footer rows (not student rows)
    confrim_checkbox = all_rows[len(all_rows)-2].find_element_by_xpath('th[1]/input') #confirm checkbox
    submit_btn = all_rows[len(all_rows)-1].find_element_by_xpath('th/input') #submit button
    absence_list = []
    student_list = []
    for row in student_rows:
      student_id = row.find_elements_by_xpath('td')[2].get_attribute('innerText')
      student_name = row.find_elements_by_xpath('td')[3].get_attribute('innerText')
      student_absence_count = int(row.find_elements_by_xpath('td')[6].get_attribute('innerText'))
      student_attendance_checkbox = row.find_element_by_xpath('td/input')

      # check the id with the bb attendance list
      student_attendance_info = bb_attendance[bb_attendance['Username'] == student_id]

      if len(student_attendance_info) > 0:
        student_attendance_duration = datetime.strptime(student_attendance_info.iloc[0]['Total time'], "%H:%M:%S")

      if len(student_attendance_info) == 0 or student_attendance_duration.hour * 60 + student_attendance_duration.minute < MINIMUM_ACCEPTED_ATTENDANCE_DURATION :
        student_absence_count += 1
        student_dic = {'id': student_id, 'name': student_name, 'absence_count':student_absence_count}
        student_list.append(student_dic)
        absence_list.append(student_dic)
        continue

      student_dic = {'id': student_id, 'name': student_name, 'absence_count':student_absence_count}
      student_list.append(student_dic)
      student_attendance_checkbox.click()

    # confirm attendance
    confrim_checkbox.click()

    # submit the form
    #submit_btn.click()

    print('\n\n ******** Attendance Marking is DONE **********')

    #print absent students
    print("-----------------------------------")
    print("---- absent student list ----------")
    for s in absence_list:
        print(s)
    print("-----------------------------------")

    #print students with high absence count
    print("---- student with denial risk -----")
    for s in student_list:
        if s['absence_count'] >= HIGH_ABSENCE_COUNT:
            print(s)
    print("-----------------------------------")

except Exception as e:
    logging.error(traceback.format_exc())

    # send notification/email if absence is more than the threshold
    ###############################################################
finally:
    # move the attendance file to the archive folder
    if not os.path.exists(ARCHIVE_FOLDER_NAME):
      os.mkdir(ARCHIVE_FOLDER_NAME)
    file_name = SECTION + '_' + lecture_date.strftime("%d-%m-%y") + '.csv'
    os.replace(glob.glob(path)[0], os.path.join(ARCHIVE_FOLDER_NAME, file_name))
    # remove the temp directory
    #os.rmdir(temp_directory_path)
    print('attendance csv file is archived at ' + os.path.join(os.getcwd(), ARCHIVE_FOLDER_NAME) + '\n')
