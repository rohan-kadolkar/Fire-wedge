from tkinter import*
import random
import mysql.connector as mysql

#connecting python with my sql
con = mysql.connect(host='localhost',user='root',passwd='rohankadolkar')
cur = con.cursor()

def quitgame():#this will run if quit button is pressed
    gmover.destroy()
    win.destroy()
lose=False 
lscore = 0 #latest score
prevscore = 0
def moveball():#after firing, the ball will move
    global firebtn,gmover,lose,posbal,lscore,prevscore
    firebtn.destroy()
    by = -5
    bx = 0
    canvas.move(ball,bx,by)
    posbal = canvas.coords(ball)

    if posbal[1]>25:
        prevscore = lscore
        if ((posobs[0]<=posbal[0]<=posobs[2]) and(posobs[1]<=posbal[1]<=posobs[3]))or((posobs[0]<=posbal[2]<=posobs[2])and(posobs[1]<=posbal[3]<=posobs[3])) :
            lscore += 1
            scoreboard = Label(win,text='Score : %s'%(lscore),width=10,height=2,
                               font=('Ariel',10,'bold')).place(anchor='center',relx=0.5,rely=0.9)
            bax = 0
            bay = 200
            canvas.move(ball,bax,bay)
            firebtn = Button(win,text='fire',background='lightpink',activeforeground='black',width=10,height=5,command=moveball)
            firebtn.place(relx=0.8,rely=0.8)
            # Event.wait(60)    
            win.after_cancel(After)  
        After = win.after(10,moveball)
    else:
        canvas.delete(obstacle)
        lose = True
        loser()

def play1():#the structure of game is designed here
    global pname,ppaswd
    pname = naam.get()
    ppaswd = password.get()
    if pname !='' and ppaswd !='':

        global canvas,firebtn,ball,by1,by2,bx1,bx2,prevscore,lscore
        nmcanva.destroy()
        
        canvas = Canvas(win,width=600,height=400,background='lightgrey')
        canvas.pack()  
        
        #creating obstacles
        def move_obstacle(event):
            global posobs,lscore,prevscore
            
            ox = 2
            oy = 0
            canvas.move(obstacle, ox, oy) 
            posobs = canvas.coords(obstacle)      
            if posobs[0]>400:
                canvas.delete(obstacle)
                if lscore == prevscore:
                    lscore = lscore - 1
                    scoreboard = Label(win,text='Score : %s'%(lscore),width=10,height=2,
                                       font=('Ariel',10,'bold')).place(anchor='center',relx=0.5,rely=0.9)
                    prevscore = lscore
                prevscore = lscore
                obstaclecreate()     
            else:
                win.after(random.choices([7,10],[0.6,0.5]),move_obstacle,None)
        def obstaclecreate():
            global obstacle
            obsx1 = 130
            obsy1 = 80 #isko fix rakhenge
            obsx2 = random.randint(140,190)
            obsy2 = 85 #keep it fix  
            obstacle = canvas.create_rectangle(obsx1,obsy1,obsx2,obsy2,fill='darkgreen')
            move_obstacle(None)
        obstaclecreate()

        # ball creation
        bx1 = 290
        by1 = 290
        bx2 = 310
        by2 = 310
        ball = canvas.create_oval(bx1,by1,bx2,by2,fill='orange')

        #this is danger zone after touching game will over
        danger = canvas.create_rectangle(200,0,400,20,fill='red')
        for lx1 in range(200,401,5):
            dangline = canvas.create_line(lx1,20,lx1,30)

        #fire button
        firebtn = Button(win,text='fire',background='lightpink',activeforeground='black',width=10,height=5,command=moveball)
        firebtn.place(relx=0.8,rely=0.8)
    else:
        entrdet = Label(nmcanva,text='Enter details completely',background='#e9c296',foreground='red',height=1)
        entrdet.place(anchor='center',relx=0.78,rely=0.38)
def loser():
    global gmover
    if lose == True:
        gmover = Tk()
        gmover.geometry('400x200')
        gmover.config(background='#FC9E21')
        lbl = Label(gmover,text='GAME OVER!',font=("Ariel",40,'bold'),background="#FC9E21")
        lbl.place(anchor='center',relx=0.5,rely=0.2)

        scorelbl = Label(gmover,text="Your score is: %s"%(lscore),font=('ariel',15,'bold'),background='#FC9E21')
        scorelbl.place(anchor='center',relx=0.5,rely=0.5)

        quitbtn = Button(gmover,text='QUIT',background='lightpink',activeforeground='black',
                         width=14,height=1,command=quitgame,
                         font=(5))
        quitbtn.place(anchor='center',relx=0.7,rely=0.8)
        detailsbtn = Button(gmover,text='previous details',background='pink',width=14,height=1,command=showdetails,font=(5))
        detailsbtn.place(anchor='center',relx=0.3,rely=0.8)
