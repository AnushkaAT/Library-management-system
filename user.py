from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector as sql
import time
import tkinter.scrolledtext as tkst
from tkinter import ttk

iduser= ''
#get data about the books
def books(lab1='', lab2='', lab3='', lab4='', radio=0):

    import mysql.connector as sql

    lab1=lab1.capitalize()
    lab2=lab2.capitalize()
    lab3=lab3.capitalize()
    lab4=lab4.capitalize()

    db=sql.connect(host='localhost',user='root',passwd='',db='library')
    cursor=db.cursor()

    query="select book_code, name,author,publisher,rack,issued from book " 
    #print(lab1)
    if(lab1 == ''):
        print('book name empty')
    else:
        query+= "where name like '%{}%' ".format(lab1)
    print(query)
    
    if (lab2=='' and lab3=='' and lab4==''):
        query=query+" order by name"
        
    elif (lab2=='' and lab3!='' and lab4==''):
        if(lab1!= ''):
            query+= 'and'
        else:
            query+= 'where '
        query=query+" publisher like '%{}%' order by name".format(lab3)

    elif (lab2!='' and lab3=='' and lab4==''):
        if(lab1!= ''):
            query+= 'and'
        else:
            query+= 'where '
        query=query+" author like '%{}%' order by name".format(lab2)
    
    elif (lab2=='' and lab3=='' and lab4!=''):
        if(lab1!= ''):
            query+= 'and'
        else:
            query+= 'where '
        query=query+" keyword like '%{}%' order by name".format(lab4)

    elif (lab2!='' and lab3!='' and lab4==''):
        if(lab1!= ''):
            query+= 'and'
        else:
            query+= 'where '
        query=query+" author like '%{}%' and publisher like '%{}%' \
    order by name".format(lab2,lab3)

    elif (lab2=='' and lab3!='' and lab4!=''):
        query=query+" publisher \
    like '%{}%' and keyword like '{}%' order by name".format(lab3,lab4)
    
    elif (lab2!='' and lab3=='' and lab4!=''):
        if(lab1!= ''):
            query+= 'and'
        else:
            query+= 'where '
        query=query+" author like '{}%' and keyword like '{}%' \
    order by name".format(lab2,lab4)

    elif (lab2!='' and lab3!='' and lab4!=''):
        if(lab1!= ''):
            query+= 'and'
        query=query+" author like '{}%' and publisher like '{}%' \
    and keyword like '{}%' order by name".format(lab2,lab3,lab4)
        
    
    if radio==1:
        query=query+", author"
        
    elif radio==2:
        query=query+", publisher"
        
    elif radio==3:
        query=query+", issued"


    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close()
    db.close()
    print(data)  
    return data

def destroy(root_login):
    root_login.destroy()
    

#Display the result of the query int abular form
def disp(data,text):
   words = text.get(1.0,tk.END)
   if words:#to clear the text box
       text.delete(1.0,tk.END)
   cols=('code', 'name', 'author', 'publisher', 'rack', 'issued')
   tree= ttk.Treeview(text, columns= cols, show= 'headings')
   tree.heading('code', text= 'Book code')
   tree.heading('name', text= 'Book name')
   tree.heading('author', text= 'Author')
   tree.heading('publisher', text= 'Publisher')
   tree.heading('rack', text= 'Rack')
   tree.heading('issued', text= 'Issued on')
    
   for row in data:
       tree.insert('', END,value= row)
   tree.pack()
   #tree.grid(row=0, column=0, sticky='nsew')
   scrollbar = ttk.Scrollbar(text, orient=VERTICAL, command=tree.yview)
   tree.configure(yscroll=scrollbar.set)
   scrollbar.pack()

#To get the values from the user to search the books in the database 
def get_values(entry1, entry2, entry3, entry4, var, text):
    words = text.get(1.0,tk.END)
    if words:#to clear the text box
        text.delete(1.0,tk.END)
    var1=var.get()
    lab1=entry1.get()
    '''if lab1=='':
        messagebox.showinfo('Alert!','Book name is required')
        return'''
    
    lab2 = entry2.get()
    lab3 = entry3.get()
    lab4 = entry4.get()

    data=books(lab1,lab2,lab3,lab4,var1)
    disp(data,text)

