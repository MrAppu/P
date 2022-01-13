from pickle import load,dump
from time import sleep
import secrets
import hashlib
from os import path,remove
import time

def first_input():
    print('''
    ###############################
    ##### Welcome to the ATM! #####
    ###############################
    
       Please select your option:
       1. Login to the system
       2. Create a new account
       3. Exit''')   
    run_inp=input('Enter the option you need:')
    if  run_inp=='1':
        Login_Card()
    elif run_inp=='2':
        Login_Name()
    elif run_inp=='3':
        print('Thank you for coming. Visit again!')
        time.sleep(5)
        first_input()
    elif run_inp=='adminconsole':
        print('Initialising admin console')
        Admin_Console()       
    else:
        print('Please enter the correct number. Press "Enter" to restart')
        input()
        first_input()


def Login_Name():
    get_user=input('Enter your username. Type "0" to go back:')
    if get_user.isalnum()==True:
        if get_user=='0':
            first_input()
        if len(get_user)>=32:
            print("All usernames must be below 32 charactors")
            input()
            Login_Name()
        else:
            Login_Pin(get_user,'log_name')
    else:
        print('Only alpha-numeric charectors allowed. Press "Enter" to go back')
        input()
        Login_Name()


def Login_Card():
    while True:
        try:
            card=int(input("Enter your 12 digit Card Number. Type '0' to go back:"))
            if card==0:
                first_input()
            elif len(str(card))==12:
                access(str(card),'card_check','')    
            else:
                print("Please enter 12 digits. Press 'Enter' key to restart")
                input()
                Login_Card()
        except ValueError:
          print("Please use numbers. Press Enter key to restart")
          input()
          Login_Card()


def Login_Pin(username,towards):
    get_pin=input("Enter your 4 digit PIN code. Type '0' to go back:")
    if get_pin=='0':
                if towards=='log_name':
                    Login_Name()
                if towards=='in_user':
                    Login_Card()
    elif len(str(get_pin))==4:
                print("Done")
                if towards=='log_name':
                    conf_module(username,get_pin)
                if towards=='in_user':
                    print("Please wait for few seconds...")
                    sleep(3)
                    access(username,'pin_chk',get_pin)

    else:
                print("Please enter 4 digits. Press 'Enter' key to restart")
                input()
                Login_Pin(towards,username)


def conf_module(user,pin):
    print(f'''Confirm your Username and PIN
    Username : {user}
    PIN : {pin}
    ''')
    conf=input("Confirmation required Y/N: ").lower()
    if conf == 'y':
        card_num(user,pin)  
    elif conf == 'n':
        sconf()
    else:
        print('Please enter Y/N. Press enter to go back ')
        input()
        conf_module(user,pin)
def sconf():
    sec_conf=input("Would you like to try it again? Y/N").lower()    
    if sec_conf == 'n':
        Login_Name()
    elif sec_conf == 'n':
        print("Exiting now!")
        print("Thank you for using the ATM, visit again!!")
        first_input()



#====================================== CARD MODULES =======================================# 

def card_gen():
    gen=secrets.randbelow(int(1e12))
    if len(str(gen))==12:
        if gen!=None:
            return gen
    else:
        card_gen()

# This checks if a card is available to give, by checking in a pregenerated file.
def card_checker(string):     
    with open(GetFileLoc("card.txt"), "a+") as file:
        for line in file:
            line = line.rstrip()
            if string in line:
                if string==line:
                    card_num()
        else:
            file.write(string+'\n')         

def splitting_card(s):
    s=str(s)
    a=(s[:4])
    b=(s[4:8])
    c=(s[8:12])
    print(a+' '+b+' '+c)

# This is where all the things are merged. It contain the generator, checker, splitter and cryptographic functions. 
def card_num(user,pin):
        crdnum=card_gen()
        card_checker(str(crdnum))
        crypt(user,pin,crdnum)
        print('This is your card number. Keep it safe') 
        splitting_card(crdnum)
        account_creation(crdnum,pin) 
        print("You have sucessfully registered. Press Enter to go back")
        input()
        first_input()



#================================= CRYPTOGRAPHIC FUNCTIONS ==================================#
        
def crypt(user,pinnum,card):
    pwd=bytes(user+str(pinnum)+str(card), encoding='utf8')
    mix_salt=secrets.token_bytes(32)
    key=hashlib.scrypt(password=pwd, salt=mix_salt, n=16384, r=8, p=1, dklen=64)
    users={}
    users[f"{user}",f"{card}"] = {
        "salt": mix_salt,
        "key" : key
    }
    txt_file = GetFileLoc('file.atm')
    with open(txt_file,'ab') as data:    
        dump(users,data)   

