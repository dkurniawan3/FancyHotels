import urllib.request
import pymysql
from tkinter import *
from re import findall
from datetime import *

username = ""
availRooms = []
startDate = ""
endDate = ""
cardNo = 0
totalCost = 0
chosenRooms = []
location = ""

def enterDB():
    try:
        data = pymysql.connect(host = 'academic-mysql.cc.gatech.edu',
                               password = 'PBUiFIo8',
                               user = 'cs4400_Group_43',
                               db = 'cs4400_Group_43')
        cursor = data.cursor()
        return cursor,data
    except Exception:
        messagebox.showinfo('WARNING', 'Connection not available. Please try again later.')
        return 0,0
    
class LoginPage:

    def __init__(self, win):
        self.rootWin = win
        self.rootWin.title("Login")

        self.frame1 = Frame(self.rootWin)
        self.frame1.pack()

        self.var1 = StringVar()
        self.var2 = StringVar()

        label1 = Label(self.frame1, text = "Username")
        label1.grid(row = 0, column = 1)

        label2 = Label(self.frame1, text = "Password")
        label2.grid(row = 1, column = 1)

        e = Entry(self.frame1, text = self.var1)
        e.grid(row = 0, column = 2)

        f = Entry(self.frame1, text = self.var2, show = "*")
        f.grid(row = 1, column = 2)

        self.button1 = Button(self.frame1, text = "New User? Create Account Here", command = self.Register)
        self.button1.grid(row = 4, column = 2)

        self.button2 = Button(self.frame1, text = "Login", command = self.Login, width = 10)
        self.button2.grid(row = 4, column = 1)
        
        self.button3 = Button(self.frame1, text = "Exit", command = self.Exit, width = 4)
        self.button3.grid(row = 4, column = 3)        

    def Register(self):
        newWin = Toplevel()
        self.rootWin.withdraw()
        RegGUI = RegisterPage(newWin, self.rootWin)

    def Login(self):

        global username
        username = self.var1.get()
        self.username = self.var1.get()
        self.password = self.var2.get()

        if self.username == "" or self.password == "":
            messagebox.showwarning('Login Error', ' Please fill out all credentials.')
            return
            
        cursor,db = enterDB()
        if cursor==0:
            return

        try:
            query = """SELECT c.Username, c.Password, m.Username, m.Password
    FROM CUSTOMER as c, MANAGEMENT as m
    WHERE c.Username = '{0}' OR m.Username = '{1}'""".format(self.username, self.username)
            cursor.execute(query)
            a = cursor.fetchone()
            if a == None:
                messagebox.showwarning("Login Error", "Username/Password combination is incorrect")
                return
            if a[0] == self.username and a[1] == self.password:
                newWin = Toplevel()
                self.rootWin.withdraw()
                HomePageGUI = CustomerHomePage(newWin, self.rootWin)
            elif a[2] == self.username and a[3] == self.password:
                newWin = Toplevel()
                self.rootWin.withdraw()
                AdminPageGUI = Admin(newWin, self.rootWin)
            else:
                messagebox.showwarning("Login Error", "Username/Password combination is incorrect")
        except:
            cursor.close()
            db.close()
            messagebox.showerror("Error!", "This Username/Password combination is incorrect")

        cursor.close()
        db.close()
            
    def Exit(self):
        self.rootWin.destroy()

class RegisterPage:

    def __init__(self, win, oldRoot):
        self.rootWin = win
        self.rootWin.title("New User Registration")
        self.oldRoot=oldRoot
        
        self.frame1 = Frame(self.rootWin)
        self.frame1.pack()

        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var3 = StringVar()
        self.var4 = StringVar()

        label1 = Label(self.frame1, text = "Username")
        label1.grid(row = 0, column = 1)

        label2 = Label(self.frame1, text = "Password")
        label2.grid(row = 1, column = 1)

        label3 = Label(self.frame1, text = "Confirm Password")
        label3.grid(row = 2, column = 1)

        label4 = Label(self.frame1, text = "Email")
        label4.grid(row = 3, column = 1)

        e = Entry(self.frame1, text = self.var1)
        e.grid(row = 0, column = 2)

        f = Entry(self.frame1, text = self.var2,show='*')
        f.grid(row = 1, column = 2)
        
        g = Entry(self.frame1, text = self.var3,show='*')
        g.grid(row = 2, column = 2)
        
        h = Entry(self.frame1, text = self.var4)
        h.grid(row = 3, column = 2)

        self.button1 = Button(self.frame1, text = "Register", command = self.Registering)
        self.button1.grid(row = 4, column = 2)

        self.button2 = Button(self.frame1, text = "Cancel", command = self.Cancel)
        self.button2.grid(row = 4, column = 1)

    def checkPassword(self):
        pwd=self.var2.get()
        reg1 = '[a-zA-Z0-9]*[A-Z]+[a-zA-Z0-9]*' #check 1 uppercase
        reg = '[a-zA-Z0-9]*[0-9]+[a-zA-Z0-9]*' #check 1 number
        search1 = findall(reg1,pwd)
        search2 = findall(reg,pwd)
        if len(search1)==0 or len(search2)==0:
            return False
        elif search1[0]==pwd and search2[0]==pwd:
            return True
        else:
            return False

    def checkEmail(self):
        email = self.var4.get()
        regx = '[a-zA-Z0-9]+\@[a-zA-Z0-9]+\.[a-zA-Z]{3}'
        search1 = findall(regx, email)

        cursor,db = enterDB()
        if cursor == 0:
            return
        query2 = "SELECT * FROM CUSTOMER WHERE Email='{0}'".format(email)
        cursor.execute(query2)
        b = cursor.fetchone()
        
        if len(search1) == 0:
            return 1
        elif b != None:
            return 2
        else:
            return 3

        cursor.close()
        db.close()

    def Registering(self):
        global username
        username = self.var1.get()
        user = self.var1.get()
        pwd1=self.var2.get()
        pwd2=self.var3.get()
        email = self.var4.get()

        if pwd1!=pwd2:
            messagebox.showwarning('Invalid password', 'Passwords do not match! Please re-enter the passwords.')
            return
        elif not(self.checkPassword()):
            messagebox.showwarning('Invalid password', 'Passwords must contain at least 1 uppercase letter and at least 1 number!')
            return
        if len(user)>15 or len(user) == 0:
            messagebox.showwarning('Invalid Username', 'Username must be between 1-15 characters')
            return
        if self.checkEmail() == 1:
            messagebox.showwarning('Invalid Email', 'Please enter a valid email')
            return
        if self.checkEmail() == 2:
            messagebox.showwarning('Invalid Email', 'This email already exists')
            return
        cursor,db = enterDB()
        if cursor==0:
            return

        query = "SELECT * FROM CUSTOMER WHERE Username='{0}'".format(user)

        cursor.execute(query)
 
        a = cursor.fetchone()
        if a == None:
            try:
                cursor.close()
                cursor=db.cursor()
                adduserQ = "INSERT INTO CUSTOMER VALUES ('{0}','{1}','{2}')".format(user, pwd1, email)
                cursor.execute(adduserQ)
                db.commit()
                messagebox.showinfo('Welcome!', 'Registration was successful!')
                self.rootWin.withdraw()
                newWin = Toplevel()
                HomePageGUI = CustomerHomePage(newWin, self.rootWin)
            except TypeError:
                messagebox.showwarning('An error occurred. Please check internet connection')
            except:
                messagebox.showwarning('Registration Failure', 'Registration unsuccessful. Try again.')
        else:
            messagebox.showwarning('Invalid username!', 'Sorry, that username is already taken')
        
        cursor.close()
        db.close()

            
    def Cancel(self):
        self.oldRoot.deiconify()
        self.rootWin.destroy()

