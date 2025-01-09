from sqlite3 import connect
from tkinter import *
import time
from tkinter import messagebox,filedialog
from turtle import bgcolor, right
from webbrowser import BackgroundBrowser
import ttkthemes
from tkinter import ttk
import pymysql
import pandas
####### Functionality Part

count = 0
text=''

def export_data():
    
    url=filedialog.asksaveasfilename(defaultextension='.xlsx')
    
    indexing=studentTable.get_children()
    newlist_to_storeData=[]
    
    for index in indexing:
        content=studentTable.item(index)
        dataList=content['values']
        newlist_to_storeData.append(dataList)
        
    table=pandas.DataFrame(newlist_to_storeData,columns=['Id','Name','Email','Gender','DOB','Mobile Number','Address','Added Record Time','Added Record Date'])

    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data saved successfully')
    
    
def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        sms_window.destroy()
    else:
        pass
    
    

def toplevel_btn_window(title,button_text,command):
    
    global idEntry,nameEntry,emailEntry,toplevelScreenBtns,genderEntry,addressEntry,mobileEntry,dobEntry
    
    toplevelScreenBtns=Toplevel()
    toplevelScreenBtns.title(title)
    toplevelScreenBtns.resizable(0,0)
    toplevelScreenBtns.grab_set()
    
    idLabel=Label(toplevelScreenBtns, text='Id', font=('times new roman',18, 'bold'))
    idLabel.grid(row=0, column=0, padx=15, pady=15, sticky=W)
    
    idEntry=Entry(toplevelScreenBtns, font=('roman',14, 'normal'),width=25)
    idEntry.grid(row=0, column=1,pady=15)
    
    nameLabel=Label(toplevelScreenBtns, text='Name', font=('times new roman',18, 'bold'))
    nameLabel.grid(row=1, column=0, padx=15, pady=15,sticky=W)
    
    nameEntry=Entry(toplevelScreenBtns, font=('roman',14, 'normal'),width=25)
    nameEntry.grid(row=1, column=1,pady=15)
    
    emailLabel=Label(toplevelScreenBtns, text='Email', font=('times new roman',18, 'bold'))
    emailLabel.grid(row=2, column=0, padx=15, pady=15,sticky=W)
    
    emailEntry=Entry(toplevelScreenBtns, font=('roman',14, 'normal'),width=25)
    emailEntry.grid(row=2, column=1,pady=15)
    
    genderLabel=Label(toplevelScreenBtns, text='Gender', font=('times new roman',18, 'bold'))
    genderLabel.grid(row=3, column=0, padx=15, pady=15,sticky=W)
    
    genderEntry=Entry(toplevelScreenBtns, font=('roman',14, 'normal'),width=25)
    genderEntry.grid(row=3, column=1,pady=15)
    
    dobLabel=Label(toplevelScreenBtns, text='DOB', font=('times new roman',18, 'bold'))
    dobLabel.grid(row=4, column=0, padx=15, pady=15,sticky=W)
    
    dobEntry=Entry(toplevelScreenBtns, font=('roman',14, 'normal'),width=25)
    dobEntry.grid(row=4, column=1,pady=15)
    
    mobileLabel=Label(toplevelScreenBtns, text='Mobile', font=('times new roman',18, 'bold'))
    mobileLabel.grid(row=5, column=0, padx=15, pady=15,sticky=W)
    
    mobileEntry=Entry(toplevelScreenBtns, font=('roman',14, 'normal'),width=25)
    mobileEntry.grid(row=5, column=1,pady=15)
    
    addressLabel=Label(toplevelScreenBtns, text='Address', font=('times new roman',18, 'bold'))
    addressLabel.grid(row=6, column=0, padx=15, pady=15,sticky=W)
    
    addressEntry=Entry(toplevelScreenBtns, font=('roman',14, 'normal'),width=25)
    addressEntry.grid(row=6, column=1,pady=15)
    
    
    StuBtn=ttk.Button(toplevelScreenBtns, text=button_text , command=command)
    StuBtn.grid(row=7, columnspan=2,pady=10)
    
    if button_text=='Update':
        indexing=studentTable.focus()
        content=studentTable.item(indexing)
        listData=content['values']
        idEntry.insert(0,listData[0])
        nameEntry.insert(0,listData[1])
        emailEntry.insert(0,listData[2])
        genderEntry.insert(0,listData[3])
        dobEntry.insert(0,listData[4])
        mobileEntry.insert(0,listData[5])
        addressEntry.insert(0,listData[6])
    


    
