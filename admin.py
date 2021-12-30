import mysql.connector as sql
from tkinter import *
from tkinter import messagebox
import time
import os
from PIL import ImageTk, Image
import tkinter.scrolledtext as tkst
from tkinter import ttk

num= 2001
db= sql.connect(host= 'localhost', user= 'root', password= '', database= 'library')

def admin():
    root= Tk()
    root.title('Admin Login')
    root.geometry('700x700')
    frame1=Frame(root,height=100)
    label=Label(frame1,text=' Admin Login ',bg='blue',fg='white',relief=SUNKEN, font=('comic sans ms',18,'bold')).pack()
    frame1.pack(fill=X,pady=50)
    login(root)
    root.mainloop()
    return root

def login(root):
    user= StringVar()
    passwd= StringVar()
    uframe= Frame(root, width= 100, height= 100)
    ulabel= Label(uframe, text= ' Username ', relief= SUNKEN, font=('Verdana',11,'bold'))
    ulabel.pack(pady= 10)
    uentry= Entry(uframe, textvariable= user)
    uentry.pack()
    uframe.pack(fill=X, padx= 70, pady= 10)
    user= (uentry.get())
    
    pframe= Frame(root, width= 100, height= 100)
    plabel= Label(pframe, text= ' Password  ', relief= SUNKEN, font=('Verdana',11,'bold'))
    plabel.pack(pady= 10)
    pentry= Entry(pframe, textvariable= passwd)
    pentry.pack()
    pframe.pack(fill= X, padx= 70)
    passwd= (pentry.get())
    #print(passwd)
    
    b= Frame(root, width= 70, height= 70)
    submit= Button(b, text= 'Login',font=('Verdana',11,'bold'),command= lambda: check_login(root, uentry, pentry),bg='green',fg='white',width=5)
    submit.grid(row= 0, column= 600)
    #b.place(relx= 0.1, rely= 0.1)
    b.pack(fill= X, padx= 180, pady= 10)
    
    eframe= Frame(root, width= 70, height= 50)
    exitb= Button(b, text= 'Exit',font=('Verdana',11,'bold'),command= lambda: close_win(root),width=5)
    exitb.grid(row= 0, column=680)
    eframe.pack(fill= X)
    
  
def admin_panel():
    win= Tk()
    win.title('Admin Panel')
    win.geometry('700x700')
    bg= ImageTk.PhotoImage(Image.open("lib2.jpg")) 
    imlabel= Label(win, image= bg)
    imlabel.pack()
    imlabel.place(x=0, y=0)
    
    frame1= Frame(win, height= 100)
    frame1.place(relx= 0.9, rely= 0.9)
    label1= Label(frame1, text= 'Welcome Admin', bg='orange',fg='white',relief=SUNKEN, font=('comic sans ms',18,'bold')).pack()
    frame1.pack(pady= 50)
    
    #new book to be inserted in database
    addf= Frame(win, height= 100)
    addbut= Button(addf, text= 'Add book', font=('comic sans ms',12,'normal'), command= lambda: insert_book(win)).pack()
    addf.pack(pady= 10)
    
    #see books issued records
    issuef= Frame(win, height= 100)
    issbut= Button(issuef, text= 'See books issued', font=('comic sans ms',12,'normal'), command= lambda: see_issued(win)).pack()
    issuef.pack(pady= 10)
    
    
    #delete books
    delf= Frame(win, height= 100)
    delbut= Button(delf, text= 'Remove a book', font=('comic sans ms',12,'normal'), command= lambda: del_book(win)).pack()
    delf.pack(pady= 10)
    
    #update information of a book
    updf= Frame(win, height= 100)
    upbut= Button(updf, text= 'Update book information', font=('comic sans ms',12,'normal'), command= lambda: update_book(win)).pack()
    updf.pack(pady= 10)
    
    #see users information
    seef= Frame(win, height= 100)
    seebut= Button(seef, text= 'See users information', font=('comic sans ms',12,'normal'), command= lambda: see_users(win)).pack()
    seef.pack(pady= 10)
    
    exitbut= Button(win, text= 'Logout and exit', command= lambda: win.destroy()).pack()
    
    win.mainloop()
    