class CustomerHomePage: #need to adjust based on customers or management
    
    def __init__(self, win, oldRoot):
        self.rootWin = win
        self.rootWin.title("New User Registration")
        self.oldRoot=oldRoot

        self.frame1 = Frame(self.rootWin)
        self.frame1.grid(row = 0, column = 1)
        self.frame2 = Frame(self.rootWin)
        self.frame2.grid(row = 0, column = 2)

        label1 = Label(self.frame1, text = "Welcome")
        label1.grid(row = 0, column = 0)
        
        self.button1 = Button(self.frame1, text = "Make a new reservation", command = self.makeReservation, width = 20)
        self.button1.grid(row = 1, column =1)

        self.button2 = Button(self.frame1, text = "Update your reservation", command = self.updateReservation, width = 20)
        self.button2.grid(row = 2, column = 1)
        
        self.button3 = Button(self.frame1, text = "Cancel Reservation", command = self.cancelReservation, width = 20)
        self.button3.grid(row = 3, column = 1)

        self.button4 = Button(self.frame1, text = "Provide feedback", command = self.giveFeedback, width = 20)
        self.button4.grid(row = 4, column = 1)
        
        self.button5 = Button(self.frame1, text = "View feedback", command = self.viewFeedback, width = 20)
        self.button5.grid(row = 5, column = 1)

        self.button6 = Button(self.frame1, text = "Log out", command = self.back, width = 20)
        self.button6.grid(row = 6, column = 1)
        
    def back(self):
        self.rootWin.destroy()
        win = Tk()
        LoginPage(win)
        win.mainloop()
    def makeReservation(self):
        newWin = Toplevel()
        self.rootWin.withdraw()
        SearchGUI = SearchRooms(newWin, self.rootWin)

    def updateReservation(self):
        newWin = Toplevel()
        self.rootWin.iconify()
        updateGUI = UpdateReservation(newWin, self.rootWin)
        

    def cancelReservation(self):
        newWin = Toplevel()
        self.rootWin.iconify()
        cancelGUI = CancelReservation(newWin, self.rootWin)

    def giveFeedback(self):
        newWin = Toplevel()
        self.rootWin.iconify()
        giveGUI = GiveReview(newWin, self.rootWin)

    def viewFeedback(self):
        newWin = Toplevel()
        self.rootWin.iconify()
        viewGUI = ViewReviews(newWin, self.rootWin)

class SearchRooms:

    def __init__(self, win, oldRoot):
        self.rootWin = win
        self.rootWin.title("Search Rooms")

        self.frame1 = Frame(self.rootWin)
        self.frame1.pack()

        label1 = Label(self.frame1, text = "Location")
        label1.grid(row = 0, column = 1)
        
        self.var1 = StringVar(self.rootWin)
        self.var2 = StringVar()
        self.var3 = StringVar()
        
        drop = OptionMenu(self.frame1, self.var1, "Atlanta", "Charlotte", "Savannah", "Orlando", "Miami")
        self.var1.set('Atlanta')
        drop.grid(row = 0, column = 2)

        label2 = Label(self.frame1, text = "Start Date: ")
        label2.grid(row = 2, column = 1)

        label3 = Label(self.frame1, text = "End Date: ")
        label3.grid(row = 2, column = 3)

        label4 = Label(self.frame1, text = "Example: YYYY-MM-DD")
        label4.grid(row = 3, column = 1)

        label5 = Label(self.frame1, text = "Example: YYYY-MM-DD")
        label5.grid(row = 3, column = 3)

        e = Entry(self.frame1, text = self.var2)
        e.grid(row = 2, column = 2)

        f = Entry(self.frame1, text = self.var3)
        f.grid(row = 2, column = 4)

        self.button1 = Button(self.frame1, text = "Search", command = self.Search)
        self.button1.grid(row = 3, column = 5)

    
    def Search(self):
        global startDate
        global endDate
        global location
        
        self.location = self.var1.get()
        location = self.location
        startDate = self.var2.get()
        endDate = self.var3.get()

        start = datetime(int(startDate[0:4]), int(startDate[5:7]), int(startDate[8:10]))
        end = datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))

        today = datetime.today()

        if start < today or end < today:
            messagebox.showwarning("Error", "Reservation dates have to be in the future")
            return

        if end <= start:
            messagebox.showwarning("Error", "End date has to be after start date.")
            return
        
        query = """SELECT RoomNo, Category, PeopleNo, Cost, ExtraCost
FROM ROOM
WHERE Location = '{2}'
AND RoomNo NOT IN (	SELECT RoomNo 
			FROM ROOM_RESERVATION left join RESERVATION
                        ON ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
		        WHERE 0 < DATEDIFF(EndDate, '{0}') AND 0 > DATEDIFF(StartDate, '{1}') AND Location = '{2}' AND Canceled = 0
		)""".format(startDate, endDate, self.location) 

        cursor, db = enterDB()
        if cursor == 0:
            return

        cursor.execute(query)
        global availRooms
        availRooms = []
        tempRooms = cursor.fetchall()
        for room in tempRooms:
            temp = ()
            for i in range(len(room)):
                if room[i] is not str:
                    t = str(room[i])
                    temp += (t,)
                else:
                    temp += (room[i],)
            availRooms += (temp,)
        cursor.close()
        db.close()

        newWin = Toplevel()
        self.rootWin.withdraw()
        MRGUI = MakeReservation(newWin, self.rootWin)