def check_pwd(card,user,pin):
    tup = (user,card)
    up_user=up[tup]
    get_salt=(up_user.get('salt', 'A fatal error has occured. Inform the admin and give this error: "0xs0"'))
    get_key=(up_user.get('key', 'A fatal error has occured. Inform the admin and give this error: "0xk0'))
    pwd_check=bytes(user+str(pin)+str(card), encoding='utf8')
    check_key=hashlib.scrypt(password=pwd_check, salt=get_salt, n=16384, r=8, p=1, dklen=64)
    global checking
    if get_key == check_key:
        checking='confrmd'
    else:
        print("Your pin or card number is wrong. Please start from the beginning. Press enter to go back.")
        input()
        Login_Card()          
#===================================== FILE FUNCTIONS =======================================# 
def GetFileLoc(file):
    file_path = path.abspath(__file__)                  # full path of your script
    dir_path = path.dirname(file_path)                  # full path of the directory of your script
    file_path = path.join(dir_path, file)
    return file_path

def access(crd,usr,pin):
    txt_file = GetFileLoc('file.atm')  
    with open(txt_file,'rb') as data:    
        global up
        unpickled = []
        while True:
            try:
                unpickled.append(load(data))
                up=unpickled[-1]
                
                for i in up:
                    if i[-1]==crd:
                        if usr=='card_check':
                            Login_Pin(crd,'in_user')
                        if usr=='pin_chk':
                            user=i[0]
                            check_pwd(crd,user,pin)
                            if checking=='confrmd':
                                  print(f'Welcome {user}!')
                                  User_Portal(crd,pin,account_db(str(crd)+str(pin),'check',''))
                                  
                                
                            elif check_pwd(crd,user,pin) is None:    
                                  print('A error has occured. Contact the manager and give this code: None error while checking user')
                                  break
            except EOFError:
                Login_Pin('in_user',crd)

#==================================== ACCOUNT FUNCTIONS =====================================#

def account_creation(card,pin):
    apwd=str(card)+str(pin)
    auth={f"{apwd}":[]}
    auth[apwd].append(0)
    txt_file =GetFileLoc('dbs.atm')  
    with open(txt_file,'ab') as data:
        dump(auth,data)
            

def User_Portal(crd,pin,Balance):
    for i in Balance.values():
        bal=i[0]
    print("\n1 - View Balance\n2 - Withdraw\n3 - Go Back ")
    selection = int(input("\nEnter your selection: "))
    if selection==1:
        print("Your total balance is : Rs",bal)
        sleep(2)
        User_Portal(crd,pin,Balance)
    elif selection == 2:
        amt = float(input("\nEnter amount to withdraw: "))
        ver_withdraw = input("Is this the correct amount, Y/N ? " + str(amt) + " ").lower()
        if ver_withdraw == "y":
            print("Verifying withdrawal")
        else:
            print('Press "Enter" to go back')
            input()
            User_Portal(crd,pin,Balance)    
        if amt < bal:
            if bal-amt < bal:
                print("You dont have the sufficient funds to perform this transaction. Please select a number less than",bal,'\nPress "Enter" to go back.')
                input()
                User_Portal()           
            else:
                bal=bal-amt
                lbal=[bal]
                print("Please collect your money below")
                print("Your Transaction number:",trans_checker(secrets.token_hex(7)))
                account_db(str(crd)+str(pin),'update',lbal)
                print('Thank you for banking with us. Press "Enter" to go back')
                input()
        else:
            print("You dont have the sufficient funds to perform this transaction. Please select a number less than",bal)
            sleep(1)
            User_Portal(crd,pin,Balance)

    elif selection == 3:
        print("Thank you for visiting us!")
        sleep(2)
        first_input()
    else:
        print("Please select the correct option.")
        User_Portal(crd,pin,Balance)  



def account_db(a,b,bal):
    u=[]
    with open(GetFileLoc('dbs.atm'),'rb') as data:
        while True:
            try:
                u.append(load(data))
            except EOFError:
                break
    co=-1
    for i in u:
        for key,value in i.items():
            co=co+1
            if key==a:
                if b=='check':
                    return(i)
                if b=='update':
                    i.update(value=bal)
                    u[co]=i
                    remove(GetFileLoc('dbs.atm'))
                    with open(GetFileLoc('dbs.atm'),'wb') as data:
                        try:
                            for i in range(len(u)):
                                dump(u[i],data)
                        except RuntimeError:
                            pass
                        except AssertionError:
                            pass
                    

def trans_checker(string):     
    with open(GetFileLoc("tran.txt"), "a+") as file:
        for line in file:
            line = line.rstrip()
            if string in line:
                if string==line:
                    trans_checker(string)
                    
        else:
            file.write(string+'\n')       



