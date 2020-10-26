from tkinter import *

import tkinter.font as font
import cx_Oracle
import tkinter.messagebox as Messagebox
main=Tk()

main.geometry("1000x300")
main.resizable(height=False ,width=False)

#########################################################
photo = PhotoImage(file='submit.png')
photo=photo.subsample(4,6)

chkin_butt=PhotoImage(file='chkbtn.png')
chkin_butt=chkin_butt.subsample(2,3)

#R e G I S T R A T I O N
background_image=PhotoImage(file='bg.png')
background_label = Label(main, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def new_reg():
    window=Toplevel()
    window.geometry("700x600")

    
    #Label
    #tagtxt=Text(window,height=1,width=30)
    #tagtxt.insert(END,"New Customer Check-In")
    #tagtxt.place(x=200,y=0)
    tag2=Label(window,text="New Customer Check-In")
    tag2.place(x=200,y=0)
    tag2.config(font=("Times", 22,'bold'))

    name=Label(window,text="Name*")
    name.place(x=100,y=40)
    name.config(font=("Courier", 14,'bold'))

    fname=Label(window,text="Father's Name*")
    fname.place(x=100,y=70)
    fname.config(font=("Courier", 14,'bold'))

    id=Label(window,text="ID Number*")
    id.place(x=100,y=100)
    id.config(font=("Courier", 14,'bold'))

    room_no=Label(window,text="Room No.")
    room_no.place(x=100,y=130)
    room_no.config(font=("Courier", 14,'bold'))

    mob=Label(window,text="Mobile Number*")
    #mob1=Label(window,text="(This will be your Ac. No.)")
    mob.place(x=100,y=160)
    #mob1.place(x=255,y=165)
    #mob1.config(font=("bold",6))
    mob.config(font=("Courier", 14,'bold'))

    address=Label(window,text="Address")
    address.place(x=100,y=190)
    address.config(font=("Courier", 14,'bold'))

    book_id=Label(window,text="Booking ID")
    book_id.place(x=100,y=220)
    book_id.config(font=("Courier", 14,'bold'))

    chkin_date=Label(window,text="Check-In Date(DDMMYYY)")
    chkin_date.place(x=100,y=250)
    chkin_date.config(font=("Courier", 14,'bold'))

    #E n t r y

    name_entry=Entry(window)
    name_entry.place(x=350,y=40)

    fname_entry=Entry(window)
    fname_entry.place(x=350,y=70)

    id_entry=Entry(window)
    id_entry.place(x=350,y=100)

    room_no_entry=Entry(window)
    room_no_entry.place(x=355,y=130)

    mob_entry=Entry(window)
    mob_entry.place(x=350,y=160)

    address_entry=Entry(window,width=50)
    address_entry.place(x=350,y=190)

    book_id_entry=Entry(window)
    book_id_entry.place(x=350,y=220)

    chkin_date_entry=Entry(window)
    chkin_date_entry.place(x=350,y=250)

    def add():
        name=name_entry.get()
        fname=fname_entry.get()
        id=id_entry.get()
        room_no=room_no_entry.get()
        mob=mob_entry.get()
        address=address_entry.get()
        book_id=book_id_entry.get()
        chkin_date=chkin_date_entry.get()

        con=cx_Oracle.connect('pythonhol/12345@localhost')
        cursor=con.cursor()
        query="SELECT MAX(book_id) from oldcust"
        cursor.execute(query)
        result=cursor.fetchall()
        result=result[0][0]
        if result==None:
            result=1
        else:
            result=int(result)+1
        cursor.close()
        con.commit()
        con.close()
        tupl=(name,fname,id,room_no,mob,address,result,chkin_date)
        data=[]
        data.append(tupl)
        if len(str(name))==0 or len(str(room_no))==0 or len(str(mob))==0 or len(str(fname))==0 or len(str(id))==0:
            Messagebox.showinfo("Alert","Oops! You missed some Required Details")
        else:
            con=cx_Oracle.connect('pythonhol/12345@localhost')
            cursor=con.cursor()
            cursor.bindarraysize=1
            cursor.setinputsizes(20,20,int,int,int,40,15,8)
            query="insert into createacc(name,fname,id,room_no,mob,address,book_id,chkin_date) values(:1,:2,:3,:4,:5,:6,:7,:8)"
            query2="insert into oldcust(name,fname,id,room_no,mob,address,book_id,chkin_date) values(:1,:2,:3,:4,:5,:6,:7,:8)"

            cursor.executemany(query,data)
            cursor.executemany(query2,data)
            cursor.close()
            con.commit()
            Messagebox.showinfo("Alert","Congratulations! Booking is Successful .  Bookung ID is : "+str(result))
            name_entry.delete(0,END)
            fname_entry.delete(0,END)
            id_entry.delete(0,END)
            room_no_entry.delete(0,END)
            mob_entry.delete(0,END)
            address_entry.delete(0,END)
            book_id_entry.delete(0,END)
            chkin_date_entry.delete(0,END)
            con.close()
            ##############################################
    #B u t t o n

    add=Button(window,image=photo,command=add)
    add.place(x=300,y=280)
def view():
        book_id=view_entry.get()
        con=cx_Oracle.connect('pythonhol/12345@localhost')
        cursor=con.cursor()
        cursor.execute('select * from oldcust where book_id=:book_id',{'book_id':(book_id)})
        result=cursor.fetchall()
        tags=["NAME:    ","Father's Name    : ","ID Number:    ","Room No.:    ","Mobile:    ","Address:    ","Booking ID:    ","Check-In Date:    ","Check Out Date:   ","Total Bill:    "]
        if len(result)==0:
            Messagebox.showinfo("Alert","No Data Found")
        else:
            root=Tk()
            root.title("Customer Details")
            root.geometry("600x300")
            ro=2
            for i in range(10):
                x=Label(root,text=tags[i]+str(result[0][i]))
                x.grid(row=ro,column=2,sticky=W)
                x.config(font=("Courier", 14,'bold'))
                ro+=5
        cursor.close()
        con.commit()
        con.close()
def empty():
    con=cx_Oracle.connect('pythonhol/12345@localhost')
    cursor=con.cursor()
    rooms=list(range(1,51))
    query='select distinct(room_no) from createacc'
    cursor.execute(query)
    result=cursor.fetchall()
    results=[]
    for i in range(len(result)):
        results.append(result[i][0])
    print(results)
    
    cursor.close()
    con.commit()
    root=Tk()
    root.title("Empty Rooms")
    col=2
    for i in rooms:
        if i not in results:
                x=Button(root,text=i)
                x.grid(row=2,column=col,sticky=W)
                x.config(font=("Courier", 8,'bold'))
                col+=5
    con.close()


def delete():
    con=cx_Oracle.connect('pythonhol/12345@localhost')
    cursor=con.cursor()
    book_id=book_id_entry.get()
    cursor.execute('select * from createacc')
    len1=len(cursor.fetchall())
    
    query = "delete from createacc where book_id=:book_id"
    if book_id=="":
        Messagebox.showinfo("Alert","Booking ID is Mandatory!!")
        book_id_entry.delete(0,END)
        chk_out.delete(0,END)
    else:
        cursor.execute(query,{'book_id':(book_id)})
        con.commit()
       
        book_id_entry.delete(0,END)
        chk_out.delete(0,END)
        cursor.execute('select * from createacc')
        len2=len(cursor.fetchall())
        if len2<len1:
            Messagebox.showinfo("Alert","Chck Out Successfull!!")
        else:
            Messagebox.showinfo("Alert","Invalid Booking ID")
    cursor.close()
    con.commit()
    con.close()
def bill():
    chkout_date=chk_out.get()
    book_id=book_id_entry.get()
    con=cx_Oracle.connect('pythonhol/12345@localhost')
    cursor=con.cursor()
    query='select chkin_date from createacc where book_id=:book_id'
    cursor.execute(query,{'book_id':(book_id)})
    result=cursor.fetchall()
    a=result[0][0][0:2]
    b=chkout_date[0:2]
    bill=800*(abs(int(a)-int(b)))
    Messagebox.showinfo("Alert","Total Bill: Rs"+str(bill))
    
    q1='update oldcust set chkout_date=:1 where book_id=:2'
    cursor.execute(q1,(chkout_date,book_id))
    q2='update oldcust set bill=:1 where book_id=:2'
    cursor.execute(q2,(bill,book_id))
    delete()
    cursor.close()
    con.commit()
    con.close()



    
main.title("Hotel Management")
new_cust=Button(main,image=chkin_butt,command=new_reg).place(x=50,y=58)
#line_label=Label(main,text='---------------------------------------------------------------------').place(x=1,y=33)

view_entry=Entry()
view_entry.place(x=267,y=80)
view=Button(main,text='View ',width=20,command=view).place(x=255,y=120)
#line_label2=Label(main,text='---------------------------------------------------------------------').place(x=1,y=80)

empty_rooms=Button(main,text="View",width=15,command=empty).place(x=440,y=100)
#line_label=Label(main,text='---------------------------------------------------------------------').place(x=1,y=125)
chk_out=Entry()
line_label=Label(main,text='Checkout date').place(x=590,y=105)
chk_out.place(x=590,y=70)

book_id_entry=Entry()
line_label=Label(main,text='Booking ID').place(x=730,y=105)

book_id_entry.place(x=690,y=70)
bill=Button(main,text="Generate Bill",command=bill).place(x=650,y=130)


main.mainloop()