class MakeReservation:

    def __init__(self, win, oldRoot):

        global availRooms
        global startDate
        global endDate
        
        self.rootWin = win
        self.rootWin.title("Make a Reservation")
        
        self.frame1 = Frame(self.rootWin)
        self.frame1.pack(anchor = N)
        Label(self.frame1,text="Room Number").grid(row=1,column=1)
        Label(self.frame1,text="Room Category").grid(row=1,column=2)
        Label(self.frame1,text="Number of people Allowed").grid(row=1,column=3)
        Label(self.frame1,text="Cost per Day").grid(row=1,column=4)
        Label(self.frame1,text="Cost of Extra Bed").grid(row=1,column=5)
        self.listbox = Listbox(self.frame1, width = 100, selectmode=MULTIPLE)
        for row in availRooms:
            self.listbox.insert(END, self.test(row[0],40) + self.test(row[1], 40) + self.test(row[2], 40) + self.test(row[3], 40) + self.test(row[4], 40))

        self.listbox.grid(row = 2, column = 1, columnspan=5)

        self.button1 = Button(self.frame1, text = "Check Details", command = self.checkDetails)
        self.button1.grid(row = 3, column = 1,columnspan=5)

        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var3 = StringVar()
        
        self.frame2 = Frame(self.rootWin)
        self.frame3 = Frame(self.rootWin)
        self.frame4 = Frame(self.rootWin)
        Label(self.frame3,text="Room Number").grid(row=1,column=1)
        Label(self.frame3,text="Room Category").grid(row=1,column=2)
        Label(self.frame3,text="Number of people Allowed").grid(row=1,column=3)
        Label(self.frame3,text="Cost per Day").grid(row=1,column=4)
        Label(self.frame3,text="Cost of Extra Bed").grid(row=1,column=5)
        self.listbox2 = Listbox(self.frame3, width = 100)

        self.listbox2.grid(row = 2, column = 1,columnspan=5)
        
        label1 = Label(self.frame2, text = "Start Date")
        label1.grid(row = 1, column = 1)

        self.var1.set(startDate)
        self.var2.set(endDate)

        e = Entry(self.frame2, text = self.var1)
        e.config(state = DISABLED)
        e.grid(row = 2, column = 1)

        label2 = Label(self.frame2, text = "End Date")
        label2.grid(row = 1, column = 2)

        f = Entry(self.frame2, text = self.var2)
        f.config(state = DISABLED)
        f.grid(row = 2, column = 2)

        label3 = Label(self.frame2, text = "Total Cost")
        label3.grid(row = 3, column =1)

        label4 = Label(self.frame2, text = "Use Card")
        label4.grid(row = 4, column = 1)

        cursor,db = enterDB()
        if cursor==0:
            return

        query1 = "SELECT CardNo FROM PAYMENT_INFO WHERE Username = '{0}'".format(username)
        cursor.execute(query1)
        self.cards = cursor.fetchall()
        cursor.close()
        db.close()

        self.cardTuple = ()
        if len(self.cards) == 0:
                self.cardTuple += ("Please add a credit card",)
        elif len(self.cards) != 0:
            for card in self.cards:
                last = card[0][12:16]
                self.cardTuple += (last,)
    

        g = Entry(self.frame2, text = self.var3)
        g.config(state = DISABLED)
        g.grid(row = 3, column = 2)           
            
        self.var12=StringVar()
        self.var12.set(self.cardTuple[0])
        drop = OptionMenu(self.frame2, self.var12, *self.cardTuple)
        drop.grid(row = 4, column = 2)

        self.button = Button(self.frame2, text = "Submit", command = self.Submit)
        self.button.grid(row = 5, column = 2)

        self.button = Button(self.frame2, text = "Edit/Add Card", command = self.AddCard)
        self.button.grid(row = 4, column = 3)

    def ExtraCalculate(self):
        global startDate
        global endDate
        global totalCost
        global chosenRooms
        global location
        
        total = 0
        totalCost = 0
        chosenRooms = []
        
        start = datetime(int(startDate[0:4]), int(startDate[5:7]), int(startDate[8:10]))
        end = datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))
        
        numDays = (end - start).days
        
        extraCost = 0
        regCost = 0
        for key, value in self.roomNos.items():
            state = value.get()
            if state != 0:
                for room in range(len(availRooms)):
                    if availRooms[room][0] == key:
                        extraCost += int(availRooms[room][-1])
        for key in self.roomNos:
            for r in range(len(availRooms)):
                if availRooms[r][0] == key:
                    regCost += int(availRooms[r][-2])

        for key, value in self.roomNos.items():
            state = value.get()
            for room in range(len(availRooms)):
                if availRooms[room][0] == key:
                    if state == 0:
                        chosenRooms.append((key, location, 0))
                        break
                    elif state != 0:
                        chosenRooms.append((key, location, 1))
                        break
                    

        total = (extraCost + regCost)*numDays
        self.var3.set(total)
        totalCost = int(total)


    def checkDetails(self):
        self.frame4.destroy()
        self.frame4 = Frame(self.rootWin)

        label5 = Label(self.frame4, text = "Which rooms would you like an extra bed in?")
        label5.grid(row = 0, column = 6)

        self.button = Button(self.frame4, text = "Calculate Total Cost", command = self.ExtraCalculate)
        self.button.grid(row = 0, column = 7)

        indices = self.listbox.curselection()
        self.roomNos = {}
        i=1
        for index in indices:
            roomNo = availRooms[index][0]
            self.roomNos[roomNo] = 0

        for item in self.roomNos:
            self.roomNos[item] = IntVar()
            c = Checkbutton(self.frame4, text = item, variable = self.roomNos[item])
            c.grid(row = i, column = 6)
            i += 1
        self.frame4.pack(side = BOTTOM)
        
        
        if len(self.listbox.curselection()) == 0:
            messagebox.showerror("Oops", "No Rooms are Selected")
            return None;
        self.listbox2.delete(0,END)
        for row in self.listbox.curselection():
            self.listbox2.insert(END, self.listbox.get(row))
        self.frame3.pack()
        self.frame2.pack(anchor = S)

    def test(self, aString, length):
        newString = aString + (length - len(aString))*"."
        return newString

    def Submit(self):
        global cardNo
        global startDate
        global endDate
        global totalCost
        
        try:
            smallCard = int(self.var12.get())
            for card in self.cards:
                if smallCard == int(card[0][12:16]):
                    cardNo = int(card[0])
        except:
            messagebox.showwarning("Error", "Please add a credit card to pay with.")
            self.AddCard()
            return

        self.ExtraCalculate()
        
        newWin = Toplevel()
        self.rootWin.withdraw()
        confirmGUI = ConfirmRegistration(newWin, self.rootWin, cardNo, startDate, endDate, totalCost)

    def AddCard(self):
        self.ExtraCalculate()
        
        newWin = Toplevel()
        self.rootWin.destroy()
        paymentGUI = PaymentInfo(newWin, self.rootWin)

class ConfirmRegistration:

    def __init__(self, win, oldRoot, CardNo, StartDate, EndDate, TotalCost):

        global username
        global startDate
        global endDate
        global chosenRooms
        
        self.rootWin = win
        self.rootWin.title("Confirm your registration")

        self.var1 = StringVar()

        r = Entry(self.rootWin, text = self.var1)
        r.grid(row = 0, column = 1)
        r.config(state = DISABLED)

        label = Label(self.rootWin, text = "Please save your reservation ID")
        label.grid(row = 0, column = 0)

        cursor,db = enterDB()
        if cursor==0:
            return

        query1 = "SELECT MAX(ReservationID)+1 FROM RESERVATION"
        cursor.execute(query1)
        a = cursor.fetchone()
        cursor.close()
        db.close()

        reservationID = a[0]
        self.var1.set(reservationID)

        cursor,db = enterDB()
        if cursor==0:
            return

        query2 = "INSERT INTO RESERVATION VALUES ({0}, '{1}', {2}, '{3}', '{4}', {5}, 0)".format(reservationID, username, CardNo, startDate, endDate, TotalCost)
        cursor.execute(query2)
        db.commit()
        cursor.close()
        db.close()

        for room in chosenRooms:
            cursor,db = enterDB()
            if cursor==0:
                return

            query = "INSERT INTO ROOM_RESERVATION VALUES ({0}, '{1}', {2}, {3})".format(room[0], room[1], reservationID, room[2])
            cursor.execute(query)
            db.commit()
            cursor.close()
            db.close()

