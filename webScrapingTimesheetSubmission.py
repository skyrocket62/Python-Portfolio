# WRITTEN BY REMINGTON PONCE (FEBRUARY 2022).
# BUILT FOR MYSELF BY MY OWN PASSION FOR PYTHON AND TO AUTOMATE TIMESHEET SUBMISSION
# THIS IS A FUNCTIONAL PROGRAM TO TAKE TIMESHEET DATA (CLOCK IN/OUT AND LUNCH IN/OUT TIMES) AND FILL THEM INTO THE CORRESPONDING FIELDS OF A TIMESHEET FORM (CORRECT DAY AND WHETHER IN/OUT)

import string
import time
from selenium import webdriver

web = webdriver.Chrome("/Users/remingtonponce/PyCharmProjects/timesheetWebAutomation/chromedriver")
web.get('https://myhr.fiu.edu/psc/hcm/EMPLOYEE/HRMS/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=HC_TIME&AJAXTransfer=Y&PanelCollapsible=Y&ICMDListSlideout=true&PTPPB_GROUPLET_ID=TL_TIME_ESS&CRefName=HC_NAVCOLL_7')  # navigate to this URL


rawTimesheetData = open("Timesheet - Remington Ponce - Feb 19 - Mar 4, 2022.csv", 'r', encoding = 'utf-8')  # find this csv timesheet data file. Be sure to  change name accordingly for each pay period
header = rawTimesheetData.readline()    # remove header

shiftStart = [ ]
lunchStart = [ ]
lunchEnd = [ ]
shiftEnd = [ ]  # initialize time data lists

for line in rawTimesheetData:
    row = line.split(',')
    shiftStart.append(row[2])
    lunchStart.append(row[3])
    lunchEnd.append(row[4])
    shiftEnd.append(row[5]) # populate time data lists

rawTimesheetData.close()    # close csv timesheet data file

# print(shiftStart)
# print(lunchStart)
# print(lunchEnd)
# print(shiftEnd)   # verify


bad = ": M" # characters in the above data that the form does not accept (so needs to be removed)


for index in range(len(shiftStart)):
    for character in bad:
        shiftStart[index] = shiftStart[index].replace(character, '')    # strip bad characters

for index in range(len(shiftStart)):
    if (len(shiftStart[index]) < 5) and (len(shiftStart[index]) != 0):  # if time format is not already 4 numbers before the "a" or "p" AND if the data isn't blank
        shiftStart[index] = "0" + shiftStart[index] # prepend a zero (form requires this)

# print(shiftStart) # verify

for index in range(len(lunchStart)):
    for character in bad:
        lunchStart[index] = lunchStart[index].replace(character, '')    # strip bad characters

for index in range(len(lunchStart)):
    if (len(lunchStart[index]) < 5) and (len(lunchStart[index]) != 0):  # if time format is not already 4 numbers before the "a" or "p" AND if the data isn't blank
        lunchStart[index] = "0" + lunchStart[index] # prepend a zero (form requires this)
    # elif len(lunchStart[index]) == 0: # if there is no lunch data
    #     lunchStart[index] = "1200P"   # put a default so Dulbys doesn't get mad and so I lose money

# print(lunchStart) # verify

for index in range(len(lunchEnd)):
    for character in bad:
        lunchEnd[index] = lunchEnd[index].replace(character, '')    # strip bad characters

for index in range(len(lunchEnd)):
    if (len(lunchEnd[index]) < 5) and (len(lunchEnd[index]) != 0):  # if time format is not already 4 numbers before the "a" or "p" AND if the data isn't blank
        lunchEnd[index] = "0" + lunchEnd[index] # prepend a zero (form requires this)
    # elif len(lunchEnd[index]) == 0:   # if there is no lunch data
    #     lunchEnd[index] = "1230P" # put a default so Dulbys doesn't get mad and so I lose money

# print(lunchEnd)   # verify

for index in range(len(shiftEnd)):
    for character in bad:
        shiftEnd[index] = shiftEnd[index].replace(character, '')    # strip bad characters

