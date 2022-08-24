import fractions
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

######Functionality Part####

def login_btn():
    if usernameEntry.get()== '' or passwordEntry.get()=='':
        messagebox.showerror('Error', 'Fields are empty!')
    elif usernameEntry.get() == 'asdf' and passwordEntry.get() == 'asdf':
        messagebox.showinfo('Success','Welcome')
        main_window.destroy()
        import SMS
        
    else:
        messagebox.showerror('Error', 'You are not allowed to enter wrong details.')
    




main_window=Tk()
main_window.geometry('1280x700+0+0')
main_window.title('Login to Student Management System')
main_window.resizable(False,False)

#adding background
backgroundImage=ImageTk.PhotoImage(file='bg.jpg')
bgLabel=Label(main_window, image=backgroundImage)
bgLabel.place(x=0,y=0)

### login frame
loginFrame=Frame(main_window,background='white')
loginFrame.place(x=400, y=150)
##logo student
stuLogoImg=PhotoImage(file='logo.png')
stuLogoLabel=Label(loginFrame, image=stuLogoImg,border=False)
stuLogoLabel.grid(row=0, column=0,columnspan=2,pady=10)
#username row
userlogoImg=PhotoImage(file='user.png')
usernameLabel=Label(loginFrame,image=userlogoImg,text='Username',compound=LEFT
                    ,font=('times new roman',20,'normal'),background='white')
usernameLabel.grid(row=1, column=0,pady=10)
#username entry field
usernameEntry=Entry(loginFrame, font=('times new roman',20,'normal'),bd=3,fg='royalblue')
usernameEntry.grid(row=1, column=1,padx=10)

#password row
passwordlogoImg=PhotoImage(file='password.png')
passwordLabel=Label(loginFrame,image=passwordlogoImg,text='Password',compound=LEFT
                    ,font=('times new roman',20,'normal'),background='white')
passwordLabel.grid(row=2, column=0,pady=10)
#password entry field
passwordEntry=Entry(loginFrame, font=('times new roman',20,'normal'),bd=3,fg='royalblue')
passwordEntry.grid(row=2, column=1,padx=10)

#Button login
LoginBtn=Button(loginFrame, text='Login',font=('times new roman',15,'bold')
                ,fg='white',bg='royalblue',width=15,activebackground='white'
                ,activeforeground='royalblue',cursor='hand2',command=login_btn)
LoginBtn.grid(row=3, column=1,pady=10)


main_window.mainloop()