def update_data():
    try:
        # Validate and reformat DOB
        from datetime import datetime
        try:
            dob = datetime.strptime(dobEntry.get(), '%d%m%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror('Error', 'DOB must be in DDMMYYYY format!', parent=toplevelScreenBtns)
            return

        # Prepare and execute the SQL query
        query = 'UPDATE students SET name=%s, email=%s, gender=%s, dob=%s, mobile=%s, address=%s WHERE id=%s'
        mycursor.execute(query, (
            nameEntry.get(), emailEntry.get(), genderEntry.get(), dob, mobileEntry.get(),
            addressEntry.get(), idEntry.get()))
        con.commit()

        # Success message and UI update
        messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=toplevelScreenBtns)
        toplevelScreenBtns.destroy()
        show_Stu()  # Refresh the TreeView
    except Exception as e:
        # Show the exact error message
        messagebox.showerror('Error', f'Error occurred: {e}', parent=toplevelScreenBtns)

    

def show_Stu():
    query='select * from students'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END, values=data)
    

def deleteStu():
    indexing=studentTable.focus()
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from students where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully')
    query='select * from students'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END, values=data)
    
 
def searchStu():
    query='select * from students where id=%s or name=%s or email=%s or gender=%s or dob=%s or mobile=%s or address=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),genderEntry.get(),dobEntry.get(),mobileEntry.get(),addressEntry.get()))
    
    studentTable.delete(*studentTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END,values=data)
        
        
    
def add_stu_data():
    if idEntry.get() == '' or nameEntry.get() == '' or emailEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '' or mobileEntry.get() == '' or addressEntry.get() == '':
        messagebox.showerror('Error', 'Field Empty!', parent=toplevelScreenBtns)
    else:
        currentdate = time.strftime('%Y-%m-%d')  # Correct format for MySQL DATE type
        currenttime = time.strftime('%H:%M:%S')  # Correct format for MySQL TIME type
        try:
            # Validate and format DOB
            from datetime import datetime

            try:
                dob = datetime.strptime(dobEntry.get(), '%d%m%Y').strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror('Error', 'DOB must be in DDMMYYYY format!', parent=toplevelScreenBtns)
                return

            # Prepare SQL query
            query = 'INSERT INTO students (id, name, email, gender, dob, mobile, address, added_time, added_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(query, (
                idEntry.get(), nameEntry.get(), emailEntry.get(), genderEntry.get(), dob, mobileEntry.get(),
                addressEntry.get(), currenttime, currentdate))
            con.commit()

            # Success message and form reset
            dec = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?',
                                      parent=toplevelScreenBtns)
            if dec:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                emailEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
                mobileEntry.delete(0, END)
                addressEntry.delete(0, END)
            else:
                pass
        except Exception as e:
            # Show the exact error message
            messagebox.showerror('Error', f'Error occurred: {e}', parent=toplevelScreenBtns)
            return


            
        
        query='select * from students'
        mycursor.execute(query)
        fetchedData=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetchedData:
            datalist=list(data)
            studentTable.insert('',END,values=datalist)
            
            
            
            
def clock():
    date=time.strftime('%d/%m/%Y')
    currentTime=time.strftime('%H:%M:%S')
    dateTimeLabel.config(text=f'   Date: {date} \nTime: {currentTime}')
    dateTimeLabel.after(1000,clock)