def check_login(root, uentry, pentry):
    global db
    user= uentry.get()
    passwd= pentry.get()
    #print(user, passwd)
    logincursor= db.cursor()
    aq= "select role from user where user_id= '{}'".format(user)
    logincursor.execute(aq)
    role= logincursor.fetchone()
    if(role== None):
        messagebox.showinfo('ERROR!', 'No admin found')
        return
    role= role[0]
    if(role != 'admin'):
        messagebox.showinfo('ERROR!', 'You are not admin!')
        return
    q= "select user_id, password from login_details where user_id= '{}'".format(user)
    logincursor.execute(q)
    res= logincursor.fetchone()
    if(res== None):
        messagebox.showinfo('ERROR!', 'No admin found')
        return
    uid= res[0]
    pwd= res[1]
    if(uid== user and pwd== passwd):
        #login successfull
        root.destroy()
        utime= "update login_details set login_time= NOW() where user_id= '{}'".format(user)
        logincursor.execute(utime)
        db.commit()
        print('Login succesful')
        admin_panel()
    else:
        messagebox.showinfo('ERROR!', 'Login credentials dont match')

def entry_string(ent):
    s= ent.get()
    s= str(s)
    return s

def entry_int(ent):
    s= ent.get()
    if(s== ''):
        return
    try:
        i= int(s)
        return i
    except:
        messagebox.showinfo('ERROR!', 'Enter a number')
    
def insert_book(root):
    root.destroy()
    win= Tk()
    win.title('Add Book')
    win.geometry('700x700')
    label=Label(win,text=' Add Book ',bg='orange',fg='white',relief=SUNKEN,\
                font=('comic sans ms',18,'bold'))
    label.pack()
    
    #title
    titf=Frame(win,width=120,height=50)
    titlabel=Label(titf,text='Book title : ',font=('Verdana',12,'normal'))
    titlabel.grid(row=0,column=0)
    titentry= Entry(titf)
    titentry.grid(row=0, column=1)
    titf.pack(fill=X,pady=12,padx=100)
    
    #author
    autf=Frame(win,width=120,height=50)
    autlabel=Label(autf,text='Author : ',font=('Verdana',12,'normal'))
    autlabel.grid(row=0,column=0)
    autentry= Entry(autf)
    autentry.grid(row=0, column=1)
    autf.pack(fill=X,pady=12,padx=100)
    
    #publisher
    pubf=Frame(win,width=120,height=50)
    publabel=Label(pubf,text='Publisher : ',font=('Verdana',12,'normal'))
    publabel.grid(row=0,column=0)
    pubentry= Entry(pubf)
    pubentry.grid(row=0, column=1)
    pubf.pack(fill=X,pady=12,padx=100)
    
    #pages
    pagef=Frame(win,width=120,height=50)
    pagelabel=Label(pagef,text='Pages: ',font=('Verdana',12,'normal'))
    pagelabel.grid(row=0,column=0)
    pagentry= Entry(pagef)
    pagentry.grid(row=0, column=1)
    pagef.pack(fill=X,pady=12,padx=100)
    
    #keyword
    keyf=Frame(win,width=120,height=50)
    keylabel=Label(keyf,text='Keyword : ',font=('Verdana',12,'normal'))
    keylabel.grid(row=0,column=0)
    keyentry= Entry(keyf)
    keyentry.grid(row=0, column=1)
    keyf.pack(fill=X,pady=12,padx=100)
    
    #rack
    racf=Frame(win,width=120,height=50)
    raclabel=Label(racf,text='Rack : ',font=('Verdana',12,'normal'))
    raclabel.grid(row=0,column=0)
    racentry= Entry(racf)
    racentry.grid(row=0, column=1)
    racf.pack(fill=X,pady=12,padx=100)
    
    subf= Frame(win, width=120, height= 50)
    subt= Button(subf,text='Add in database', bd=4, command= lambda: add_db(titentry, autentry, pubentry, pagentry, keyentry, racentry)).pack()
    subf.pack(pady=30)
    
    hframe= Frame(win, height= 100)
    homeb= Button(hframe, text= 'Home', command= lambda: return_to_admin(win)).pack()
    hframe.pack(pady= 10)
    win.mainloop()
    
def add_db(titentry, autentry, pubentry, pagentry, keyentry, racentry):
    global num, db
    tit= entry_string(titentry)
    aut= entry_string(autentry)
    pub= entry_string(pubentry)
    pages= entry_int(pagentry)
    keyword= entry_string(keyentry)
    rack= entry_string(racentry)
    code= keyword[0]+ str(num+1)
    num+=1
    
    query= "insert into Book values('{}','{}','{}','{}',{},'{}', '{}', 0)".format(code, tit, aut, pub, pages, keyword, rack)
    try:
        inscursor= db.cursor()
        inscursor.execute(query)
        db.commit()
    except Exception as e:
        messagebox.showinfo('Error', text= e)
    