class PaymentInfo:

    def __init__(self, win, oldRoot):
        global username
        
        self.rootWin = win
        self.rootWin.title("Payment Information")
     
        self.oldRoot = oldRoot

        self.frame1 = Frame(self.rootWin)
        self.frame1.pack(side = LEFT)

        label = Label(self.frame1, text = "Add Card Info")
        label.grid(row = 0, column = 0)

        label1 = Label(self.frame1, text = "Name on Card")
        label1.grid(row = 1, column = 1)

        label2 = Label(self.frame1, text = "Card Number (16 digits)")
        label2.grid(row = 2, column = 1)

        label3 = Label(self.frame1, text = "Expiration Date YYYY-MM-DD")
        label3.grid(row = 3, column = 1)

        label4 = Label(self.frame1, text = "CVV (3 digits) ")
        label4.grid(row = 4, column = 1)
        
        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var3 = StringVar()
        self.var4 = StringVar()
        
        e = Entry(self.frame1, text = self.var1)
        e.grid(row = 1, column = 2)

        f = Entry(self.frame1, text = self.var2)
        f.grid(row = 2, column = 2)

        g = Entry(self.frame1, text = self.var3)
        g.grid(row = 3, column = 2)

        h = Entry(self.frame1, text = self.var4)
        h.grid(row = 4, column = 2)

        self.button1 = Button(self.frame1, text = "Save Card", command = self.Save)
        self.button1.grid(row = 5, column = 2)

        self.button2 = Button(self.frame1, text = "Use Card for reservation", command = self.Confirm)
        self.button2.grid(row = 5, column = 3)

        self.frame2 = Frame(self.rootWin)
        self.frame2.pack(side = RIGHT)

        self.var12 = StringVar()

        label1 = Label(self.frame2, text = "Delete Card")
        label1.grid(row = 0, column = 1)

        label1 = Label(self.frame2, text = "Card Number")
        label1.grid(row = 1, column = 1)

        cursor,db = enterDB()
        if cursor==0:
            return

        query1 = "SELECT CardNo FROM PAYMENT_INFO WHERE Username = '{0}'".format(username)
        cursor.execute(query1)
        self.cards = cursor.fetchall()
        cursor.close()
        db.close()

        cardTuple = ()
        if len(self.cards) == 0:
                cardTuple += ("Please add a credit card",)
        elif len(self.cards) != 0:
            for card in self.cards:
                last = card[0][12:16]
                cardTuple += (last,)

        self.var12.set(cardTuple[0])
        drop = OptionMenu(self.frame2, self.var12, *cardTuple)
        drop.grid(row = 1, column = 2)

        self.button1 = Button(self.frame2, text = "Delete", command = self.Delete)
        self.button1.grid(row = 2, column = 2)

    def checkCreditCard(self):
        nameoncard = self.var1.get()
        cardNo = self.var2.get()
        regex1 = '[0-9]{16}'
        CVV = self.var4.get()
        regex2 = '[0-9]{3}'
        expDate = self.var3.get()
        regex3 = '\d{4}-\d{2}-\d{2}'

        today = datetime.now()

        if len(expDate) == 0:
            return
        elif len(cardNo) == 0 or len(cardNo) > 16 or len(cardNo) < 16:
            return
        elif len(CVV) == 0 or len(CVV) > 3:
            return
        elif len(nameoncard) == 0:
            return
        exp = datetime(int(expDate[0:4]), int(expDate[5:7]), int(expDate[8:10]))

        if today >= exp:
            messagebox.showwarning("Card Error", "This card is expired")
            return

        search1 = findall(regex1, cardNo)
        search2 = findall(regex2, CVV)
        search3 = findall(regex3, expDate)

        if len(search1) == 0 or len(search2) == 0 or len(search3) == 0:
            return False
        else:
            return True
            
    def Save(self):
        global username
        global cardNo

        if not(self.checkCreditCard()):
            messagebox.showwarning('Invalid Card', 'Please fill out the information correctly')
            return
        
        nameoncard = self.var1.get()
        cardNo = self.var2.get()
        expDate = self.var3.get()
        CVV = self.var4.get()
        
        bl= messagebox.askyesno("Confirmation", "Do you wish to add this card? You will be returned to the welcome page.")
        if bl:
            cursor,db = enterDB()
            if cursor==0:
                return
            
            adduserQ = "INSERT INTO PAYMENT_INFO VALUES ('{0}','{1}','{2}', '{3}', '{4}')".format(cardNo, username, nameoncard, expDate, CVV)
            cursor.execute(adduserQ)
            db.commit()

            cursor.close()
            db.close()

            newWin = Toplevel()
            self.rootWin.destroy()
            self.rootWin = ""
            HomePageGUI = CustomerHomePage(newWin, self.rootWin)

    def Confirm(self):
        global username
        global cardNo
        global startDate
        global endDate
        global totalCost

        if not(self.checkCreditCard()):
            messagebox.showwarning('Invalid Card', 'Please fill out the information correctly')
            return
        
        nameoncard = self.var1.get()
        cardNo = self.var2.get()
        expDate = self.var3.get()
        CVV = self.var4.get()

        bl= messagebox.askyesno("Confirmation", "Do you wish to add this card and use it to pay? Your total cost is {0}.".format(totalCost))
        if bl:
            cursor,db = enterDB()
            if cursor==0:
                return
            adduserQ = "INSERT INTO PAYMENT_INFO VALUES ('{0}','{1}','{2}', '{3}', '{4}')".format(cardNo, username, nameoncard, expDate, CVV)
            cursor.execute(adduserQ)
            db.commit()

            cursor.close()
            db.close()

            newWin = Toplevel()
            self.rootWin.destroy()
            confirmGUI = ConfirmRegistration(newWin, self.rootWin, cardNo, startDate, endDate, totalCost)
            
    def Delete(self):
        global username

        cardNo = 0

        try:
            smallCard = int(self.var12.get())
            for card in self.cards:
                if smallCard == int(card[0][12:16]):
                    cardNo = int(card[0])

            cursor,db = enterDB()
            if cursor==0:
                return

            query1 = """SELECT DISTINCT p.CardNo
    FROM PAYMENT_INFO as p
    WHERE p.CardNo NOT IN (SELECT RESERVATION.CardNo
        FROM RESERVATION inner join PAYMENT_INFO
        ON RESERVATION.Username = PAYMENT_INFO.Username
        WHERE RESERVATION.Canceled = 0 AND RESERVATION.StartDate >= CURDATE()
    )AND p.Username = '{0}'""".format(username)
            cursor.execute(query1)
            unusedCards = cursor.fetchall()
            cursor.close()
            db.close()

            for i in unusedCards:

                if int(cardNo) == int(i[0]):
                    cursor,db = enterDB()
                    if cursor==0:
                        return

                    query1 = "DELETE FROM PAYMENT_INFO WHERE CardNo = {0} AND Username = '{1}'".format(cardNo, username)
                    cursor.execute(query1)
                    db.commit()
                    cursor.close()
                    db.close()
                    
                    messagebox.showinfo("Success!", "Card has been deleted")
                    newWin = Toplevel()
                    self.rootWin.destroy()
                    self.rootWin = ""
                    HomePageGUI = CustomerHomePage(newWin, self.rootWin)
                    return
            
             
            messagebox.showwarning("Error", "This card is being used for a reservation.")
        except:
            messagebox.showwarning("Error", "No credit card to delete")
            return 
                