def connect_database():
    
    def connectdb():
        global mycursor,con
        if hostEntry.get()=='' or usernameEntry.get() == '' or passwordEntry.get()=='':
            messagebox.showerror('Error', 'Empty field',parent=connectwindow)
             
        else:
            
            try:
                
                con=pymysql.connect(host=hostEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
                mycursor=con.cursor()
                messagebox.showinfo('success', 'Connection is successfull',parent=connectwindow)
                query=f'use {dbEntry.get()}'
                mycursor.execute(query)
                connectwindow.destroy()
                
                addStudentBtn.config(state=NORMAL)
                SearchStudentBtn.config(state=NORMAL)
                deleteStudentBtn.config(state=NORMAL)
                updateStudentBtn.config(state=NORMAL)
                showStudentBtn.config(state=NORMAL)
                exportStudentBtn.config(state=NORMAL)
                
                
            except:
                messagebox.showerror('Error','Invalid Details',parent=connectwindow)

            

    
    
    connectwindow=Toplevel()
    connectwindow.grab_set()
    connectwindow.geometry('470x400+730+230')
    connectwindow.title('Connect to Database')
    connectwindow.resizable(0,0)
    
    hostnameLabel=Label(connectwindow, text='Host Name',font=('arial',17, 'normal'))
    hostnameLabel.grid(row=0, column=0)
    
    hostEntry=Entry(connectwindow, font=('roman',14, 'normal'),bd=2)
    hostEntry.grid(row=0, column=1,padx=35,pady=20)
    
    dbnameLabel=Label(connectwindow, text='Database Name',font=('arial',17, 'normal'))
    dbnameLabel.grid(row=1, column=0)
    
    dbEntry=Entry(connectwindow, font=('roman',14, 'normal'),bd=2)
    dbEntry.grid(row=1, column=1,padx=35,pady=20)
    
    usernameLabel=Label(connectwindow, text='Username',font=('arial',17, 'normal'))
    usernameLabel.grid(row=2, column=0)
    
    usernameEntry=Entry(connectwindow, font=('roman',14, 'normal'),bd=2)
    usernameEntry.grid(row=2, column=1,padx=35,pady=20)
    
    passwordLabel=Label(connectwindow, text='Password',font=('arial',17, 'normal'))
    passwordLabel.grid(row=3, column=0)
    
    passwordEntry=Entry(connectwindow, font=('roman',14, 'normal'),bd=2)
    passwordEntry.grid(row=3, column=1,padx=35,pady=20)
    
    connectBtn=ttk.Button(connectwindow, text='Connect',command=connectdb)
    connectBtn.grid(row=4, columnspan=2)
    
    
    

def slider():
    global text,count 
    if count== len(s):
        count=0
        text=''

    text=text+s[count]
    sliderLabel.config(text=text)
    sliderLabel.config(fg='royalblue')
    count+=1

    sliderLabel.after(300,slider)
    
    

sms_window=ttkthemes.ThemedTk()

sms_window.get_themes()


sms_window.set_theme('radiance')


sms_window.geometry('1174x680+0+0')
sms_window.resizable(0, 0)
sms_window.title('Student Management System')

##showing date and time
dateTimeLabel=Label(sms_window,text='Here is time',font=('times new roman',17,'bold'))
dateTimeLabel.place(x=5, y=5)
clock()

## slider
s='Student Management System'
sliderLabel=Label(sms_window, text=s, font=('arial', 28, 'bold'),width=38)
sliderLabel.place(x=200, y=0)
slider()

### connect to database button
connectBtn=ttk.Button(sms_window, text='Connect database', command=connect_database)
connectBtn.place(x=980, y=0)

####### FRAMES
leftFrame=Frame(sms_window)
leftFrame.place(x=50, y=80, width=300, height=600)

logoImage=PhotoImage(file='student1.png')
logoLabel=Label(leftFrame, image=logoImage)
logoLabel.grid(row=0, column=0)

### left frame buttons
addStudentBtn=ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED, command=lambda :toplevel_btn_window('Add Student', 'Add Student',add_stu_data))
addStudentBtn.grid(row=1, column=0,pady=20)

SearchStudentBtn=ttk.Button(leftFrame, text='Search Student', state=DISABLED,width=25,command=lambda :toplevel_btn_window('Search Student','Search',searchStu))
SearchStudentBtn.grid(row=2, column=0,pady=20)

deleteStudentBtn=ttk.Button(leftFrame, text='Delete Student', width=25,state=DISABLED,command=deleteStu)
deleteStudentBtn.grid(row=3, column=0,pady=20)

updateStudentBtn=ttk.Button(leftFrame, text='Update Student', width=25,state=DISABLED, command=lambda :toplevel_btn_window('Update Student Record','Update',update_data))
updateStudentBtn.grid(row=4, column=0,pady=20)

showStudentBtn=ttk.Button(leftFrame, text='Show Student', width=25,state=DISABLED, command=show_Stu)
showStudentBtn.grid(row=5, column=0,pady=20)

exportStudentBtn=ttk.Button(leftFrame, text='Export Data', width=25,state=DISABLED, command=export_data)
exportStudentBtn.grid(row=6, column=0,pady=20)

exitBtn=ttk.Button(leftFrame, text='Exit', width=25, command=iexit)
exitBtn.grid(row=7, column=0,pady=20)


### rigth frame
rightFrame=Frame(sms_window)
rightFrame.place(x=350, y=80, width=820, height=600)

## scroll bar
scrollBarX=Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame, orient=VERTICAL)


### Table 
studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Email', 'Gender', 'DOB','Mobile Number','Address'
                                 ,'Record Added Time','Record Added Date')
                          ,xscrollcommand=scrollBarX.set
                          ,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)


scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)


studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Email',text='Email')
studentTable.heading('Gender',text='Gender')
studentTable.heading('DOB',text='DOB')
studentTable.heading('Mobile Number',text='Mobile Number')
studentTable.heading('Address',text='Address')
studentTable.heading('Record Added Time',text='Record Added Time')
studentTable.heading('Record Added Date',text='Record Added Date')

studentTable.column('Id',width=50, anchor=CENTER)
studentTable.column('Name',width=300, anchor=CENTER)
studentTable.column('Email',width=350, anchor=CENTER)
studentTable.column('Gender',width=90)
studentTable.column('DOB',width=150)
studentTable.column('Mobile Number',width=140, anchor=CENTER)
studentTable.column('Address',width=350, anchor=CENTER)
studentTable.column('Record Added Time',width=175, anchor=CENTER)
studentTable.column('Record Added Date',width=175, anchor=CENTER)


styletree=ttk.Style()
styletree.configure('Treeview', rowhieght=40,font=('arial',12,'bold'),background='orange')

styletree.configure('Treeview.Heading',font=('arial',13,'bold'))
studentTable.config(show='headings')



sms_window.mainloop()