def return_to_admin(root):
    root.destroy()
    admin_panel()
    
def see_issued(root):
    global db
    query= "select book.book_code, book.name, user.user_id, user.name, issued_on, return_date\
        from user, book, issue where user.user_id= issue.user_id and book.book_code= issue.book_code;"
    sicursor= db.cursor()
    sicursor.execute(query)
    data= sicursor.fetchall()
    print(data)
    
    root.destroy()
    win= Tk()
    win.title('Books Issued')
    win.geometry('700x700')
    label=Label(win,text=' Books issued ',bg='orange',fg='white',relief=SUNKEN,\
                font=('comic sans ms',18,'bold')).pack()

    cols= ('code', 'name', 'id', 'uname', 'issue', 'return')
    tree= ttk.Treeview(win, columns= cols, show= 'headings')
    tree.heading('code', text= 'Book code')
    tree.heading('name', text= 'Book name')
    tree.heading('id', text= 'User ID')
    tree.heading('uname', text= 'Users name')
    tree.heading('issue', text= 'Issued on')
    tree.heading('return', text= 'Return date')
    
    for row in data:
        tree.insert('', END,value= row)
    tree.pack()
    #tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = ttk.Scrollbar(win, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack()
    #scrollbar.grid(row=0, column=1, sticky='ns')
    
    hframe= Frame(win, height= 100)
    homeb= Button(hframe, text= 'Home', command= lambda: return_to_admin(win)).pack()
    hframe.pack(pady= 10)
    win.mainloop()
    
def del_book(root):
    root.destroy()
    win= Tk()
    win.title('Remove Book')
    win.geometry('700x700')
    label=Label(win,text=' Remove Book ',bg='orange',fg='white',relief=SUNKEN,\
                font=('comic sans ms',18,'bold'))
    label.pack()
    
    #code
    codef=Frame(win,width=120,height=50)
    codelabel=Label(codef,text='Book Code : ',font=('Verdana',12,'normal'))
    codelabel.grid(row=0,column=0)
    codentry= Entry(codef)
    codentry.grid(row=0, column=1)
    codef.pack(fill=X,pady=12,padx=100)
    
    #title
    titf=Frame(win,width=120,height=50)
    titlabel=Label(titf,text='Book title : ',font=('Verdana',12,'normal'))
    titlabel.grid(row=0,column=0)
    titentry= Entry(titf)
    titentry.grid(row=0, column=1)
    titf.pack(fill=X,pady=12,padx=100)
    
    subf= Frame(win, width=120, height= 50)
    subt= Button(subf,text='Remove from database', bd=4, command= lambda: deleteb(codentry, titentry)).pack()
    subf.pack(pady=30)
    
    hframe= Frame(win, height= 100)
    homeb= Button(hframe, text= 'Home', command= lambda: return_to_admin(win)).pack()
    hframe.pack(pady= 10)
    win.mainloop()
    
def deleteb(codentry, titentry):
    global db
    code= entry_string(codentry)
    name= entry_string(titentry)
    query= "delete from book where book_code= '{}' and name= '{}'".format(code, name)
    try:
        dc= db.cursor()
        dc.execute(query)
        db.commit()
        messagebox.showinfo('Successful', text= 'Record deleted successfully!')
    except Exception as e:
        messagebox.showinfo('Error', text= e)
    
