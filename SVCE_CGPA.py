'''
*A script which can be used by svceians
*This is an automted python script to calculate your CGPA directly from your cms.
*Provided that you have to enter your cms login_id and password.
___________________________________________________________________________________________
Packages needed to run the script:
-> selenium
-> chrome|firefox webdriver
-> BeautifulSoup
___________________________________________________________________________________________
KEY Feature
CGPA Predicter:
    *How much grade you have to get in the subjects of current sem to achieve your dream CGPA
Web APP with these implementations.

'''

#necessary packages were imported selenium and BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup

#Upto which semester cgpa you need: enter here
global I #This is assigned as a global variable 
sem = []
print('Enter  your admission number(2016cse08xx):')
arr = input().upper()
print('')
print('Enter your Password:')
u1 = input('pass')
print('------------------------------------------------------------------')
print('')
print('CGPA of Which Semester Wanted:')
print('Note::: Please ensure that you cms have the data till the sem number you are entering  ')
I = int(input()) + 1

#Hit the webdriver
browser = webdriver.Chrome()
browser.get("https://cms.svce.ac.in/") 
time.sleep(2)

#Enter User Credentials
user_id = 'ST'+arr+'.SVCE'
passcode = u1

#user_name and password field in the webpage is found using ID
username = browser.find_element_by_id("userName")
password = browser.find_element_by_id("hashedpassword")

#Passing the user values
username.send_keys(user_id)
password.send_keys(passcode)

#Entering values of submit button
login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
login_attempt.submit()

#according to cms the university result field is hit for no of I semesters needed
for i in range(1,I):
    query = 'Semester '+ str(i)
#much needed and important try and catch block to wait for all the operations to complete    
    try:
        
        b = browser.find_element_by_xpath("//select[@id='semesterDropDown1']/option[text()='" + query + "']").click()
        time.sleep(3)
    except:
        pass
    
    #page source code is parsed to BeautifulSoup
    page = browser.page_source
    soup = BeautifulSoup(page)
    unimark = soup.find(lambda tag: tag.name=='div' and tag.has_attr('id') and tag['id']=="University_Mark") 
    
    rows = unimark.find('tbody')
    #Appending the subject code and grade of each subject to the list
    se = []
    for sr in rows.findAll('td'):

        if len(sr.text) <= 8 or len(sr.text) == 1:
            se.append(sr.text)
    sem.append(se)
    
        
        
        
#Hit thi)s page to get the subject details and credits
browser.get('https://cms.svce.ac.in/studentSubjectDetails')
page = browser.page_source
soup = BeautifulSoup(page)
unimark = soup.find(lambda tag: tag.name=='section' and tag.has_attr('id') and tag['id']=="content") 

rows = unimark.find('tbody')
#Appending credits and subject codes to list c
c = []
for sr in rows.findAll('td'):
     if len(sr.text) <= 8 or len(sr.text) == 1 or len(sr.text) == 2:
            c.append(sr.text)
            
#converting the list c to dict
credits = dict(zip(c[::2], c[1::2]))

#fisplit is the final splitup in where subject code , grades,marks are being matched
last = []
for i in sem:
        lee = []
        for j in range(0,len(i),2):
            li = []
            li.append(i[j])
            li.append(credits[i[j]])
            li.append(i[j+1])
            lee.append(li)
        last.append(lee)


#function to calculate CGPA and GPA    
def cal(sub):
    num = 0
    den = 0
    cgpa = 0
    
    for ent in sub:
        den += int(ent[1] )
        if ent[2].lower() == 's':
            num = num + 10*int(ent[1])
        elif ent[2].lower() == 'a':
            num = num + 9*int(ent[1])
        elif ent[2].lower() == 'b':
            num = num + 8*int(ent[1])
        elif ent[2].lower() == 'c':
            num = num + 7*int(ent[1])
        elif ent[2].lower() == 'd':
            num = num + 6*int(ent[1])
        elif ent[2].lower() == 'e':
            num = num + 5*int(ent[1])
        else:
            continue
    global den_c
    global num_c
        
    den_c += den
    num_c += num
    #For GPA Estimator
    n_g.append(num)
    d_g.append(den)
    n_cg.append(num_c)
    d_cg.append(den_c)
    gpa1 = num/den
    cgpa1 = num_c/den_c
    g.append(gpa1)
    cg.append(cgpa1)

    gpa = round(num/den,2)
    cgpa = round(num_c/den_c,2)
    print('GPA in SEM'+str(i+1)+':'+str(gpa))
    

    return [gpa,cgpa]
#Function for CGPA Estimator
def run(exp,cc,s):
    exp = float(exp)
    cc = int(cc)
    s= int(s)
    
    s = s-1
    anz = (((exp * float(d_cg[s])) -  float(n_cg[s-1]))/cc)
    anzz = anz*cc
    if(anz <= 10 and anz >= 5):
        print('You have to score the GPA of  : ' + str(round(anz,2))+' in sem '+str(esti)+' to get your Dream CGPA')
    else:
        print('Sorry Folks, Its not possible to achieve this CGPA..')
        print('You either would have entered a higher cgpa or a lesser which you cant get ')
    
    return [anz,anzz]

den_c = 0
num_c = 0
cgpa = 0
d_g = []
n_g = []
d_cg = []
n_cg = []
g = []
cg = []
#All of those for this small piece 
for i in range(len(last)):
    result = cal(last[i])
print('____________________________')
print('FINAL CGPA:'+ str(result[1]))
print('____________________________')
print('')
print('')
print('------------------------------------------------------------------------------------')
print('---------------------------NEW FETURE-----------------------------------------------')
print('------------------------------------------------------------------------------------')
print('You can now estimate how much GPA you need to get in a semester to get your dream CGPA ')
print('Example: I wrote till 5th semester and i have the data of subjects and marks till sem5 in my cms')
print('and i want to know, how much GPA do I have to get in SEM-6 to get 9.5?')
print('Well Its Possible here')
print('------------------------------------------------------------------------------------')
print('------------------------------------------------------------------------------------')
print('------------------------------------------------------------------------------------')

xx = 0
esti = input('Enter The Semester Number for which you want to know the estimate:')
cc = input('Total Number of credits in the semester usually(25 or 23): ')

def ulti():
    exp = input('Enter your dream CGPA:')
    if int(esti) <= len(d_cg):
        run(exp,cc,esti)

    elif int(esti) == (len(d_cg)+1):
        d_cg.append(d_cg[int(esti) - 2] + int(cc) )

        lulu = run(exp,cc,esti)
            #print('You have to score the GPA of in sem ' +str(esti)+str(lulu[0])+' to get your Dream CGPA')

        d_cg.remove(d_cg[-1])
    else:
        print('Not enough data to process your request')
        print('The Data Scrapped is till sem '+str(len(n_cg)) )
    return

while xx == 0:
    ulti()
    print('')
    print('Press 0 to continue and 1  to exit')
    xx += int(input())


    








