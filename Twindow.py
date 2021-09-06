import tkinter as tk

class Twindow():
	def __init__(self,root):
		print("init")

		self.root = root

		self.canvasMain = tk.Canvas(root,width=500,height=100)
		self.canvasMain.place(x=0,y=0)
		self.canvasSub = tk.Canvas(root,width=500,height=500)
		self.canvasSub.place(x=0,y=100)

		self.addChkValue = tk.BooleanVar()
		self.rmChkValue = tk.BooleanVar()

		self.leftEntrys = []
		self.rightEntrys = []

		self.leftBtns = []
		self.rightBtns = []

		self.loginIdEntry = None

		self.mode = None

		print("call Wset")
		self.WindowSet()

	def Mode(self):
		return self.mode

	def RmIds(self):
		return self.rmIds

	def Tags(self):
		return self.chkTxts,self.excTxts

	def LoginData(self):
		return self.loginId,self.passwd

	def MylistName(self):
		return self.mylistName

	def Chk(self,flg):
		print(flg)
		if flg == "add" and self.addChkValue.get():
			self.mode = flg
			self.rmChkValue.set(False)
			self.AddMode()
		if flg == "rm" and self.rmChkValue.get():
			self.mode = flg
			self.addChkValue.set(False)
			self.RmMode()
		if not self.rmChkValue.get() and not self.addChkValue.get():
			self.mode = None
			self.Clear()

	def Submit(self):
		print("submit")
		if self.mode == None:
			print("None")
			return
		elif self.mode == "add":
			self.chkTxts = [entry.get().lower() for entry in self.leftEntrys if entry.get()]
			self.excTxts = [entry.get().lower() for entry in self.rightEntrys if entry.get()]
			self.loginId = self.loginIdEntry.get()
			self.passwd = self.loginPassEntry.get()
			self.mylistName = self.mylistNameEntry.get()
			print(self.chkTxts,self.excTxts)
			if not self.loginId:
				print("No mail adress")
				return
			if not self.passwd:
				print("No password")
				return
			if not self.chkTxts:
				print("No check Tag")
				return
			if not self.mylistName:
				print("No mylist name")
				return

		elif self.mode == "rm":
			self.rmIds = [int(entry.get()) for entry in self.leftEntrys if entry.get()]
			print(self.rmIds)
			if not self.rmIds:
				print("No remove id")
				return

		self.root.destroy()

	def WindowSet(self):
		print("Wset")
		self.canvasMain.create_text(160,20,text="自動マイリスト登録システム",font=("",20))
		self.canvasMain.create_text(50,70,text="mode",font=("",20))

		tk.Checkbutton(self.canvasMain,text="Add",font=("",20),variable=self.addChkValue,command=lambda:self.Chk("add")).place(x=130,y=50)
		tk.Checkbutton(self.canvasMain,text="Remove",font=("",20),variable=self.rmChkValue,command=lambda:self.Chk("rm")).place(x=220,y=50)

		tk.Button(text="submit",font=("",20),command=self.Submit).place(x=390,y=540)

		self.root.mainloop()

	def AddMode(self):
		print("addmode")
		self.Clear()

		leftBtnPlace = [self.leftEntryPlace[0]+165,self.leftEntryPlace[1]+15]
		rightBtnPlace = [self.rightEntryPlace[0]+165,self.rightEntryPlace[1]+15]

		self.canvasSub.create_text(80,20,text="check tag",font=("",20))
		self.canvasSub.create_text(350,20,text="exclusion tag",font=("",20))

		leftAddBtn = tk.Button(text="+",command=lambda:self.EntryAdd(self.leftEntryPlace,self.leftEntrys,self.leftBtns,leftBtnPlace))
		leftAddBtn.place(x=leftBtnPlace[0],y=leftBtnPlace[1])
		leftDelBtn = tk.Button(text="-",command=lambda:self.EntryDel(self.leftEntryPlace,self.leftEntrys,self.leftBtns,leftBtnPlace))
		leftDelBtn.place(x=leftBtnPlace[0]-20,y=leftBtnPlace[1])

		rightAddBtn = tk.Button(text="+",command=lambda:self.EntryAdd(self.rightEntryPlace,self.rightEntrys,self.rightBtns,rightBtnPlace))
		rightAddBtn.place(x=rightBtnPlace[0],y=rightBtnPlace[1])
		rightDelBtn = tk.Button(text="-",command=lambda:self.EntryDel(self.rightEntryPlace,self.rightEntrys,self.rightBtns,rightBtnPlace))
		rightDelBtn.place(x=rightBtnPlace[0]-20,y=rightBtnPlace[1])

		leftDelBtn["state"] = "disable"
		rightDelBtn["state"] = "disable"

		self.leftBtns = [leftAddBtn,leftDelBtn]
		self.rightBtns = [rightAddBtn,rightDelBtn]

		self.canvasSub.create_text(70,410,text="mylist name",font=("",15))
		self.canvasSub.create_text(70,440,text="mail adress",font=("",15))
		self.canvasSub.create_text(70,470,text="password",font=("",15))

		self.mylistNameEntry = tk.Entry(width=40)
		self.loginIdEntry = tk.Entry(width=40)
		self.loginPassEntry = tk.Entry(width=20,show="*")
		self.mylistNameEntry.place(x=120,y=500)
		self.loginIdEntry.place(x=120,y=530)
		self.loginPassEntry.place(x=120,y=560)

		self.EntryAdd(self.leftEntryPlace,self.leftEntrys,self.leftBtns,leftBtnPlace)
		self.EntryAdd(self.rightEntryPlace,self.rightEntrys,self.rightBtns,rightBtnPlace)

	def RmMode(self):
		print("rmmode")
		self.Clear()
		self.canvasSub.create_text(100,20,text="movie ID",font=("",20))

		leftBtnPlace = [self.leftEntryPlace[0]+165,self.leftEntryPlace[1]+15]

		leftAddBtn = tk.Button(text="+",command=lambda:self.EntryAdd(self.leftEntryPlace,self.leftEntrys,self.leftBtns,leftBtnPlace))
		leftAddBtn.place(x=leftBtnPlace[0],y=leftBtnPlace[1])
		leftDelBtn = tk.Button(text="-",command=lambda:self.EntryDel(self.leftEntryPlace,self.leftEntrys,self.leftBtns,leftBtnPlace))
		leftDelBtn.place(x=leftBtnPlace[0]-20,y=leftBtnPlace[1])

		self.leftBtns = [leftAddBtn,leftDelBtn]

		self.EntryAdd(self.leftEntryPlace,self.leftEntrys,self.leftBtns,leftBtnPlace)

	def EntryAdd(self,entryPlace,entrys,btns,btnPlace):
		entry = tk.Entry(width=30)
		entry.place(x=entryPlace[0],y=entryPlace[1])

		entrys.append(entry)

		btns[0].place(x=btnPlace[0],y=btnPlace[1])
		btns[1].place(x=btnPlace[0]-20,y=btnPlace[1])

		self.canvasSub.create_text(entryPlace[0]-15,entryPlace[1]-90,text="#%s"%len(entrys),font=("",15),tag="#%s%s"%(len(entrys),entryPlace[0]))

		entryPlace[1] += 20
		btnPlace[1] += 20

		if len(entrys) == 1:
			btns[1]["state"] = "disable"
		elif len(entrys) == 2:
			btns[1]["state"] = "active"
		elif len(entrys) == 11:
			btns[0]["state"] = "disable"

	def EntryDel(self,entryPlace,entrys,btns,btnPlace):
		btnPlace[1] -= 40
		btns[0].place(x=btnPlace[0],y=btnPlace[1])
		btns[1].place(x=btnPlace[0]-20,y=btnPlace[1])

		self.canvasSub.delete("#%s%s"%(len(entrys),entryPlace[0]))

		entry = entrys.pop(-1)

		entry.destroy()

		entryPlace[1] -= 20
		btnPlace[1] += 20

		if len(entrys) == 1:
			btns[1]["state"] = "disable"
		elif len(entrys) == 10:
			btns[0]["state"] = "active"

	def Clear(self):
		print("clear")
		self.canvasSub.delete("all")
		for entry in self.leftEntrys:
			entry.destroy()
		self.leftEntrys = []
		for entry in self.rightEntrys:
			entry.destroy()
		self.rightEntrys = []
		for btn in self.leftBtns:
			btn.destroy()
		self.leftBtns = []
		for btn in self.rightBtns:
			btn.destroy()
		self.rightBtns = []

		self.leftEntryPlace = [35,150]
		self.rightEntryPlace = [280,150]

		if self.loginIdEntry:
			self.loginIdEntry.destroy()
			self.loginPassEntry.destroy()
			self.mylistNameEntry.destroy()
