#main file of home page
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk
import mysql.connector as sql

def home_screen():
    root= Tk()
    root.title('Library Manager')
    root.geometry('800x800')
    bg= ImageTk.PhotoImage(Image.open("lib2.jpg")) 
    imlabel= Label(root, image= bg)
    imlabel.pack()
    imlabel.place(x=1, y=1)
    frame1=Frame(root,height=100)
    label=Label(frame1,text=' Welcome to Library manager! ',bg='orange',fg='white',relief=SUNKEN, font=('comic sans ms',18,'bold')).pack()
    frame1.pack(pady=50)
    
    
    userf= Frame(root, height= 100)
    userbut= Button(userf, text= 'User Login', font=('comic sans ms',12,'normal'), command= lambda: user_login(root)).pack()
    userf.pack(pady= 10)
    
    
    adminf= Frame(root, height= 100)
    adminbut= Button(adminf, text= 'Admin Login', font=('comic sans ms',12,'normal'), command= lambda: admin_login(root)).pack()
    adminf.pack(pady= 10)
    
    
    
    newf= Frame(root, height= 100)
    newbut= Button(newf, text= 'Register new user', font=('comic sans ms',12,'normal'), command= lambda: new_user(root)).pack()
    newf.pack(pady= 10)
    
    exitf= Frame(root, height= 100)
    exitb= Button(exitf, text= 'Exit', command= lambda: root.destroy()).pack()
    exitf.pack(pady=10)
    
    
    root.mainloop()
    return root

def user_login(root):
    root.destroy()
    import user

def admin_login(root):
    root.destroy()
    import admin

def new_user(oldroot):
    oldroot.destroy()
    root= Tk()
    root.title('New User')
    root.geometry('800x800')
    frame1=Frame(root,height=100)
    label=Label(frame1,text=' Register new user ',bg='orange',fg='white',relief=SUNKEN, font=('comic sans ms',18,'bold')).pack()
    frame1.pack(pady=50)
    
    uframe= Frame(root, height= 100)
    ulabel= Label(uframe, text= ' User ID ', relief= SUNKEN, font=('Verdana',11,'bold'))
    ulabel.pack(pady= 10)
    uentry= Entry(uframe)
    uentry.pack()
    uframe.pack(fill=X, padx= 70, pady= 10)
    
    nframe= Frame(root, height= 100)
    nlabel= Label(nframe, text= ' Name ', relief= SUNKEN, font=('Verdana',11,'bold'))
    nlabel.pack(pady= 10)
    nentry= Entry(nframe)
    nentry.pack()
    nframe.pack(fill=X, padx= 70, pady= 10)
    
    dframe= Frame(root, height= 100)
    dlabel= Label(dframe, text= ' Department ', relief= SUNKEN, font=('Verdana',11,'bold'))
    dlabel.pack(pady= 10)
    dentry= Entry(dframe)
    dentry.pack()
    dframe.pack(fill=X, padx= 70, pady= 10)
    
    phframe= Frame(root, height= 100)
    phlabel= Label(phframe, text= ' Phone numebr ', relief= SUNKEN, font=('Verdana',11,'bold'))
    phlabel.pack(pady= 10)
    phentry= Entry(phframe)
    phentry.pack()
    phframe.pack(fill=X, padx= 70, pady= 10)
    
    pframe= Frame(root, height= 100)
    plabel= Label(pframe, text= ' Password  ', relief= SUNKEN, font=('Verdana',11,'bold'))
    plabel.pack(pady= 10)
    pentry= Entry(pframe)
    pentry.pack()
    pframe.pack(fill= X, padx= 70)
    
    b= Frame(root, width= 70, height= 70)
    submit= Button(b, text= 'Register',font=('Verdana',11,'bold'),command= lambda: register(uentry, nentry, dentry, phentry, pentry),bg='green',fg='white')
    submit.grid(row= 0, column= 600)
    #b.place(relx= 0.1, rely= 0.1)
    b.pack(fill= X, padx= 180, pady= 10)
    
    eframe= Frame(root, width= 70, height= 50)
    exitb= Button(b, text= 'Exit',font=('Verdana',11,'bold'),command= lambda: root.destroy())
    exitb.grid(row= 0, column=680)
    eframe.pack(fill= X)


def register(uentry, nentry, dentry, phentry, pentry):
    userid= uentry.get()
    name= nentry.get()
    dept= dentry.get()
    phone= phentry.get()
    password= pentry.get()
    
    insu= "insert into user values ('{}', 'user', '{}', '{}', '{}');".format(userid, name, dept, phone)
    inslog= "insert into login_details values ('{}', '{}', NOW());".format(userid, password)
    db= sql.connect(host= 'localhost', user= 'root', password= '', database= 'library')
    ic= db.cursor()
    try:
        ic.execute(insu)
        db.commit()
    except Exception as e:
        messagebox.showinfo('Error', text= e)
    try:
        ic.execute(inslog)
        db.commit()
    except Exception as e:
        messagebox.showinfo('Error', text= e)
    

home_screen()