def issued_book(bentry):
    global iduser
    b_name= bentry.get()
    if(b_name==''):
        messagebox.showinfo('Alert!','Book name is required')
        return
    try:
        db=sql.connect(host='localhost',user='root',passwd='',db='library')
        cursor=db.cursor()
        query="select issued from book where name='{}'".format(b_name)
        cursor.execute(query)
        print('Done 1')
        issued_num=cursor.fetchone()
        issued_num= issued_num[0]
        print(issued_num)
        if (issued_num <5):#set issued attribute to autoincrement
            query="update book set issued= issued+1 where name='{}'".format(b_name)
            cursor.execute(query)
            print('Done 2')
            query= "select book_code from book where name= '{}'".format(b_name)
            cursor.execute(query)
            print('Done 3')
            bid= cursor.fetchone()
            bid= bid[0]
            query= "insert into issue values('{}', '{}', NOW(), NULL)".format(iduser, bid)
            cursor.execute(query)
            db.commit()
            print('Done 4')
            messagebox.showinfo('Successful', 'Book issued')
        else:
            messagebox.showinfo('Alert Box','No copy available to issue')
    except Exception as e:
        messagebox.showinfo('Alert Box', e)
        
def returned_book(bentry):
    global iduser
    b_name= bentry.get()
    if(b_name==''):
        messagebox.showinfo('Alert!','Book name is required')
        return
    try:
        db=sql.connect(host='localhost',user='root',passwd='',db='library')
        cursor=db.cursor()
        query="select issued from book where name='{}'".format(b_name)
        cursor.execute(query)
        issued_num=cursor.fetchone()
        issued_num= issued_num[0]
        if(issued_num > 0):
            query="update book set issued= issued-1 where name='{}'".format(b_name)
            cursor.execute(query)
            query= "select book_code from book where name= '{}'".format(b_name)
            cursor.execute(query)
            bid= cursor.fetchone()
            bid= bid[0]
            query="update issue set return_date= NOW() where book_code= '{}' and user_id= '{}'".format(bid, iduser)
            cursor.execute(query)
            db.commit()
            db.close()
            messagebox.showinfo('Alert Box','Thank you, Copy returned successfully!')
        else:
            messagebox.showinfo('Alert Box','No book issued by the user!')
    except:
        messagebox.showinfo('Alert Box','Error!!')
        
def favorite(bentry):
    global iduser
    b_name= bentry.get()
    #print(b_name)
    if(b_name==''):
        messagebox.showinfo('Alert!','Book name is required')
        return
    try:
        db=sql.connect(host='localhost',user='root',passwd='',db='library')
        cursor=db.cursor()
        query= "select book_code from book where name= '{}'".format(b_name)
        cursor.execute(query)
        bid= cursor.fetchone()
        bid= bid[0]
        query= "insert into favorite values('{}', '{}')".format(iduser, bid)
        cursor.execute(query)
        db.commit()
        db.close()
        messagebox.showinfo('Successful', 'Book added to favorite')
    except:
        messagebox.showinfo('Alert Box','Error!!')
        
    
#user panel 
def panel():   
    root1 = tk.Tk()

    root = tk.Frame(root1)
    root1.title('Library Management')
    root1.geometry('800x600')

    label1 = tk.Label(root,text='Book name : ',font=('Verdana',12))
    label1.grid(row=0,column=0,pady=10)

    entry1 = tk.Entry(root,font=('Verdana',12),bd=2)
    entry1.grid(row=0,column=1,pady=10)

    label2 = tk.Label(root,text='Author name : ',font=('Verdana',12))
    label2.grid(row=1,column=0)

    entry2 = tk.Entry(root,font=('Verdana',12),bd=2)
    entry2.grid(row=1,column=1,pady=8)

    label3 = tk.Label(root,text='Publisher : ',font=('Verdana',12))
    label3.grid(row=0,column=2,pady=10,padx=15)

    entry3 = tk.Entry(root,font=('Verdana',12),bd=2)
    entry3.grid(row=0,column=3,pady=10)

    label4 = tk.Label(root,text='Keywords : ',font=('Verdana',12))
    label4.grid(row=1,column=2,pady=10,padx=15)

    entry4 = tk.Entry(root,font=('Verdana',12),bd=2)
    entry4.grid(row=1,column=3,pady=10)
    root.pack(pady=10)

    label5 = tk.Label(root,text='Sort by : ',font=('Comic Sans',10,'bold italic'))
    label5.grid(row=2,column=0,pady=10,padx=15)

    var = tk.IntVar()
    r1 = tk.Radiobutton(root, text='Author',font=('Comic Sans',10,'bold'), variable=var,value=1)
    r1.grid(row=2, column=1)

    r2 = tk.Radiobutton(root, text='Publisher',font=('Comic Sans',10,'bold'), variable=var,value=2)
    r2.grid(row=2, column=2)

    r3 = tk.Radiobutton(root, text='Issued',font=('Comic Sans',10,'bold'), variable=var,value=3)
    r3.grid(row=2, column=3)
    
    #textarea
    frame1 = tk.Frame(root1)
    text=tkst.ScrolledText(master = frame1,width  = 67,height = 20,
                           font=('Verdana',11))
    text.grid(row=0,column=1)
    frame1.pack(expand = tk.YES,padx=15)
    
    #submit
    #submit = tk.Button(root,text='List Books',bd=3,font=('Cambria',12,'bold'), command=lambda:get_values(lab1='',lab2='',lab3='',lab4='',var,entry1,text))
    submit = tk.Button(root,text='List Books',bd=3,font=('Cambria',12,'bold'), command=lambda:get_values(entry1, entry2, entry3, entry4, var, text))
    submit.grid(row=3,column= 1, pady=10)
    
    #iframe= Frame(root1)
    issue = tk.Button(root, text = 'Issue', bd=3, font=('Cambria',12,'bold'), command = lambda:issued_book(entry1))
    issue.grid(row=3, column= 2, pady=10)
    #iframe.pack()
    
    returned = tk.Button(root, text = 'Return', bd=3, font=('Cambria',12,'bold'), command = lambda:returned_book(entry1))
    returned.grid(row=3,column= 3, pady=10)
    
    fav= tk.Button(root, text = 'Add to favorites', bd=3, font=('Cambria',12,'bold'), command = lambda:favorite(entry1))
    fav.grid(row= 3, column= 4, pady= 10)
    
    #iframe.pack()

    root.mainloop()
    