class UpdateReservation:
    def __init__(self, win, oldRoot):
        self.master = win
        self.rootWin = oldRoot
        self.master.title("Update Reservation")

        self.frame1 = Frame(self.master)
        self.frame2 = Frame(self.master)
        self.frame3 = Frame(self.master)

        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var3 = StringVar()
        self.var4 = StringVar()
        self.var5 = StringVar()
        self.var6 = StringVar()

        Label(self.frame1, text = "Reservation ID").grid(row=0,column=0)
        self.E1 = Entry(self.frame1, textvariable = self.var1)
        self.B1 = Button(self.frame1, text = "Search", command = self.search)
        self.B4 = Button(self.frame1, text = "Go back to functionality tab", command = self.back)
        self.B4.grid(row=0, column=3)
        self.E1.grid(row=0, column=1)
        self.B1.grid(row=0, column=2)

        Label(self.frame2, text = "Current Start Date").grid(row=0, column=0)
        Label(self.frame2, text = "Current End Date").grid(row=0, column=2)
        Label(self.frame2, text = "New Start Date").grid(row=1, column=0)
        Label(self.frame2, text = "New End Date").grid(row=1, column=2)

        self.E2 = Entry(self.frame2, textvariable = self.var2,state="readonly")
        self.E3 = Entry(self.frame2, textvariable = self.var3,state="readonly")
        self.E4 = Entry(self.frame2, textvariable = self.var4)
        self.E5 = Entry(self.frame2, textvariable = self.var5)
        self.B2 = Button(self.frame2, text = "Search Availability", command = self.searchAvail)

        self.E2.grid(row=0, column=1)
        self.E3.grid(row=0, column=3)
        self.E4.grid(row=1, column=1)
        self.E5.grid(row=1, column=3)
        self.B2.grid(row=2, column=0, columnspan=4)

        Label(self.frame3,text="Room Number").grid(row=1,column=1)
        Label(self.frame3,text="Room Category").grid(row=1,column=2)
        Label(self.frame3,text="Number of people Allowed").grid(row=1,column=3)
        Label(self.frame3,text="Cost per Day").grid(row=1,column=4)
        Label(self.frame3,text="Cost of Extra Bed").grid(row=1,column=5)
        Label(self.frame3,text="Extra Bed?").grid(row=1,column=6)
        self.listbox = Listbox(self.frame3, width = 100, selectmode=SINGLE)
        self.listbox.grid(row=2,column=1,columnspan=6)
        self.E6 = Entry(self.frame3, textvariable = self.var6,state="readonly")
        Label(self.frame3,text="Total Cost").grid(row=3,column=3)
        self.E6.grid(row=3,column=4)
        
        self.B3 = Button(self.frame3, text="Submit Update", command = self.update)
        self.B3.grid(row=4,column=1,columnspan=5)

        self.frame1.pack()
    def back(self):
        self.master.destroy()
        self.rootWin.deiconify()
    def search(self):
        self.var2.set("")
        self.var3.set("")
        self.var4.set("")
        self.var5.set("")
        self.RID = self.var1.get()

        if self.RID == "":
            messagebox.showerror("opps", "Please Enter Reservation ID")
            return None

        cursor, db = enterDB()
        query1 = """SELECT Location FROM ROOM_RESERVATION WHERE ReservationID IN (SELECT ReservationID
                                                                                  FROM RESERVATION
                                                                                  WHERE ReservationID = {0})""".format(self.RID)
        cursor.execute(query1)
        rawLoc = cursor.fetchone()
        if rawLoc == None:
            messagebox.showerror("Error", "Reservation ID does not exist.")
            return
        else:
            self.location = rawLoc[0]

        cursor,db = enterDB()
        query = """SELECT ROOM_RESERVATION.RoomNo, ROOM.Category, ROOM.PeopleNo,ROOM.Cost,ROOM.ExtraCost,ROOM_RESERVATION.ExtraBed, RESERVATION.StartDate, RESERVATION.EndDate
 FROM ROOM left join ROOM_RESERVATION 
on ROOM.Location = ROOM_RESERVATION.Location and ROOM.RoomNo = ROOM_RESERVATION.RoomNo
left join RESERVATION 
on ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
where RESERVATION.ReservationID = {0} AND RESERVATION.StartDate >= CURDATE() AND RESERVATION.Username = '{1}' AND RESERVATION.Canceled = 0""".format(self.RID,username)
        cursor.execute(query)
        a = cursor.fetchall()
        if len(a)==0:
            messagebox.showerror("opps", "Invalid Reservation ID\nThis Might occur if one of the followings happened\n1. Reservation Startdate already passed\n2.Reservation is not made from your account.")
            return None
        self.aList=[]
        for row in a:
            self.aList.append(row[:6])
            self.var2.set(row[6])
            self.var3.set(row[7])
        cursor.close()
        db.close()
        today = datetime(date.today().year, date.today().month, date.today().day)
        today3 = today + timedelta(days=4)
        originalStart = datetime(int(self.var2.get()[:4]),int(self.var2.get()[5:7]),int(self.var2.get()[8:]))
        self.E4.config(state=NORMAL)
        if originalStart < today3:
            messagebox.showinfo("Check!", "You can only cancel your reservation if you are within 3 days of the start date.")
            return
        self.frame2.pack()
    def searchAvail(self):
        self.listbox.delete(0,END)
        if len(self.var4.get()) != 10 and re.findall('\d{4}-\d{2}-\d{2}',self.var4.get()) == []:
            messagebox.showerror("opps", "Please fill in the start date in YYYY-MM-DD format")
            return None
        if len(self.var5.get()) != 10 and re.findall('\d{4}-\d{2}-\d{2}',self.var5.get()) == []:
            messagebox.showerror("opps", "Please fill in the End date in YYYY-MM-DD format")
            return None
        today = datetime(date.today().year, date.today().month, date.today().day)
        today3 = today + timedelta(days=4)
        originalStart = datetime(int(self.var2.get()[:4]),int(self.var2.get()[5:7]),int(self.var2.get()[8:]))
        self.Start = datetime(int(self.var4.get()[:4]),int(self.var4.get()[5:7]),int(self.var4.get()[8:]))
        self.End = datetime(int(self.var5.get()[:4]),int(self.var5.get()[5:7]),int(self.var5.get()[8:]))
        if self.Start < today:
            messagebox.showerror("opps", "You cannot set the new Start date to time before today")
            return None
        if self.End <= self.Start:
            messagebox.showerror("opps", "You cannot set the new enddate before the new startdate")
            return None
        cursor,db = enterDB()
        query = """SELECT RoomNo
FROM ROOM_RESERVATION 
WHERE ReservationID  IN (	SELECT ReservationID
				FROM RESERVATION
				WHERE 0 < (SELECT DATEDIFF(EndDate, "{0}"))
				AND 0 > (SELECT DATEDIFF(StartDate, "{1}"))
				AND ReservationID != {2}
				AND Canceled = 0
			) 
AND Location = '{3}' 
AND RoomNo IN ( SELECT RoomNo 
		FROM ROOM_RESERVATION 
		WHERE ReservationID = {2})""".format(self.var4.get(),self.var5.get(),self.RID, self.location)
        cursor.execute(query)
        a = cursor.fetchall()
        if len(a) != 0:
            messagebox.showerror("opps", "Room not available in those Dates")
            return None
        self.listbox.delete(0,END)
        for row in self.aList:
            self.listbox.insert(END, self.test(str(row[0]),35) + self.test(str(row[1]), 35)
                                + self.test(str(row[2]), 35) + self.test(str(row[3]), 35)
                                + self.test(str(row[4]), 35) + self.test(str(row[5]), 35))
        aNum = 0
        for row in self.aList:
            aNum = aNum + (row[3]+(row[4]*row[5]))*(self.End-self.Start).days
        self.var6.set(aNum)
        cursor.close()
        db.close()
        self.frame3.pack()
    def update(self):
        bl= messagebox.askyesno("Confirmation?", "You are changing your date to {0} to {1}, from {2} to {3}, with updated cost of {4}. \nContinue?".format(
            self.var2.get(),self.var3.get(),self.var4.get(),self.var5.get(),self.var6.get()))
        if bl:
            cursor,db = enterDB()
            query = """UPDATE RESERVATION
    SET StartDate = '{0}', EndDate = '{1}', TotalCost = {2}
    WHERE ReservationID = {3}""".format(self.var4.get(),self.var5.get(),self.var6.get(),self.RID)
            cursor.execute(query)
            db.commit()
            cursor.close()
            db.close()
            self.master.destroy()
            self.rootWin.deiconify()
    def test(self, aString, length):
        newString = aString + (length - len(aString))*"."
        return newString

