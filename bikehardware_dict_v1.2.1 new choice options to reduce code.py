
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bicycle Hardware Database using two dictionaries saved to a single JSON file. One dictionary 'bike' holds 
bike specific hardware such as Bottom Bracket, Headset etc. The other 'wheels' holds cassette changes
for the wheels.
The app will create the dictionaries on first or subsequent runs with 2 dummy data entries.
Work to do:
    - Update the maintenance function 
    - Provide a first run option to create the keys specific to the user.
    - Provide an analysis function to show rate of change for specific items and update to include 
      specific manufacturers of the hardware to so if there is a correlation for manufacturer and usable life
    
"""

from datetime import datetime, timedelta
import json
from tabulate import tabulate
import os
import regex as re

#Colour code definitions for fancy_print command
CRED = '\033[31;1m'
CGRE = '\033[32;1m'
CMAG = '\033[36m'
CBRT = '\033[1m'

CEND = '\033[0m'

def wheel_table():
    """Creates the full wheel history table and calls the fancy_print() to print it"""
    
    temp = []
    for k, v in wheel.items():
        temp.append([k, v])
    title = (['Wheel', 'Date History'])
    fancy_print(temp, title)
    return()


def bike_table():
    """Creates the full bike hardware history table and calls the fancy_print() to print it"""
    
    temp = []
    for k, v in bike.items(): 
        for ki, vi in v.items():
            temp.append([k, ki, vi])
    title = (['Bike', 'Hardware', 'Date History'])
    fancy_print(temp, title)    
    return()


def dynamicMenu(target):
    """Creates the dynamic menu elements accomadating the addition and removal of bikes or wheels. It adds
    the Full History and new bikes and wheels options as these can not be derived from the existing
    dictionary keys. """
    
    itemList = list(target.keys())
    ilist_len = len(itemList) 
    inc = 1
    for b in itemList:
        print(f'{ilist_len - (ilist_len-inc)}- {itemList[(inc-1)]} ')
        inc = inc +1
    if target == wheel:
        prompt = 'Full wheel history'
        prompt2 = 'Add new wheel'
        itemList.append(prompt)
        itemList.append(prompt2)
    elif target == bike:
        prompt2 = 'Add new bike'
        prompt = 'Full bike history'
        itemList.append(prompt)
        itemList.append(prompt2)
    print(CMAG + f'{ilist_len+1}- '+  prompt + CEND)  
    print(CMAG + f'{ilist_len+2}- '+  prompt2 + CEND)
    options = itemList
    choicex = input(CGRE + f'\nSelect number of option required {list(range(1,(ilist_len+3)))}  :  '+ CEND)
    if choicex == 'x':
        main(bike, wheel)
    choice = int(choicex)
    choice = choice -1
    choice = itemList[choice]
    print('\n\n')
    return(choice, options)


def fancy_print(temp, title): # Works
    """Provides the table printing for all entry confirmation and status requests and called from 
    wheel and bike table functions"""

    table = tabulate(temp, tablefmt="fancy_grid", headers = title)
    print(table)
    return()


def dict_populate(item):
    """Used to add elements to the existing dictionaries or adds the hardware elements to the bike 
    dictionary if the apps is starting from scratch. Currently the hardware elements that are automatically
    added for each new bike consist of Headset, BottomBracket, Chainset, Chain and cables. Further work 
    can look at adding to these or improving resolution, for example tracking specific cable histories
     """
    hardwareItems = {'Headset': [], 'BottomBracket': [],'Chainset': [], 'Chain': [], 'Cables': []}
    if item == bike:
        if bool(bike):  
            while True:
                temp = input(CGRE + '\n Please enter new BIKE to be added to the database........   ' + CEND)
                print('\nEnter "x" to exit')
                if len(temp) != 1:
                    active = True
                    date = user_choice('date', active)
                    isValidDate = date_validate(date)
                    if isValidDate:
                        bike[temp] = hardwareItems
                        return(bike)
                else:
                    main(bike, wheel)
            bike_table()
        else:
            while True:
                temp = input('\n Please enter BIKE or BIKES to be recorded to the database........   ')
                print('\nEnter "x" to exit')
                if len(temp) != 1:
                    bike[temp] = hardwareItems    
                else:
                    main(bike, wheel)
            bike_table()
            return(bike)


    elif item == wheel:
        if bool(wheel):
            while True:
                temp = input(CGRE + 
                    '\n\nEnter new WHEELS details........  '  + CEND)
                print('\nEnter "x" to exit')
                if len(temp) != 1:
                    active = True
                    date = user_choice('date', active)
                    isValidDate = date_validate(date)
                    if isValidDate:
                        wheel[temp] = list()
                        wheel[temp].append(date)
                        wheel_table()
                        return(user_choice('initial', True))
                else:
                    main(bike, wheel)
            wheel_table()        
            return(wheel)
        

def open_file(path, file):   # Works
    """ The function imports the existing data file. 
    If no file exists it is created and the two dicts are created as empty dictionaries. In the case
    of the new bike, the dict_populate() is called to added the nested dictionary of hardware elements"""

    if os.path.exists(path+file):
        with open(path+file, 'r') as x:
            temp = str(x)
            temp = json.load(x)
        print(CMAG + '\nExisting ' + file + ' file imported.\n ' + CEND )
        return(temp[0], temp[1])  
    else:
        print('Does not exist')
        date = datetime.now()
        bike = dict()
        wheel = dict()
        dateString = date.date().strftime("%d/%m/%y")
        bike = dict_populate(bike)
        wheel = dict_populate(wheel)
        print('The file has been created ' + dateString)
        return(bike, wheel)
 

def dummy_fill_bike(bike): # Works
    """Provides and automated mechanism to add some initial data points to check functionality. It is
    likely this will be reemoved in the final release, or possibly offered as an initial option
    to the user when first run to generate initial verification entries. It is likely a similar feature
    will be added to remove these later if the user so requires."""
    
    for k,v in bike.items():
        for k1, v1 in v.items():
            bike[k][k1].append('1/1/2000')
            bike[k][k1].append('2/1/2000')
    return(bike)

def dummy_fill_wheel(wheel): #works
    """Provides and automated mechanism to add some initial data points to check functionality. It is
    likely this will be reemoved in the final release, or possibly offered as an initial option
    to the user when first run to generate initial verification entries. It is likely a similar feature
    will be added to remove these later if the user so requires."""
    
    for k,v in wheel.items():
        wheel[k].append('1/1/2000') 
        wheel[k].append('1/1/2000')
    return(wheel)
               

#Data handling function definitions

def check_age(ageCheck, queryType): #  Works
    """Checks on dictionary entries on each execution and flags hardware that has not been changed in 720 days.
    The current dayCount is defined for all hardware elements however this could be changed to accomadate
    the differing wear seen by different elements. For example cassettes wear faster than chains and both
    faster than Chainsets  (generally)"""
    
    a = True
    dayCount =100   #Change daycount to set alarm threshold. Option to add wheel or bike specific
    if ageCheck == wheel:
        for k,v in ageCheck.items():
            if datetime.now().date() > (datetime.strptime(v[-1], '%d/%m/%Y').date() + timedelta(days = dayCount)):
                print(CRED + f'The {k} has been used for greater than {dayCount} days, please check it ' + CEND)
                a = False
            else:
                continue
    elif ageCheck == bike:
        for k,v in ageCheck.items():
            for x, y in v.items():
                if datetime.now().date() > (datetime.strptime(y[-1], '%d/%m/%Y').date() + timedelta(days = dayCount)):
                    print(CRED + f'The {k} {x} has been used for greater than {dayCount} days, please check it ' + CEND)
                    a = False
                else:
                    continue            
    if a == True:
        print(f'\nNo time alarms found for your {queryType}.\n')
    return()

def user_choice(choice_type, active): # Works
    """Function to offer a central function call  to generate choices and present these to the user. The 
    menu choice is based on the type variable choice_type. This may be 'initial' for the initial menu
    'bik', for bike, 'whe', for wheel, 'hw_update' for updates to the hardware database or 'date'. 
    For date the function also confirms the date entry isa cvalid format using a regex.        """
    choice = '' 

    if choice_type == 'initial':  
        while choice not in ['1','2','3', '4', '5']:
            try:    
                print(CBRT + '\n1-  Wheel- Cassette Record -', CEND + CMAG + 'Add wheel' + CEND, '\n2-  Specific bike history -', CMAG + ' Add new bike  ' + CEND, '\n3-  Update hardware record  \n4-  All hardware & wheel status  \n5-  Exit programme') 
                choice = input(CGRE + '\nPlease enter your interaction type as shown above - use number:  ' + CEND)
                if choice not in ['1', '2', '3', '4', '5', 'x']:
                    print(CRED + '\nSorry, that is an invalide choice.\n Please enter 1, 2, 3, 4 or 5 '+  CEND)
                else:
                    return(choice)
            except ValueError:
                print(CRED + '\nSorry, that is an invalide choice.\n Please enter 1, 2, 3, 4 or 5 ' + CEND)           
        return(choice)  
    elif choice_type == 'whe':
        choice, options = dynamicMenu(wheel)
        while choice not in options:
            try:    
                if choice not in options: 
                    print(CRED + 'f\nSorry, that is an invalide choice.\n Please enter {options}' + CEND)
                elif choice == options[-1]:
                    wheel_table()
                elif choice == options[-2]:
                    dict_populate(wheel)
                else:
                    print('This is choice returned ' , choice)
                    return(choice, options)
            except ValueError:
                print(CRED + f'\nSorry, that is an invalid choice.\n Please enter{options} ' + CEND)           
        return(choice, options)
    elif choice_type =='bik':
        choice, options = dynamicMenu(bike)
        while choice not in options:
            try:   
                if choice not in options:
                    print(CRED + f'\nSorry, that is an invalid choice.\n Please enter {options}' + CEND)
                #elif choice  == 'x':
                        #return(user_choice('bik', False))
                elif choice == options[-1]:
                        bike_table()
                elif choice == options[-2]:
                        dict_populate(bike)
                else:
                    print('This is choice returned ' , choice)
                    return(choice, options)
            except ValueError:
                print(CRED + f'\nSorry, that is an invalide choice.\n Please enter {options}' + CEND)           
        return(choice, options)
    elif choice_type == 'hw_update':
        while choice not in ['1','2','3','4','5', 'x']:
            try:    
                print('\n1- Headset \n2- Bottom Bracket \n3- Chainset \n4- Chain \n5- Cables')    
                choice = input('\nPlease enter 1, 2, 3, 4, or 5 for your hardware choice :  ')
                if choice not in ['1', '2', '3', '4', '5', 'x']:
                    print(CRED + '\nSorry, that is an invalide choice.\n Please enter 1, 2, 3, 4  or 5 ' + CEND)
                else:
                    if choice  == 'x':
                        return(user_choice('whe', True))
                    else:
                     return(choice)
            except ValueError:
                print(CRED + '\nSorry, that is an invalide choice.\n Please enter 1, 2, 3, 4 or 5' + CEND)           
        return(choice)
    elif choice_type == 'date':
        r = re.compile('^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$')
        try:
            date = input(CGRE + '\nEnter date of new hardware, wheel.  dd/mm/yyyy: ' + CEND)
            if re.findall(r, date):
                return(date)
        except ValueError:
            print(CRED + '\nSorry, that date entry does not use the dd/mm/yyyy format. ' + CEND)
 
              
def close_file(path, file, all_dic):  # Works
    """Write data to JSON file on closing and return "File Saved" confirmation"""
    
    json.dump(all_dic, open(path+file, "w"))
    return(print(CMAG + f'\nThank you. Your file {file} has been saved' + CEND))



def review_bike_history(choice, options): # Works
    """Provides complete history for the selected bike and is returned as a table"""
    if choice == 'Add new bike':
        dict_populate(bike)
    elif choice == 'Full bike history':
        bike_table() 
    else:
        temp =[]
        title = ([choice, ' Hardware', 'Date History'])
        for k, v in bike.items():
            if k.startswith((choice,)):
                for x, y in v.items():
                    temp.append([x,y])            
        fancy_print(temp, title)
    return()


def update_hardware_database(choice, options): # Works
    """make updates to the hardware database - bike dict"""
    print(choice)
    print(options)
    hdw_choice  =user_choice('hw_update', options)
    hdw_choice = int(hdw_choice)
    hardw = ['Chain' , 'BottomBracket','Chainset','Headset', 'Cables']  
    date = user_choice('date', options)
    isValidDate = date_validate(date)
    if isValidDate:
        print('Valid Date')  
        bike[choice][hardw[hdw_choice-1]].append(date) 
        return(bike)
   
    return(bike)
 
   
def date_validate(date):  # Works
    """Takes input date and confirms it is of the right format, if not it returns an error."""
    
    isValidDate = True
    if isValidDate == 'x':
        return()
    try:
        isValidDate = bool(datetime.strptime(date, '%d/%m/%Y'))
    except ValueError:
        isValidDate= False
    if(isValidDate):
        print(CMAG + "\nInput date IS valid. Thankyou ..  We have updated the database accordingly" + CEND)
        return(isValidDate)
    else:
        print(CRED + "\nInput date is NOT valid. Please try again using dd/mm/yyyy format" + CEND)
        return()

    
def wheel_cassette_record(choice, options):
    """Provide a history of wheel updates for the chosen wheel"""
    print(options)
    temp =[]
    if choice ==  'Full wheel history':
        wheel_table()
        return(wheel)
    elif choice == 'Add new wheel':
        dict_populate(wheel)
    else:
        title =(['Wheel', 'Date History'])
        for k, v in wheel.items():
            if k.startswith(choice):
                temp.append([k, v])
        fancy_print(temp, title)
        NewCass= input(CGRE + f'\nEnter date new {choice} cassette installed dd/mm/yyyy: ' + CEND)
        date_validate(NewCass)
        wheel[choice].append(NewCass)
        print('\nCassette changes have been made on the dates shown in the table above. Your update is included. Thank you: \n\n')
        for k, v in wheel.items():
            if k.startswith(choice):
                temp.append([k, v])
        fancy_print(temp, title)
    return(wheel)    


def tidy_up(): #Not yet converted to new all-dic format
    """Hidden function call usinr 't' entry will delete old entries and keep just the last 4"""
    
    temp = []
    for k in hardware.keys():
        length = len(hardware[k])
        size = length -4
        start = 0
        while start <= size :
            del hardware[k][0]
            start += 1
    print( 'Tidy up function complete. The new database is shown below\n\n')
    for k , v in hardware.items():
        temp.append([k,v])
    print(CMAG)
    table = tabulate(temp, tablefmt="fancy_grid")
    print('\n' + table)
    print(CEND)
    return()
    
    
def main(bike, wheel):
    """main program definition from which main menu is initially called using user_choice()
    The main then calls the required functions as defined and required"""

    active = True
    all_dic =[wheel, bike]
    while active:
        print('\n                Welcome to your bike hardware maintenance database.')
        print(CMAG + '\nTo enter maintenance mode type m  '+ CEND)
        inter_type = user_choice('initial', active)
        if  inter_type == '1':
            choice, options  = user_choice('whe', active)
            wheel = wheel_cassette_record(choice, options)
        elif inter_type == '2':
            choice, options = user_choice('bik', active)
            bike = review_bike_history(choice, options)       
        elif inter_type == '3':
            choice, options = user_choice('bik', active)
            bike = update_hardware_database(choice, options)
        elif inter_type == '4':
            bike_table()
            wheel_table()
        elif inter_type == '5':
            all_dic =[wheel, bike]
            close_file(path, file, all_dic)
            active = False
            break
        elif inter_type == 'm':
            tidy_up()
        else:
            continue
    
#Program starts
file = 'hardware.json'
path = 'C:/Users/Geoff/Desktop/'
wheel, bike = open_file(path, file)


if __name__ == '__main__':
    main(bike, wheel)




    