localtime = time.asctime( time.localtime(time.time()) )
localtime=localtime.split()
x=localtime[1]+' '+localtime[2]+', '+localtime[-1]
localtime.pop(1)
localtime.pop(1)
localtime.pop(-1)
localtime.insert(1,x)
x=localtime[2][:5]
localtime.pop(-1)
localtime.insert(2,x)
localtime=', '.join(localtime)

root = tk.Tk()
root.configure(bd=4, relief = tk.SOLID)
root.title('Login Window')
root.geometry('700x500')

def close_win():
    root.destroy()

def neww():
    newwin = tk.Toplevel(root)

def login():
    global iduser
    db=sql.connect(host='localhost',user='root',passwd='',db='library')
    cursor=db.cursor()
    
    user_id=entry1.get()
    user_id=user_id.lower()
    pass1=entry2.get()

    try:
        query="select user_id, password from login_details where user_id='{}'" .format(user_id)
        cursor.execute(query)
        pass2=cursor.fetchone()
        user_id=pass2[0]
        pass2=pass2[1]
        
        if pass1==pass2:
            query="update login_details set login_time = NOW() where user_id='{}'".format(user_id)
            #query="insert into login_details VALUES ('{}',NOW())".format(user_id)
            cursor.execute(query)
            db.commit()
            db.close()
            root.destroy()
            iduser= user_id
            panel()
        elif pass1!=pass2:
            messagebox.showinfo('Alert Box','Login Credentials not matched!!')
    except:
        messagebox.showinfo('Alert Box','Error!!')
        

root1 = tk.Frame(root, width = 100, height = 100)
label1 = tk.Label(root1, text = ' Login into Library ', bg = 'purple', fg ='white', font = ('Comic sans',15,'bold'),relief=tk.SUNKEN, height=2,width=18,bd=4)
label1.pack()
label1 = tk.Label(root1,text='\n'+localtime,\
             font=('Comic sans',15))
label1.pack()
root1.pack(fill= tk.X, pady=80)

root2 = tk.Frame(root,width=100,height=50)
label2 = tk.Label(root2,text='UserID : ',font=('Verdana',12,'bold'))
label2.pack(side = tk.LEFT)

entry1 = tk.Entry(root2,font=('Verdana',12),bd=2)
entry1.pack(side = tk.LEFT)
root2.pack(fill = tk.X, padx=190)

root3 = tk.Frame(root,width=100,height=100)
label3 = tk.Label(root3,text='Password : ',font=('Verdana',12,'bold'))
label3.pack(side = tk.LEFT)

entry2 = tk.Entry(root3,font=('Verdana',12),bd=2)
entry2.pack(side = tk.LEFT)
root3.pack(fill = tk.X, pady=15,padx=194)

root4 = tk.Frame(root,width=100,height=100,bd=4)
submit = tk.Button(root4,text='Login',font=('Verdana',12,'bold'),command=login,\
              bg='yellow',fg='black',width=5)
submit.grid(row=0,column=0)
submit = tk.Button(root4,text='Exit',font=('Verdana',12,'bold'),\
              bg='blue',fg='white',width=5,command=close_win)
submit.grid(row=0,column=3,padx=50)
root4.pack(fill = tk.X, pady=20,padx=250)

root.mainloop()

#panel()