class CancelReservation:
    def __init__(self, win, oldRoot):
        self.master = win
        self.rootWin = oldRoot
        self.master.title("Cancel Reservation")

        self.frame1 = Frame(self.master)
        self.frame2 = Frame(self.master)
        self.frame3 = Frame(self.master)
        self.frame4 = Frame(self.master)

        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var3 = StringVar()
        self.var4 = StringVar()
        self.var5 = StringVar()
        self.var6 = StringVar()
        
        Label(self.frame1, text = "Reservation ID").grid(row=0,column=1)
        self.E1 = Entry(self.frame1, textvariable = self.var1)
        self.B1 = Button(self.frame1, text = "Search", command = self.search)
        self.B3 = Button(self.frame1, text = "Go Back to Functionality Tab", command= self.back)
        self.B3.grid(row=0,column=4)

        self.E1.grid(row=0, column=2)
        self.B1.grid(row=0, column=3)

        Label(self.frame2, text = "Start Date").grid(row=0, column=1)
        Label(self.frame2, text = "End Date").grid(row=0, column=3)

        self.E2 = Entry(self.frame2, textvariable = self.var2,state="readonly")
        self.E3 = Entry(self.frame2, textvariable = self.var3,state="readonly")
        self.E2.grid(row=0, column=2)
        self.E3.grid(row=0, column=4)

        Label(self.frame3,text="Room Number").grid(row=1,column=1)
        Label(self.frame3,text="Room Category").grid(row=1,column=2)
        Label(self.frame3,text="Number of people Allowed").grid(row=1,column=3)
        Label(self.frame3,text="Cost per Day").grid(row=1,column=4)
        Label(self.frame3,text="Cost of Extra Bed").grid(row=1,column=5)
        Label(self.frame3,text="Extra Bed?").grid(row=1,column=6)
        self.listbox = Listbox(self.frame3, width = 100, selectmode=SINGLE)
        self.listbox.grid(row=2,column=1,columnspan=6)

        Label(self.frame4, text = "Total Cost of Reservation").grid(row=0, column=0)
        Label(self.frame4, text = "Date of Cancellation").grid(row=1, column=0)
        Label(self.frame4, text = "Amount Refunded").grid(row=2, column=0)
        self.E4 = Entry(self.frame4, textvariable = self.var4,state="readonly")
        self.E5 = Entry(self.frame4, textvariable = self.var5,state="readonly")
        self.E6 = Entry(self.frame4, textvariable = self.var6,state="readonly")
        self.E4.grid(row=0, column=1)
        self.E5.grid(row=1, column=1)
        self.E6.grid(row=2, column=1)
        
        self.B2 = Button(self.frame4, text="Submit Cancellation", command = self.cancel)
        self.B2.grid(row=3,column=0,columnspan=2)
        self.frame1.pack()
    def back(self):
        self.master.destroy()
        self.rootWin.deiconify()
    def cancel(self):
        bl= messagebox.askyesno("Confirmation?", "You are cancelling your reservation date of {0} to {1} with refund of {2}. \nContinue?".format(
            self.var2.get(),self.var3.get(),self.var6.get()))
        if bl:
            cursor,db = enterDB()
            query = """UPDATE RESERVATION
SET Canceled=1, TotalCost = TotalCost - {0}
WHERE ReservationID = {1}""".format(self.var6.get(), self.RID)
            cursor.execute(query)
            db.commit()
            cursor.close()
            db.close()
            self.master.destroy()
            self.rootWin.deiconify()
    def search(self):
        self.listbox.delete(0,END)
        self.var2.set("")
        self.var3.set("")
        self.var4.set("")
        self.var5.set("")
        self.var6.set("")
        self.RID = self.var1.get()
        if self.RID == "":
            messagebox.showerror("opps", "Please Enter Reservation ID")
            return None
        cursor,db = enterDB()
        query = """SELECT ROOM_RESERVATION.RoomNo, ROOM.Category, ROOM.PeopleNo,ROOM.Cost,ROOM.ExtraCost,ROOM_RESERVATION.ExtraBed, RESERVATION.StartDate, RESERVATION.EndDate
 FROM ROOM left join ROOM_RESERVATION 
on ROOM.Location = ROOM_RESERVATION.Location and ROOM.RoomNo = ROOM_RESERVATION.RoomNo
left join RESERVATION 
on ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
where RESERVATION.ReservationID = {0} AND RESERVATION.StartDate >= CURDATE() AND RESERVATION.Username = '{1}' AND RESERVATION.Canceled = 0""".format(self.RID,username)
        cursor.execute(query)
        a = cursor.fetchall()
        if len(a)==0:
            messagebox.showerror("opps", "Invalid Reservation ID")
            return None
        self.aList=[]
        for row in a:
            self.aList.append(row[:6])
            self.var2.set(row[6])
            self.var3.set(row[7])
        cursor.close()
        db.close()
        for row in self.aList:
            self.listbox.insert(END, self.test(str(row[0]),35) + self.test(str(row[1]), 35)
                                + self.test(str(row[2]), 35) + self.test(str(row[3]), 35)
                                + self.test(str(row[4]), 35) + self.test(str(row[5]), 35))
        today = datetime(date.today().year, date.today().month, date.today().day)
        self.Start = datetime(int(self.var2.get()[:4]),int(self.var2.get()[5:7]),int(self.var2.get()[8:]))
        self.End = datetime(int(self.var3.get()[:4]),int(self.var3.get()[5:7]),int(self.var3.get()[8:]))
        aNum = 0
        for row in self.aList:
            aNum = aNum + (row[3]+(row[4]*row[5]))*(self.End-self.Start).days
        self.var4.set(aNum)
        self.var5.set(str(date.today()))
        if (self.Start - today).days < 2:
            self.var6.set(0)
        elif (self.Start - today).days < 4:
            self.var6.set(float(self.var4.get())*.8)
        else:
            self.var6.set(self.var4.get())
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
    def test(self, aString, length):
        newString = aString + (length - len(aString))*"."
        return newString

