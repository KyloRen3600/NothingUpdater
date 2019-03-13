import urllib.request, json
import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import zipfile
from shutil import rmtree
from distutils.dir_util import copy_tree


main_color = '#%02x%02x%02x' % (24, 50, 78)  # (69, 66, 73) (18, 38, 59)
changelog_color = '#%02x%02x%02x' % (30, 63, 98)  # (69, 66, 73) (18, 38, 59)

path = format(os.getcwd())
path = path.replace("\\", "/")

launcher_path = path
launcher_path = launcher_path.split("/")
launcher_path[len(launcher_path)-1] = "Launcher/"
launcher_path = "/".join(launcher_path)

nothing_path = path.split("/")
del nothing_path[len(nothing_path)-1]

user = os.getlogin()
folder = "C:\\Users\\{0}\\AppData\\Roaming\\NothingGames".format(user)
try:
	os.makedirs(folder)
except:
	pass


try:
	with urllib.request.urlopen("https://raw.githubusercontent.com/KyloRen3600/NothingInfos/master/Infos.json") as url:
		infos = json.loads(url.read().decode())
		exe = str(infos["Launcher-executable"]).replace("NOTHINGGAMES", "/".join(nothing_path))
		launcher_folder = str(infos["Launcher-folder"]).replace("NOTHINGGAMES", "/".join(nothing_path))
		download_url = infos["Download-url"]
		folder_to_extract = infos["Folder-to-extract"]
except:
	with open("Infos.json", 'r') as f:
		infos = json.load(f)
		exe = str(infos["Launcher-executable"]).replace("NOTHINGGAMES", "/".join(nothing_path))
		launcher_folder = str(infos["Launcher-folder"]).replace("NOTHINGGAMES", "/".join(nothing_path))
		download_url = infos["Download-url"]
		folder_to_extract = infos["Folder-to-extract"]

def update():
	destroy()
	files = os.listdir("./Temp")
	for file in files:
		try:
			os.remove('./Temp/{0}'.format(file))
		except:
			rmtree('./Temp/{0}'.format(file))
	urllib.request.urlretrieve(download_url, "Temp/LauncherUpdate.zip")
	zip_ref = zipfile.ZipFile("Temp/LauncherUpdate.zip", 'r')
	zip_ref.extractall("Temp/LauncherUpdate")
	zip_ref.close()
	dst = "NOTHINGGAMES/Launcher".replace("NOTHINGGAMES", "/".join(nothing_path))
	copy_tree('./Temp/LauncherUpdate/{0}'.format(folder_to_extract), "{0}".format(dst))
	files = os.listdir("./Temp")
	for file in files:
		try:
			os.remove('./Temp/{0}'.format(file))
		except:
			rmtree('./Temp/{0}'.format(file))





class Void(tkinter.Button):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(relief=FLAT, state=DISABLED, bg=main_color)




def destroy():
	update_window.destroy()

def get_changelog():
	if connection == True:
		changelog_url = "https://raw.githubusercontent.com/KyloRen3600/NothingLauncher/master/Changelog.txt"
		with urllib.request.urlopen(changelog_url) as url:
			return url.read().decode()
	else:
		return "Connexion au serveur impossible !\nVeuillez vérifier votre connexion Internet..."

class ChangelogFrame(ScrolledText):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(font=("Courrier"), bg=changelog_color, foreground="white", borderwidth=0)
		self.insert(INSERT, changelog_text)
		self.config(state=DISABLED)