def showdetails():
    cur.execute("create database if not exists pythongame")
    cur.execute('use pythongame')
    cur.execute('select * from pygame;')
    displaydata = cur.fetchall()
    for d in displaydata:
        if naam.get() == d[0] and password.get() == d[1]:
            windet = Tk()
            windet.title('details of player')
            windet.geometry('400x200')
            detcanva = Canvas(windet,width=400,height=200,background='#e9c296')
            detcanva.pack()
            headlbl = Label(detcanva,text=f"Details of {naam.get()}",font=('ariel',30,'bold'),background="#e9c296")
            headlbl.place(anchor='center',relx=0.5,rely=0.2)

            lscrlbl = Label(detcanva,text=f"Latest Score was {d[2]}",background="#e9c296",font=('ariel,20,bold'))
            lscrlbl.place(anchor='center',relx=0.5,rely=0.5)
            
            maxcrlbl = Label(detcanva,text=f"highest Score was {d[3]}",background="#e9c296",font=('ariel,20,bold'))
            maxcrlbl.place(anchor='center',relx=0.5,rely=0.7)
            
            mincrlbl = Label(detcanva,text=f"lowest Score was {d[4]}",background="#e9c296",font=('ariel,20,bold'))
            mincrlbl.place(anchor='center',relx=0.5,rely=0.9)
            break
    else:
        entrdet = Label(nmcanva,text='No details about this name and password check it again',background='#e9c296',foreground='red',height=1)
        entrdet.place(anchor='center',relx=0.48,rely=0.45)

win = Tk()# this is the window where we are playing game
win.title('fire game')
win.geometry('600x400')

nmcanva = Canvas(win,width=600,height=400,background="#e9c296")#window which ask user name and password
nmcanva.pack() 
lbl = Label(nmcanva,text='Welcome to py game',width=None,height=None,font=('ariel 40 bold'),
            background='#e9c296').place(anchor='center',relx=0.5,rely=0.2)

nmlbl = Label(nmcanva,text='⊛ Enter your name',font=('ariel 13 bold'),
              background='#e9c296').place( anchor='center',relx=0.26,rely=0.35)
paswdlbl = Label(nmcanva,text='⊛ Password',font=('ariel 13 bold'),
              background='#e9c296').place( anchor='center',relx=0.215,rely=0.41)

naam = StringVar()
nm = Entry(nmcanva,width=20,background='#fcf0e2',textvariable=naam).place(anchor='center',relx=0.55,rely=0.35)
password = StringVar()
nm = Entry(nmcanva,width=20,background='#fcf0e2',textvariable=password).place(anchor='center',relx=0.55,rely=0.41)


rulelabel = Label(nmcanva,background='#e9c296',text='⊛ RULES',font=('ariel 10 bold')).place(relx=0.1335,rely=0.5)
rule1lbl = Label(nmcanva,background='#e9c296',text="<1>Fire obstacles and gain score +1",font=('ariel 10 bold')).place(relx=0.15,rely=0.55)
rule2lbl = Label(nmcanva,background='#e9c296',text="<2>Don't leave any obstacle otherwise lose 1 score",font=('ariel 10 bold')).place(relx=0.15,rely=0.6)
rule3lbl = Label(nmcanva,background='#e9c296',text="<3>Enjoy!",font=('ariel 10 bold')).place(relx=0.15,rely=0.65)

playbtn = Button(nmcanva,text='Play game',font=('ariel',15,'bold'),
                 background='pink',width=15,height=1,command=play1).place(anchor='center',relx=0.8,rely=0.9)
detailsbtn = Button(nmcanva,text='Show previous details',font=('ariel',15,'bold'),
                 background='pink',width=20,height=1,command=showdetails).place(anchor='center',relx=0.3,rely=0.9)
win.mainloop()

cur.execute("create database if not exists pythongame")
cur.execute('use pythongame')
cur.execute("create table if not exists pygame(playername varchar(20) not null,ppassword varchar(10) not null,lscore int,maxscore int,minscore int);")
cur.execute("select * from pygame")
data = cur.fetchall()

if data != []:
    for tup in data:
        if tup[0] == pname and tup[1] == ppaswd:
            lowest = tup[4]
            highest = tup[3]
            if lscore > highest:
                highest = lscore
            elif lscore < lowest:
                lowest = lscore
            cur.execute(f"update pygame set lscore ={lscore},maxscore = {highest},minscore = {lowest} where playername = '{naam.get()}' and ppassword = '{password.get()}'")
            break
        else:
            cur.execute(f"insert into pygame values('{naam.get()}','{password.get()}',{lscore},{lscore},{lscore});")
else:
    cur.execute(f"insert into pygame values('{naam.get()}','{password.get()}',{lscore},{lscore},{lscore});")

con.commit()
cur.close()
con.close()
#END