class GiveReview:

    def __init__(self, win, oldRoot):
        self.master = win
        self.rootWin = oldRoot
        self.master.title("Give Review")
        global username
        self.frame1 = Frame(self.master)
        self.frame1.pack()

        self.var1 = StringVar()
        self.var2 = StringVar()
        self.var3 = StringVar()

        label1 = Label(self.frame1, text = "Hotel Location")
        label1.grid(row = 0, column = 1)

        label2 = Label(self.frame1, text = "Rating")
        label2.grid(row = 1, column = 1)

        label3 = Label(self.frame1, text = "Comment")
        label3.grid(row = 2, column = 1)

        drop = OptionMenu(self.frame1, self.var1, "Atlanta", "Charlotte", "Savannah", "Orlando", "Miami")
        drop.grid(row = 0, column = 2)

        drop = OptionMenu(self.frame1, self.var2, 1,2,3,4,5)
        drop.grid(row = 1, column = 2)

        self.button1 = Button(self.frame1, text = "Submit", command = self.Submit)
        self.button1.grid(row = 4, column = 3)

        e = Entry(self.frame1, text = self.var3)
        e.grid(row = 2, column = 2)

        self.B1 = Button(self.frame1, text = "Cancel", command = self.back)
        self.B1.grid(row=4, column=4)
    def back(self):
        self.master.destroy()
        self.rootWin.deiconify()
    def Submit(self):
        bl= messagebox.askyesno("Confirmation?", "You are submitting a Review of {0} for {1} location. \nContinue?".format(
            self.var1.get(),self.var2.get()))
        if bl:
            cursor,db = enterDB()
            query = """INSERT INTO HOTEL_REVIEW
SELECT Max(ReviewNo)+1, '{0}', {1}, '{2}', '{3}' FROM HOTEL_REVIEW""".format(username,self.var2.get(),self.var3.get(),self.var1.get())
            cursor.execute(query)
            db.commit()
            cursor.close()
            db.close()
            self.master.destroy()
            self.rootWin.deiconify

class ViewReviews:
    def __init__(self, win, oldRoot):
        self.master = win
        self.rootWin = oldRoot
        self.master.title("View Review")
        
        self.frame1 = Frame(self.master)
        self.frame2 = Frame(self.master)
        self.var1 = StringVar()
        self.B1 = Button(self.frame1, text = "Check Reviews", command = self.check)
        self.E1 = OptionMenu(self.frame1, self.var1, "Atlanta", "Charlotte", "Savannah", "Orlando", "Miami")
        self.E1.grid(row=0,column=1)
        Label(self.frame1, text = "Hotel Location").grid(row=0,column=0)
        self.B1.grid(row=0,column=2)
        self.B2 = Button(self.frame2, text = "Go Back", command = self.back)
        self.B2.grid(row=0,column=3)

        Label(self.frame2, text = "Rating").grid(row=0,column=0)
        Label(self.frame2, text = "Comment").grid(row=0,column=1)
        self.listbox1 = Listbox(self.frame2)
        self.listbox2 = Listbox(self.frame2)
        self.listbox1.grid(row=1,column=0)
        self.listbox2.grid(row=1,column=1)
        self.frame1.pack()
    def back(self):
        self.master.destroy()
        self.rootWin.deiconify()
    def check(self):
        self.listbox1.delete(0,END)
        self.listbox2.delete(0,END)
        cursor,db = enterDB()
        query = """SELECT Rating, Comment
FROM HOTEL_REVIEW
WHERE Location = '{0}'""".format(self.var1.get())
        cursor.execute(query)
        a = cursor.fetchall()
        for row in a:
            self.listbox1.insert(END, row[0])
            self.listbox2.insert(END, row[1])
        cursor.close()
        db.close()
        self.frame2.pack()