class UpdateFrame(Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config(bg=main_color)
		self.frame_update = Frame(self, bg=main_color)
		self.frame_update.config(bg=main_color)
		Void(self.frame_update).pack()
		if int(local_build) != 0:
			self.label = ttk.Label(self.frame_update, foreground="white", text="Mise à jour disponible !",  font="Helvetica 18 bold", background=main_color).pack()
		else:
			self.label = ttk.Label(self.frame_update, foreground="white", text="Installation:",  font="Helvetica 18 bold", background=main_color).pack()
		Void(self.frame_update).pack()
		self.changelog = ChangelogFrame(self.frame_update, bg=main_color)
		self.changelog.pack()
		self.version = Label(self.frame_update, background=main_color, foreground="white", text="Version actuelle: {0}\nDernière version: {1}".format(local_version, version), font="Courrier").pack()
		Void(self.frame_update).pack()
		self.frame_update.grid(row=2)

		self.frame_buttons = Frame(self, bg=main_color)
		if local_build == 0:
			self.image_install = PhotoImage(file="button_install.png")
			self.button_install = Button(self.frame_buttons, image=self.image_install, activebackground=changelog_color, command=update)
			self.button_install["bg"] = changelog_color
			self.button_install["border"] = "0"
			if connection == False:
				self.button_install.config(state=DISABLED)
			self.button_install.grid(row=1, column=1)


		else:
			self.image_yes = PhotoImage(file="button_yes.png")
			self.button_yes = Button(self.frame_buttons, image=self.image_yes, activebackground=changelog_color, command=update)
			self.button_yes["bg"] = changelog_color
			self.button_yes["border"] = "0"
			self.button_yes.grid(row=1, column=1)


			Void(self.frame_buttons).grid(row=1, column=2)
			Void(self.frame_buttons).grid(row=1, column=3)
			Void(self.frame_buttons).grid(row=1, column=4)
			Void(self.frame_buttons).grid(row=1, column=5)
			self.image_no = PhotoImage(file="button_no.png")
			self.button_no = Button(self.frame_buttons, image=self.image_no, activebackground=changelog_color, command=destroy)
			self.button_no["bg"] = main_color
			self.button_no["border"] = "0"
			self.button_no.grid(row=1, column=6)
		#Void(self).pack(side=TOP)
		self.frame_buttons.grid(row=3)



class MainFrame(Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.frame_update = UpdateFrame(self)
		self.frame_update.grid(row=2)



class MainWindow(Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs),
		if local_build == 0:
			self.title("NothingLauncher Installer")
		else:
			self.title("NothingLauncher Updater")
		path = format(os.getcwd())
		path = path.replace("\\", "/")
		path = path.split("/")
		del path[len(path)-1]
		self.iconbitmap("{0}/NothingGames.ico".format("/".join(path)))
		self.geometry("750x650")
		self.resizable(False, False)
		self.config(background=main_color)
		self.frame = MainFrame(self)
		self.frame.pack()
		windowWidth = self.winfo_reqwidth()
		windowHeight = self.winfo_reqheight()
		positionRight = int(self.winfo_screenwidth() / 3 - windowWidth / 2)
		positionDown = int(self.winfo_screenheight() / 7 - windowHeight / 2)
		self.geometry("+{}+{}".format(positionRight, positionDown))



class DownloadWindow(Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs),
		self.overrideredirect(True)
		if local_build == 0:
			self.title("NothingLauncher Installer")
		else:
			self.title("NothingLauncher Updater")
		self.background = PhotoImage(file="background.png")
		self.canvas = Canvas(self, width=self.background.width(), height=self.background.height())
		self.background_label = Label(self.canvas, image=self.background)
		self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.geometry("{0}x{1}".format(self.background.width(), self.background.height()))
		windowWidth = self.winfo_reqwidth()
		windowHeight = self.winfo_reqheight()
		positionRight = int(self.winfo_screenwidth() / 3 - windowWidth / 2)
		positionDown = int(self.winfo_screenheight() / 3 - windowHeight / 2)
		self.geometry("+{}+{}".format(positionRight, positionDown))
		self.canvas.pack()

local_build = 0
local_version = "Non installé"
connection = True

try:
	with open("{0}/Version.json".format(launcher_path), 'r') as f:
		datastore = json.load(f)
		local_build = int(datastore["Build"])
		local_version = datastore["Version"]
		version = datastore["Version"]
except:
	pass

try:
	with urllib.request.urlopen("https://raw.githubusercontent.com/KyloRen3600/NothingLauncher/master/Version.json") as url:
		data = json.loads(url.read().decode())
		build = data["Build"]
		version = data["Version"]
except urllib.error.URLError:
	connection = False


if float(local_build) != 0:
	try:
		if float(build) > float(local_build):
			changelog_text = get_changelog()

			update_window = MainWindow()
			update_window.mainloop()
	except:
		pass
else:
	changelog_text = get_changelog()
	update_window = MainWindow()
	update_window.mainloop()

try:
	with open("{0}/Version.json".format(launcher_path), 'r') as f:
		datastore = json.load(f)
		local_build = int(datastore["Build"])
		local_version = datastore["Version"]
		version = datastore["Version"]
except:
	pass

if local_build != 0:
	os.chdir(launcher_folder)
	#os.system(r"{0}".format(exe))
	os.system(r"{0}".format("Launcher.py"))