def update_book(root):
    root.destroy()
    win= Tk()
    win.title('Update Book')
    win.geometry('700x700')
    label=Label(win,text=' Update information ',bg='orange',fg='white',relief=SUNKEN,\
                font=('comic sans ms',18,'bold'))
    label.pack()
    
    codef=Frame(win,width=120,height=50)
    codelabel=Label(codef,text='Book Code : ',font=('Verdana',12,'normal'))
    codelabel.grid(row=0,column=0)
    codentry= Entry(codef)
    codentry.grid(row=0, column=1)
    codef.pack(fill=X,pady=12,padx=100)
    
    #title
    titf=Frame(win,width=120,height=50)
    titlabel=Label(titf,text='Book title : ',font=('Verdana',12,'normal'))
    titlabel.grid(row=0,column=0)
    titentry= Entry(titf)
    titentry.grid(row=0, column=1)
    titf.pack(fill=X,pady=12,padx=100)
    
    #author
    autf=Frame(win,width=120,height=50)
    autlabel=Label(autf,text='Author : ',font=('Verdana',12,'normal'))
    autlabel.grid(row=0,column=0)
    autentry= Entry(autf)
    autentry.grid(row=0, column=1)
    autf.pack(fill=X,pady=12,padx=100)
    
    #publisher
    pubf=Frame(win,width=120,height=50)
    publabel=Label(pubf,text='Publisher : ',font=('Verdana',12,'normal'))
    publabel.grid(row=0,column=0)
    pubentry= Entry(pubf)
    pubentry.grid(row=0, column=1)
    pubf.pack(fill=X,pady=12,padx=100)
    
    #pages
    pagef=Frame(win,width=120,height=50)
    pagelabel=Label(pagef,text='Pages: ',font=('Verdana',12,'normal'))
    pagelabel.grid(row=0,column=0)
    pagentry= Entry(pagef)
    pagentry.grid(row=0, column=1)
    pagef.pack(fill=X,pady=12,padx=100)
    
    #keyword
    keyf=Frame(win,width=120,height=50)
    keylabel=Label(keyf,text='Keyword : ',font=('Verdana',12,'normal'))
    keylabel.grid(row=0,column=0)
    keyentry= Entry(keyf)
    keyentry.grid(row=0, column=1)
    keyf.pack(fill=X,pady=12,padx=100)
    
    #rack
    racf=Frame(win,width=120,height=50)
    raclabel=Label(racf,text='Rack : ',font=('Verdana',12,'normal'))
    raclabel.grid(row=0,column=0)
    racentry= Entry(racf)
    racentry.grid(row=0, column=1)
    racf.pack(fill=X,pady=12,padx=100)
    
    subf= Frame(win, width=120, height= 50)
    subt= Button(subf,text='Update in database', bd=4, command= lambda: update(codentry, titentry, autentry, pubentry, pagentry, keyentry, racentry)).pack()
    subf.pack(pady=30)
    
    hframe= Frame(win, height= 100)
    homeb= Button(hframe, text= 'Home', command= lambda: return_to_admin(win)).pack()
    hframe.pack(pady= 10)
    win.mainloop()

def update(codentry, titentry, autentry, pubentry, pagentry, keyentry, racentry):
    global db
    code= entry_string(codentry)
    name= entry_string(titentry)
    aut= entry_string(autentry)
    pub= entry_string(pubentry)
    pages= entry_int(pagentry)
    keyword= entry_string(keyentry)
    rack= entry_string(racentry)
    if(code== ''):
        messagebox.showinfo('ERROR!', 'Book code cant be empty')
        return
    query= "update book set "
    if(name!= ''):
        query+= "name='{}' ".format(name)
    if(aut!= ''):
        query+= ", author='{}' ".format(aut)
    if(pub!= ''):
        query+= ", publisher='{}' ".format(pub)
    if(pages!= None):
        query+= ", pages={} ".format(pages)
    if(keyword!= ''):
        query+= ", keyword='{}' ".format(keyword)
    if(rack!= ''):
        query+= ", rack='{}' ".format(rack)
    query+= "where book_code= '{}';".format(code)
    dc= db.cursor()
    try:
        dc.execute(query)
        db.commit()
        messagebox.showinfo('Successful', text= 'Record updated successfully!')
    except Exception as e:
        messagebox.showinfo('Error', text= e)

def see_users(root):
    global db
    query= "select * from user;"
    sicursor= db.cursor()
    sicursor.execute(query)
    data= sicursor.fetchall()
    #print(data)
    
    root.destroy()
    win= Tk()
    win.title('User Information')
    win.geometry('700x700')
    label=Label(win,text=' Users Information ',bg='orange',fg='white',relief=SUNKEN,\
                font=('comic sans ms',18,'bold')).pack()
    
    cols= ('id', 'role', 'name', 'dept', 'phone')
    tree= ttk.Treeview(win, columns= cols, show= 'headings')
    tree.heading('id', text= 'User ID')
    tree.heading('name', text= 'User name')
    tree.heading('role', text= 'Role')
    tree.heading('dept', text= 'Department')
    tree.heading('phone', text= 'Phone number')
    
    for row in data:
        tree.insert('', END,value= row)
    tree.pack()
    #tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = ttk.Scrollbar(win, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack()
    #scrollbar.grid(row=0, column=1, sticky='ns')
    
    hframe= Frame(win, height= 100)
    homeb= Button(hframe, text= 'Home', command= lambda: return_to_admin(win)).pack()
    hframe.pack(pady= 10)
    win.mainloop()

def close_win(root):
    root.destroy()

def get_time():
    localtime = time.ctime()
    return localtime
    
root= admin()