for index in range(len(shiftEnd)):
    if (len(shiftEnd[index]) < 5) and (len(shiftEnd[index]) != 0):  # if time format is not already 4 numbers before the "a" or "p" AND if the data isn't blank
        shiftEnd[index] = "0" + shiftEnd[index] # prepend a zero (form requires this)

# print(shiftEnd)   # verify


# print(shiftStart)
# print(lunchStart)
# print(lunchEnd)
# print(shiftEnd)   # verify

assert len(shiftStart) == len(lunchStart) == len(lunchEnd) == len(shiftEnd), "Unequal indices in one or more lists."    # make sure that each list is equally long

table = [ ]
for r in range(len(shiftStart)):    # since we made sure above that all lists are the same length, I just picked the first list for the len() function argument
    table.append([shiftStart[r], lunchStart[r], lunchEnd[r], shiftEnd[r]])  # populate a table of the left to right, row by row time data

# print(table)  # verify


ss = [''] * 14
ls = [''] * 14
le = [''] * 14
se = [''] * 14  # initialize xpath data lists

accumulator1 = -1
for cell in range(len(ss)):
    accumulator1 = accumulator1 + 1
    accumulator1 = str(accumulator1)
    ss[cell] = '//*[@id="PUNCH_TIME_1$' + accumulator1 + '"]'
    accumulator1 = int(accumulator1)    # generate the xpath for each row of the shift start time column (had to figure this shit out manually from inspecting the site's elements)

accumulator1 = -1
for cell in range(len(ls)):
    accumulator1 = accumulator1 + 1
    accumulator1 = str(accumulator1)
    ls[cell] = '//*[@id="PUNCH_TIME_2$' + accumulator1 + '"]'
    accumulator1 = int(accumulator1)    # generate the xpath for each row of the lunch start time column

accumulator1 = -1
for cell in range(len(le)):
    accumulator1 = accumulator1 + 1
    accumulator1 = str(accumulator1)
    le[cell] = '//*[@id="PUNCH_TIME_3$' + accumulator1 + '"]'
    accumulator1 = int(accumulator1)    # generate the xpath for each row of the lunch end time column

accumulator1 = -1
for cell in range(len(se)):
    accumulator1 = accumulator1 + 1
    accumulator1 = str(accumulator1)
    se[cell] = '//*[@id="PUNCH_TIME_4$' + accumulator1 + '"]'
    accumulator1 = int(accumulator1)    # generate the xpath for each row of the shift end time column

# print(ss)
# print(ls)
# print(le)
# print(se) # verify

table2 = [ ]
for r in range(14):
    table2.append([ss[r], ls[r], le[r], se[r]])  # populate a table of the left to right, row by row xpath 'addresses'

# print(table2)  # verify

# print(table)
# print(table2) # see both beautiful tables with their matching row,column values

value = 0
input = 0   # initialize these soon-to-be dynamic variables to serve the purpose of filling in the form fields

daySpan = list(range(2, 7)) # first set of weekdays (monday to friday)
daySpan.extend(list(range(9, 14))) # second set of weekdays (monday to friday). This defines which days of the week to use from the full 14-day, in order (Sat(0),Sun(1),Mon(2),Tue (3),Wed(4),Thu(5),Fri(6),Sat(7),Sun(8),Mon(9),Tue(10),Wed(11),Thu(12),Fri(13)) xpath data (table2)
# print(daySpan)    # verify

time.sleep(25)  # delay data entry execution to allow time for you to log in/the site to load
web.switch_to.frame(web.find_element_by_xpath('//*[@id="main_target_win0"]'))   # switch element frame in focus
count = -1  # initializing a variable for use to iterate over the time data table (table)
for r in daySpan:   # for each day in your custom list of indices from the 14-day xpath list (table2)
    count = count + 1   # increment the iterating variable for use with the time data list indices (table)
    for c in range(4):  # for each time type/column (shift start, lunch start, lunch end, shift end)
        value = table[count][c] # load the time
        input = table2[r][c]    # load the corresponding xpath
        Input = web.find_element_by_xpath(input)    # link the xpath
        Input.send_keys(value)  # type the time at that xpath

print('System: ' + 'Enjoy, sir :D')