class Admin:
    def __init__(self, win, oldroot):

        self.Main = win
        self.rootWin = oldroot
        self.Main.title("Admin Functionality Tab")

        Label(self.Main, text = "Welcome Admin User").grid(row=1,column=1)
        self.B1 = Button(self.Main, text = "View Reservation Report",command=self.viewReserve)
        self.B1.grid(row=2,column=1,sticky=W+S+E+N)
        self.B2 = Button(self.Main, text = "View Revenue Report",command=self.viewRevenue)
        self.B2.grid(row=3,column=1,sticky=W+S+E+N)
        self.B3 = Button(self.Main, text = "View Popular Room Category Report",command=self.viewPopular)
        self.B3.grid(row=4,column=1,sticky=W+S+E+N)
        self.B1 = Button(self.Main, text = "Quit",command=self.quit)
        self.B1.grid(row=5,column=1,sticky=W+S+E+N)
        self.Main.mainloop()

    def viewReserve(self):
        self.Main.iconify()
        self.Reserve = Toplevel()
        self.Reserve.title("View Reservation Report")
        self.LB11 = Listbox(self.Reserve, selectmode=NONE,width=50)
        self.LB11.grid(row=1,column=0)
        Label(self.Reserve, text = "Month").grid(row=0,column=0)
        self.LB12 = Listbox(self.Reserve, selectmode=SINGLE,width=50)
        self.LB12.grid(row=1,column=1)
        Label(self.Reserve, text = "Location").grid(row=0,column=1)
        self.LB13 = Listbox(self.Reserve, selectmode=SINGLE,width=50)
        self.LB13.grid(row=1,column=2)
        Label(self.Reserve, text = "Number of Reservation").grid(row=0,column=2)
        
        cursor,db = enterDB()
        query = """select EXTRACT(month FROM RESERVATION.StartDate) as month, ROOM_RESERVATION.Location as location, count(RESERVATION.StartDate) as NumofReserve
    from RESERVATION left join ROOM_RESERVATION
    On RESERVATION.ReservationID = ROOM_RESERVATION.ReservationID
    where MONTH(RESERVATION.StartDate) = 8 or MONTH(RESERVATION.StartDate) = 9
    group by ROOM_RESERVATION.Location, Month ORDER BY Month"""
        cursor.execute(query)
        a = cursor.fetchall()
        for row in a:
            self.LB11.insert(END, row[0])
            self.LB12.insert(END, row[1])
            self.LB13.insert(END, row[2])
        cursor.close()
        db.close()
        
        self.B4 = Button(self.Reserve, text = "Back to Functionality Tab", command=self.rbackf)
        self.B4.grid(row=3,column=0,sticky=W+S+E+N,columnspan=3)
    def rbackf(self):
        self.Reserve.destroy()
        self.Main.deiconify()
    
    def viewPopular(self):
        self.Main.iconify()
        self.Popular = Toplevel()
        self.Popular.title("View Popularity Table")
        self.LB2 = Listbox(self.Popular, selectmode=SINGLE)
        self.LB2.grid(row=1,column=0)
        Label(self.Popular, text = "Month").grid(row=0,column=0)
        self.LB21 = Listbox(self.Popular, selectmode=NONE,width=50)
        self.LB21.grid(row=1,column=1)
        Label(self.Popular, text = "Top-Room Category").grid(row=0,column=1)
        self.LB22 = Listbox(self.Popular, selectmode=SINGLE,width=50)
        self.LB22.grid(row=1,column=2)
        Label(self.Popular, text = "Location").grid(row=0,column=2)
        self.LB23 = Listbox(self.Popular, selectmode=SINGLE,width=50)
        self.LB23.grid(row=1,column=3)
        Label(self.Popular, text = "Total Number of Reservation").grid(row=0,column=3)

        cursor,db = enterDB()
        query = """SELECT R2.month,R3.Category,R2.Location,R2.newNum
FROM 
   (SELECT MAX(num) as newNum, location, month
   FROM
       (SELECT Count(RESERVATION.ReservationID) as num, Category, EXTRACT(month FROM RESERVATION.StartDate) as month, ROOM.location
       FROM ROOM left join ROOM_RESERVATION 
       on ROOM.Location = ROOM_RESERVATION.Location and ROOM.RoomNo = ROOM_RESERVATION.RoomNo
       left join RESERVATION on ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
       where MONTH(RESERVATION.StartDate) = 9
       group by ROOM_RESERVATION.Location, ROOM.Category,month
       order by month, ROOM.Location) as R
   group by Location) as R2,
   (SELECT Count(RESERVATION.ReservationID) as num, Category, EXTRACT(month FROM RESERVATION.StartDate) as month, ROOM.location
       FROM ROOM left join ROOM_RESERVATION 
       on ROOM.Location = ROOM_RESERVATION.Location and ROOM.RoomNo = ROOM_RESERVATION.RoomNo
       left join RESERVATION on ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
       where MONTH(RESERVATION.StartDate) = 9
       group by ROOM_RESERVATION.Location, ROOM.Category,month
       order by month, ROOM.Location) as R3
    WHERE R2.newNum = R3.num AND R2.location = R3.location
UNION
SELECT R2.month,R3.Category,R2.Location,R2.newNum
FROM 
   (SELECT MAX(num) as newNum, location, month
   FROM
       (SELECT Count(RESERVATION.ReservationID) as num, Category, EXTRACT(month FROM RESERVATION.StartDate) as month, ROOM.location
       FROM ROOM left join ROOM_RESERVATION 
       on ROOM.Location = ROOM_RESERVATION.Location and ROOM.RoomNo = ROOM_RESERVATION.RoomNo
       left join RESERVATION on ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
       where MONTH(RESERVATION.StartDate) = 8
       group by ROOM_RESERVATION.Location, ROOM.Category,month
       order by month, ROOM.Location) as R
   group by Location) as R2,
   (SELECT Count(RESERVATION.ReservationID) as num, Category, EXTRACT(month FROM RESERVATION.StartDate) as month, ROOM.location
       FROM ROOM left join ROOM_RESERVATION 
       on ROOM.Location = ROOM_RESERVATION.Location and ROOM.RoomNo = ROOM_RESERVATION.RoomNo
       left join RESERVATION on ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
       where MONTH(RESERVATION.StartDate) = 8
       group by ROOM_RESERVATION.Location, ROOM.Category,month
       order by month, ROOM.Location) as R3
    WHERE R2.newNum = R3.num AND R2.location = R3.location"""
        cursor.execute(query)
        a = cursor.fetchall()
        for row in a:
            self.LB2.insert(END, row[0])
            self.LB21.insert(END, row[1])
            self.LB22.insert(END, row[2])
            self.LB23.insert(END, row[3])
        cursor.close()
        db.close()
        
        self.B5 = Button(self.Popular, text = "Back to Functionality Tab", command=self.pbackf)
        self.B5.grid(row=2,column=0,sticky=W+S+E+N,columnspan=4)
    def vbackf(self):
        self.Revenue.destroy()
        self.Main.deiconify()

    def viewRevenue(self):
        self.Main.iconify()
        self.Revenue = Toplevel()
        self.Revenue.title("View Revenue Report")
        self.LB31 = Listbox(self.Revenue, selectmode=NONE,width=50)
        self.LB31.grid(row=1,column=0)
        Label(self.Revenue, text = "Month").grid(row=0,column=0)
        self.LB32 = Listbox(self.Revenue, selectmode=SINGLE,width=50)
        self.LB32.grid(row=1,column=1)
        Label(self.Revenue, text = "Location").grid(row=0,column=1)
        self.LB33 = Listbox(self.Revenue, selectmode=SINGLE,width=50)
        self.LB33.grid(row=1,column=2)
        Label(self.Revenue, text = "Total Revenue").grid(row=0,column=2)

        cursor,db = enterDB()
        query = """SELECT EXTRACT(month FROM RESERVATION.StartDate) as month, ROOM.Location as Location, SUM(DATEDIFF(RESERVATION.EndDate, RESERVATION.StartDate)*ROOM.Cost) 
as Cost
    FROM ROOM left join ROOM_RESERVATION 
    on ROOM.Location = ROOM_RESERVATION.Location and ROOM.RoomNo = ROOM_RESERVATION.RoomNo
    left join RESERVATION 
    on ROOM_RESERVATION.ReservationID = RESERVATION.ReservationID
    where MONTH(RESERVATION.StartDate) = 8 or MONTH(RESERVATION.StartDate) = 9
    group by ROOM_RESERVATION.Location, Month ORDER BY Month"""
        cursor.execute(query)
        a = cursor.fetchall()
        for row in a:
            self.LB31.insert(END, row[0])
            self.LB32.insert(END, row[1])
            self.LB33.insert(END, row[2])
        cursor.close()
        db.close()
                
        self.B6 = Button(self.Revenue, text = "Back to Functionality Tab", command=self.vbackf)
        self.B6.grid(row=2,column=0,sticky=W+S+E+N,columnspan=3)
    def pbackf(self):
        self.Popular.destroy()
        self.Main.deiconify()
        
    def quit(self):
        self.Main.destroy()
        self.rootWin.destroy()
        win = Tk()
        LoginPage(win)
        win.mainloop()
win = Tk()
myWin = LoginPage(win)
win.mainloop()