#===================================== ADMIN FUNCTIONS ======================================#



def Admin_Console():
    pwd=input("Enter your Password:")
    if pwd=='administrator':
        print("Sucessfully logged in")
        ad_menu()
    else:
        print("Wrong Password!. Wait for 3 seconds...")
        sleep(3)
        Admin_Console()

def ad_menu():
    print('''
    1. Accounts
    2. Records
    3. Exit
    ''')
    
    inp=input('Enter the option you need:')
    if  inp=='1':
        print('''
        1. Create Account
        2. Delete Account
        3. Go Back''')
        Acc=input("Enter your option:")
        if Acc=='1':
            AccWriting()
            print("Done Sucessfully!")
            sleep(1)
            ad_menu()
        if Acc=='2':
            AccRemove()
            sleep(1)
            ad_menu()            
        if Acc=='3':
            ad_menu() 
        else:
            print('Please enter the correct number. Press "Enter" to restart')
            input()
            ad_menu()           
    elif inp=='2':
        print('''
        1. Search By Name
        2. Search By Card Number
        3. List All
        4. Go back''')
        Rec=input("Enter your option:")
        if Rec=='1':
            RecLook(Rec,'name')
            sleep(1)
            ad_menu()            
        if Rec=='2':
            RecLook(Rec,'card')
            sleep(1)
            ad_menu()
        if Rec=='3':
            RecLookAll()
            sleep(1)
            ad_menu()
        if Rec=='4':
            ad_menu()                                    
    elif inp=='3':
        first_input()      
    else:
        print('Please enter the correct number. Press "Enter" to restart')
        input()
        ad_menu()

def AccWriting():
    acc_name=input("Enter the holders name:")
    acc_card=input("Enter the holders card number:")
    acc_pin=input("Enter the holders pin number:")    
    print("The values you entered are,")
    print("1. Account Holders Name : ",acc_name)
    print("2. Account Holders Card Number : ",acc_card)
    print("3. Account Holders Pin Number : ",acc_pin)
    verf=str(input("Enter 1 if this is correct. Enter 2 to go back. Enter 3 for main menu:"))
    
    if verf=='1':
        crypt(acc_name,acc_pin,acc_card)
        account_creation(acc_card,acc_pin)
    if verf=='2':
        AccWriting()
    if verf=='3':
        ad_menu()    
    else:
        print('Please enter the correct number. Press "Enter" to restart')
        input()
        AccWriting() 

def AccRemove():
    acc_name=input("Enter the holders name:")
    acc_card=input("Enter the holders card number:")
    acc_pin=input("Enter the holders pin number:")
    print("The values you entered are,")
    print("1. Account Holders Name : ",acc_name)
    print("2. Account Holders Card Number : ",acc_card)
    print("3. Account Holders Pin Number : ",acc_pin)
    verf=input("Enter 1 if this is correct.(This will make the account useless!) Enter 2 to go back. Enter 3 for main menu:")
    if verf=='1':
        u=[]
        with open(GetFileLoc('dbs.atm'),'rb') as data:
            while True:
                try:
                    u.append(load(data))
                except EOFError:
                    break 
        co=-1
        for i in u:
            for key,value in i.items():
                co=co+1
                if key==(str(acc_card)+str(acc_pin)):
                    del u[co]
                    remove(GetFileLoc('dbs.atm'))
                    with open(GetFileLoc('dbs.atm'),'wb') as data:
                        try:
                            for i in range(len(u)):
                                dump(u[i],data)
                        except RuntimeError:
                            pass
                        except AssertionError:
                            pass
    if verf=='2':
        AccRemove()
    if verf=='3':
        ad_menu()    
    else:
        print('Please enter the correct number. Press "Enter" to restart')
        input()
        AccWriting()        

def RecLook(val,lookup): 
    with open('file.atm','rb') as data:    
        global up
        unpickled = []
        while True:
            try:
                unpickled.append(load(data))
                up=unpickled[-1]
                for i in up:
                    if lookup=='name':
                        if i[0]==val:
                            print("\nName:",val)
                            print("Card No:",i[1])
                    if lookup=='card':
                        if i[-1]==val:
                            print("\nName:",i[0])
                            print("Card No:",val)

            except EOFError:
                break

def RecLookAll():
    with open('file.atm','rb') as data:    
        global up
        unpickled = []
        while True:
            try:
                unpickled.append(load(data))
                up=unpickled[-1]
                for i in up:
                    print("\nName:",i[0])
                    print("Card:",i[1])
            except EOFError:
                break









first_input()
