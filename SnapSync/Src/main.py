import os
import subprocess
import tkinter as tk
import customtkinter as ctk
from Src.Utility.iconLoader import Icons
from CTkToolTip import *
from tkinter import filedialog
from Src.Utility.mediaProcesser import findImagesAndVideos, storeIntoDatabase, getThumbNail
from Src.Utility.mediaViewer import MediaViewer
import sqlite3

class HomePage(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Database path
        self.dbPath = r"C:\Users\User\Coding\SnapSync\Src\Database\media.db"
        #Disabling the default window; to enable app customization
        self.overrideredirect(True)
        self.openWindowCentreOfScreen(850, 600)
        self.xOffSet = None
        self.yOffSet = None

        #Setting a variable to track light/dark mode
        self.mode = "dark"
        ctk.set_appearance_mode(self.mode)

        #Setting a variable to track what page we on
        self.currentPage = "home"
        #Displaying images.videos from the database
        #self.displayMedia()

        self.backgroundImageLabel = ctk.CTkLabel(self, text = "", fg_color = ("#FAF9FE", "#12141B"))

        self.frameNames = ["home", "folder", "favourite", "settings"]
        self.frames = {}
        self.currentFrame = None
        for frame in self.frameNames:
            self.frames[frame] = self.createFrame(frame)

        #Loading up the widgets for the main window
        self.setupMainWindow()

        #icons/labels in left navigation bar
        self.leftNavBarIcons = {
            "home" : [self.leftNavBarHomePageIcon, Icons().homePage, Icons().homeLightHoverPage, Icons().homeDarkHoverPage],
            "folder" : [self.leftNavBarFolderPageIcon, Icons().folderPage, Icons().folderLightHoverPage, Icons().folderDarkHoverPage],
            "favourite" : [self.leftNavBarFavouritePageIcon, Icons().favouritePage, Icons().favouriteLightHoverPage, Icons().favouriteDarkHoverPage],
            "settings" : [self.leftNavBarSettingsPageIcon, Icons().settingsPage, Icons().settingsLightHoverPage, Icons().settingsDarkHoverPage],
        }

        self.bindEventsWithFrame("home", {
            "<Button-1>" : self.startMovingWindow,
            "<B1-Motion>" : self.dragWindow
        })
        self.bindEventsWithFrame("folder", {
            "<Button-1>": self.startMovingWindow,
            "<B1-Motion>": self.dragWindow
        })
        self.bindEventsWithFrame("favourite", {
            "<Button-1>": self.startMovingWindow,
            "<B1-Motion>": self.dragWindow
        })
        self.bindEventsWithFrame("settings", {
            "<Button-1>": self.startMovingWindow,
            "<B1-Motion>": self.dragWindow
        })
        self.showFrame("home")
        self.homeFrameMedia = []
        self.displayMediaOnHomePage()

    def setupMainWindow(self) -> None:
        #Setting the label which will act as the background image
        self.backgroundImageLabel.pack(fill = "both", expand = True)
        self.backgroundImageLabel.bind("<Button-1>", self.startMovingWindow)
        self.backgroundImageLabel.bind("<B1-Motion>", self.dragWindow)

        #Setting up the top navigation bar
        self.topNavBar = ctk.CTkFrame(self.backgroundImageLabel, width = 791, height = 61, fg_color = ("#FFFFFF", "#1C1C24"), border_color = ("#E2E2EA", "#292A32"), corner_radius = 0)
        self.topNavBar.place(x = 60, y = 0)
        self.topNavBar.bind("<Button-1>", self.startMovingWindow)
        self.topNavBar.bind("<B1-Motion>", self.dragWindow)

        #Menu to minimize/close
        self.closeWindow = ctk.CTkLabel(self.topNavBar, width = 30, height = 30, image = Icons().close, fg_color = ("#FFFFFF", "#1C1C24"), text = "")
        self.closeWindow.place(x = 746, y = 15)
        closeWindowToolTip = CTkToolTip(self.closeWindow, message = "Close Window")
        self.closeWindow.bind("<Button-1>", lambda event, typeOfIcon = "close" : self.iconPressed(event, typeOfIcon))
        self.closeWindow.bind("<Enter>", lambda event, typeOfIcon = "close" : self.iconHoverEnter(event, typeOfIcon))
        self.closeWindow.bind("<Leave>", lambda event, typeOfIcon = "close" : self.iconHoverExit(event, typeOfIcon))

        #Setting up the left navigation bar
        leftNavBar = ctk.CTkFrame(self.backgroundImageLabel, width = 61, height = 600, fg_color = ("#FFFFFF", "#1C1C24"), border_color = ("#E2E2EA", "#292A32"))
        leftNavBar.place(x = 0, y = 0)
        leftNavBar.bind("<Button-1>", self.startMovingWindow)
        leftNavBar.bind("<B1-Motion>", self.dragWindow)
        #SnapSync Logo
        leftNavBarSnapSyncIcon = ctk.CTkLabel(leftNavBar, width = 60, height = 60, fg_color = ("#FFFFFF", "#1C1C24"), text = "", image = Icons().snapSync)
        leftNavBarSnapSyncIcon.place(x = 0, y = 0)
        leftNavBarSnapSyncIconToolTip = CTkToolTip(leftNavBarSnapSyncIcon, message = "Snap Sync")

        self.leftNavBarHomePageIcon = ctk.CTkLabel(leftNavBar, width = 60, height = 60, text = "", image = Icons().homeLightHoverPage if self.mode == "light" else Icons().homeDarkHoverPage)
        self.leftNavBarHomePageIcon.place(x = 0, y = 60)
        leftNavBarHomePageIconToolTip = CTkToolTip(self.leftNavBarHomePageIcon, message = "Home Page")
        self.leftNavBarHomePageIcon.bind("<Button-1>", lambda event, typeOfIcon = "home" : self.iconPressed(event, typeOfIcon))
        self.leftNavBarHomePageIcon.bind("<Enter>", lambda event, typeOfIcon = "home" : self.iconHoverEnter(event, typeOfIcon))
        self.leftNavBarHomePageIcon.bind("<Leave>", lambda event, typeOfIcon = "home" : self.iconHoverExit(event, typeOfIcon))

        self.leftNavBarFolderPageIcon = ctk.CTkLabel(leftNavBar, width = 60, height = 60, text = "", image = Icons().folderPage)
        self.leftNavBarFolderPageIcon.place(x = 0, y = 120)
        leftNavBarFolderPageIconToolTip = CTkToolTip(self.leftNavBarFolderPageIcon, message = "Folder Page")
        self.leftNavBarFolderPageIcon.bind("<Button-1>", lambda event, typeOfIcon = "folder" : self.iconPressed(event, typeOfIcon))
        self.leftNavBarFolderPageIcon.bind("<Enter>", lambda event, typeOfIcon = "folder" : self.iconHoverEnter(event, typeOfIcon))
        self.leftNavBarFolderPageIcon.bind("<Leave>", lambda event, typeOfIcon = "folder" : self.iconHoverExit(event, typeOfIcon))

        self.leftNavBarFavouritePageIcon = ctk.CTkLabel(leftNavBar, width = 60, height = 60, text = "", image = Icons().favouritePage)
        self.leftNavBarFavouritePageIcon.place(x = 0, y = 180)
        leftNavBarFavouritePageIconToolTip = CTkToolTip(self.leftNavBarFavouritePageIcon, message="Favourites Page")
        self.leftNavBarFavouritePageIcon.bind("<Button-1>", lambda event, typeOfIcon = "favourite" : self.iconPressed(event, typeOfIcon))
        self.leftNavBarFavouritePageIcon.bind("<Enter>", lambda event, typeOfIcon = "favourite" : self.iconHoverEnter(event, typeOfIcon))
        self.leftNavBarFavouritePageIcon.bind("<Leave>", lambda event, typeOfIcon = "favourite" : self.iconHoverExit(event, typeOfIcon))

        self.leftNavBarSettingsPageIcon = ctk.CTkLabel(leftNavBar, width = 60, height = 60, text = "", image = Icons().settingsPage)
        self.leftNavBarSettingsPageIcon.place(x = 0, y = 240)
        leftNavBarSettingsPageIconToolTip = CTkToolTip(self.leftNavBarSettingsPageIcon, message="Settings Page")
        self.leftNavBarSettingsPageIcon.bind("<Button-1>", lambda event, typeOfIcon = "settings" : self.iconPressed(event, typeOfIcon))
        self.leftNavBarSettingsPageIcon.bind("<Enter>", lambda event, typeOfIcon = "settings" : self.iconHoverEnter(event, typeOfIcon))
        self.leftNavBarSettingsPageIcon.bind("<Leave>", lambda event, typeOfIcon = "settings" : self.iconHoverExit(event, typeOfIcon))

        self.leftNavBarLightDarkMode = ctk.CTkLabel(leftNavBar, width = 60, height = 60, text = "", image = Icons().darkMode if self.mode == "light" else Icons().lightMode)
        self.leftNavBarLightDarkMode.place(x = 0, y = 540)
        self.leftNavBarLightDarkMode.bind("<Button-1>", lambda event, typeOfIcon = "modeIcon" : self.iconPressed(event, typeOfIcon))
        self.leftNavBarLightDarkMode.bind("<Enter>", lambda event, typeOfIcon = "modeIcon" : self.iconHoverEnter(event, typeOfIcon))
        self.leftNavBarLightDarkMode.bind("<Leave>", lambda event, typeOfIcon = "modeIcon" : self.iconHoverExit(event, typeOfIcon))

        self.addIcon = ctk.CTkLabel(self.topNavBar, width = 30, height = 30, text = "", image = Icons().add)
        self.addIcon.place(x = 655, y = 15)
        addIconToolTip = CTkToolTip(self.addIcon, message = "Add Image/Video files")
        self.addIcon.bind("<Button-1>", lambda event, typeOfIcon = "add" : self.iconPressed(event, typeOfIcon))
        self.addIcon.bind("<Enter>", lambda event, typeOfIcon = "add" : self.iconHoverEnter(event, typeOfIcon))
        self.addIcon.bind("<Leave>", lambda event, typeOfIcon = "add" : self.iconHoverExit(event, typeOfIcon))

        self.refreshIcon = ctk.CTkLabel(self.topNavBar, width = 25, height = 25, text = "", image = Icons().refresh)
        self.refreshIcon.place(x = 703, y = 18)
        refreshIconToolTip = CTkToolTip(self.refreshIcon, message = "Refresh Media")
        self.refreshIcon.bind("<Button-1>", lambda event, typeOfIcon = "refresh" : self.iconPressed(event, typeOfIcon))
        self.refreshIcon.bind("<Enter>", lambda event, typeOfIcon = "refresh" : self.iconHoverEnter(event, typeOfIcon))
        self.refreshIcon.bind("<Leave>", lambda event, typeOfIcon = "refresh" : self.iconHoverExit(event, typeOfIcon))

    def displayMediaOnHomePage(self) -> None:
        try:
            with sqlite3.connect(self.dbPath) as db:
                cursor = db.cursor()
                query = "SELECT id, type, path FROM media ORDER BY RANDOM() LIMIT 6;"
                data = cursor.execute(query).fetchall()

            for widget in self.frames["home"].grid_slaves():
                widget.destroy()

            frameWidth, frameHeight = 774, 540
            itemSize = 250
            cols = 3
            rows = 2

            horizontalGap = (frameWidth - (cols * itemSize)) // (cols + 1)
            verticalGap = (frameHeight - (rows * itemSize)) // (rows + 1)

            for index, (id, type, path) in enumerate(data):
                col = index % cols
                row = index // cols
                x = horizontalGap + col * (itemSize + horizontalGap)
                y = verticalGap + row * (itemSize + verticalGap)
                self.frames["home"].propagate(False)
                #Checking to see the image path stored exists
                if os.path.exists(path):
                    if type == "image": thumbnail = getThumbNail(path, type, (itemSize, itemSize))
                    elif type == "video": thumbnail = getThumbNail(path, type, (itemSize, itemSize))
                    else: thumbnail = None
                #Placing the image onto the frame
                if thumbnail:
                    image = ctk.CTkLabel(self.frames["home"], image = thumbnail, bg_color = ("#FAF9FE", "#12141B"), width = itemSize, height = itemSize)
                    image.image = thumbnail
                    image.place(x = x, y = y)
                    if type == "image": imageLabelIconToolTip = CTkToolTip(image, message = "Open Image")
                    elif type == "video": imageLabelIconToolTip = CTkToolTip(image, message = "Open Video")
                    image.bind("<Button-1>", lambda event, pathMedia = path, typeMedia = type, idNo = id, home = "home": self.viewMedia(event, pathMedia, typeMedia, idNo, home))
        except Exception as e:
            print(e)

    def displayMediaOnFavouritePage(self) -> None:
        try:
            with sqlite3.connect(self.dbPath) as db:
                data = db.execute("SELECT mediaID, mediaType, filePath FROM likedMedia ORDER BY RANDOM() LIMIT 6;").fetchall()

            for widget in self.frames["favourite"].grid_slaves():
                widget.destroy()

            frameWidth, frameHeight = 774, 540
            itemSize = 250
            cols = 3
            rows = 2
            horizontalGap = (frameWidth - (cols * itemSize)) // (cols + 1)
            verticalGap = (frameHeight - (rows * itemSize)) // (rows + 1)

            for index, (id, type, path) in enumerate(data):
                col = index % cols
                row = index // cols
                x = horizontalGap + col * (itemSize + horizontalGap)
                y = verticalGap + row * (itemSize + verticalGap)
                self.frames["favourite"].propagate(False)
                #Checking to see the image path stored exists
                if os.path.exists(path):
                    if type == "image": thumbnail = getThumbNail(path, type, (itemSize, itemSize))
                    elif type == "video": thumbnail = getThumbNail(path, type, (itemSize, itemSize))
                    else: thumbnail = None
                #Placing the image onto the frame
                if thumbnail:
                    image = ctk.CTkLabel(self.frames["favourite"], image = thumbnail, bg_color = ("#FAF9FE", "#12141B"), width = itemSize, height = itemSize)
                    image.image = thumbnail
                    image.place(x = x, y = y)
                    if type == "image": imageLabelIconToolTip = CTkToolTip(image, message = "Open Image")
                    elif type == "video": imageLabelIconToolTip = CTkToolTip(image, message = "Open Video")
                    image.bind("<Button-1>", lambda event, pathMedia = path, typeMedia = type, idNo = id, fav = "favourite": self.viewMedia(event, pathMedia, typeMedia, idNo, fav))
        except Exception as e:
            print(e)

    def viewMedia(self, event, pathOfMediaFile : str, mediaType : str, id : int, frameName : str) -> None:
        self.withdraw()
        MediaViewer(self, pathOfMediaFile, mediaType, id, frameName)

    def createFrame(self, nameOfFrame : str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.backgroundImageLabel, width = 774, height = 540, corner_radius = 0, fg_color = ("#FAF9FE", "#12141B"))
        frame.place(x = 60, y = 60)
        frame.place_forget()
        return frame

    def bindEventsWithFrame(self, nameOfFrame : str, bindings : dict) -> None:
        frame = self.frames.get(nameOfFrame)
        if frame:
            for event, handler in bindings.items():
                frame.bind(event, handler)

    def showFrame(self, nameOfFrame : str) -> None:
        if self.currentFrame:
            self.frames[self.currentFrame].place_forget()
        frame = self.frames.get(nameOfFrame)
        if frame:
            frame.place(x = 60, y = 60)
            self.currentFrame = nameOfFrame

    def iconPressed(self, event, typeOfIcon : str) -> None:
        if typeOfIcon == "modeIcon":
            if self.mode == "dark":
                self.leftNavBarLightDarkMode.configure(image=Icons().lightMode)
                self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][2])
                ctk.set_appearance_mode("light")
                self.mode = "light"
            elif self.mode == "light":
                self.leftNavBarLightDarkMode.configure(image = Icons().darkMode)
                self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][3])
                ctk.set_appearance_mode("dark")
                self.mode = "dark"
        elif typeOfIcon == "home":
            if self.currentPage == typeOfIcon: return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image = self.leftNavBarIcons[typeOfIcon][2])
                elif self.mode == "dark":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image=self.leftNavBarIcons[typeOfIcon][3])
                if self.currentPage == "folder": self.addIcon.place(x = 655, y = 15)
                self.displayMediaOnHomePage()
                self.currentPage = "home"
                self.showFrame("home")
        elif typeOfIcon == "favourite":
            if self.currentPage == typeOfIcon: return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image = self.leftNavBarIcons[typeOfIcon][2])
                elif self.mode == "dark":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image=self.leftNavBarIcons[typeOfIcon][3])
                if self.currentPage == "folder": self.addIcon.place(x = 655, y = 15)
                self.displayMediaOnFavouritePage()
                self.currentPage = "favourite"
                self.showFrame("favourite")
        elif typeOfIcon == "folder":
            if self.currentPage == typeOfIcon: return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image = self.leftNavBarIcons[typeOfIcon][2])
                elif self.mode == "dark":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image=self.leftNavBarIcons[typeOfIcon][3])
                self.displayFolderFrame()
                self.currentPage = "folder"
                self.showFrame("folder")
        elif typeOfIcon == "settings":
            if self.currentPage == typeOfIcon: return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image = self.leftNavBarIcons[typeOfIcon][2])
                elif self.mode == "dark":
                    self.leftNavBarIcons[self.currentPage][0].configure(image = self.leftNavBarIcons[self.currentPage][1])
                    self.leftNavBarIcons[typeOfIcon][0].configure(image=self.leftNavBarIcons[typeOfIcon][3])
                    if self.currentPage == "folder": self.addIcon.place(x = 655, y = 15)
                self.displaySettingsFrame()
                self.currentPage = "settings"
                self.showFrame("settings")
        elif typeOfIcon == "close":
            self.destroy()
        elif typeOfIcon == "add":
            folderPath = filedialog.askdirectory(title = "Select the folder that contains images or videos")
            if folderPath and os.path.isdir(folderPath):
                files = os.listdir(folderPath)
                filesWithPath = []
                for file in files:
                    filePath = os.path.join(folderPath, file)
                    filesWithPath.append(filePath)
                if not filesWithPath:
                    print("Empty File")
                else:
                    processedFiles = findImagesAndVideos(filesWithPath)
                    storeIntoDatabase(processedFiles[0], processedFiles[1])
                    if self.currentPage == "home": self.displayMediaOnHomePage()
            else:
                pass
        elif typeOfIcon == "refresh":
            if self.currentPage == "home":
                self.displayMediaOnHomePage()
            elif self.currentPage == "favourite":
                self.displayMediaOnFavouritePage()

    def iconHoverEnter(self, event, typeOfIcon : str) -> None:
        if typeOfIcon == "modeIcon":
            if self.mode == "light":
                self.leftNavBarLightDarkMode.configure(width = 60, height = 60, image = Icons().darkModeHover)
            elif self.mode == "dark":
                self.leftNavBarLightDarkMode.configure(width = 60, height = 60, image = Icons().lightModeHover)
        elif typeOfIcon == "home":
            if self.currentPage == "home": return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarHomePageIcon.configure(image = Icons().homeLightHoverPage)
                elif self.mode == "dark":
                    self.leftNavBarHomePageIcon.configure(image = Icons().homeDarkHoverPage)
        elif typeOfIcon == "favourite":
            if self.currentPage == "favourite": return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarFavouritePageIcon.configure(image = Icons().favouriteLightHoverPage)
                elif self.mode == "dark":
                    self.leftNavBarFavouritePageIcon.configure(image = Icons().favouriteDarkHoverPage)
        elif typeOfIcon == "folder":
            if self.currentPage == "folder": return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarFolderPageIcon.configure(image = Icons().folderLightHoverPage)
                elif self.mode == "dark":
                    self.leftNavBarFolderPageIcon.configure(image = Icons().folderDarkHoverPage)
        elif typeOfIcon == "settings":
            if self.currentPage == "settings": return
            elif self.currentPage != typeOfIcon:
                if self.mode == "light":
                    self.leftNavBarSettingsPageIcon.configure(image = Icons().settingsLightHoverPage)
                elif self.mode == "dark":
                    self.leftNavBarSettingsPageIcon.configure(image = Icons().settingsDarkHoverPage)
        elif typeOfIcon == "close":
            self.closeWindow.configure(image = Icons().closeHover)
        elif typeOfIcon == "refresh":
            self.refreshIcon.configure(image = Icons().refreshHover)
        elif typeOfIcon == "add":
            self.addIcon.configure(image = Icons().addHover)

    def iconHoverExit(self, event, typeOfIcon : str) -> None:
        if typeOfIcon == "modeIcon":
            if self.mode == "light":
                self.leftNavBarLightDarkMode.configure(width = 60, height = 60, image = Icons().darkMode)
            elif self.mode == "dark":
                self.leftNavBarLightDarkMode.configure(width = 60, height = 60, image = Icons().lightMode)
        elif typeOfIcon == "home":
            if self.currentPage == typeOfIcon: return
            else: self.leftNavBarHomePageIcon.configure(image = Icons().homePage)
        elif typeOfIcon == "favourite":
            if self.currentPage == typeOfIcon: return
            else: self.leftNavBarFavouritePageIcon.configure(image = Icons().favouritePage)
        elif typeOfIcon == "folder":
            if self.currentPage == typeOfIcon: return
            else: self.leftNavBarFolderPageIcon.configure(image = Icons().folderPage)
        elif typeOfIcon == "settings":
            if self.currentPage == typeOfIcon: return
            else: self.leftNavBarSettingsPageIcon.configure(image = Icons().settingsPage)
        elif typeOfIcon == "close":
            self.closeWindow.configure(image = Icons().close)
        elif typeOfIcon == "refresh":
            self.refreshIcon.configure(image = Icons().refresh)
        elif typeOfIcon == "add":
            self.addIcon.configure(image = Icons().add)

    def displaySettingsFrame(self) -> None:
        try:
            def resetDatabaseButtonExit() -> None:
                try:
                    with sqlite3.connect(self.dbPath) as db:
                        db.execute("DELETE FROM media")
                        db.execute("DELETE FROM likedMedia")
                        db.commit()
                        self.displayMediaOnHomePage()
                except Exception as e:
                    print(e)
            resetDatabaseButton = ctk.CTkButton(self.frames["settings"], command = resetDatabaseButtonExit(), width = 218, height = 45, text = "Reset Database", font = ("Inter", 20), corner_radius = 10, bg_color = ("#FAF9FE", "#12141B"), fg_color = "#FF0000", hover_color = "#FF3636")
            resetDatabaseButton.place(x = 25, y = 25)
            resetDatabaseToolTip = CTkToolTip(resetDatabaseButton, message = "Reset Database")
        except Exception as e:
            print(e)


    def displayFolderFrame(self) -> None:
        try:
            self.addIcon.place_forget()
            imagesLabel = ctk.CTkLabel(self.frames["folder"], font = ("Inter", 20), width = 135, height = 20, text = "Images/Videos", text_color = "#007AFF", anchor = "w")
            imagesLabel.place(x = 24, y = 15)
            mediaScrollableFrame = ctk.CTkScrollableFrame(self.frames["folder"], width = 720, height = 460, corner_radius = 10, fg_color = ("#92929C", "#41414D"), bg_color = ("#FAF9FE", "#12141B"))
            mediaScrollableFrame.place(x = 24, y = 55)

            with sqlite3.connect(self.dbPath) as db:
                 media = db.execute("SELECT * FROM media").fetchall()
            for data in media:
                infoLabel = ctk.CTkLabel(mediaScrollableFrame, width = 710, height = 45, corner_radius = 10, bg_color = ("#92929C", "#41414D"), fg_color = ("#FAF9FE", "#12141B"))
                infoLabel.pack(pady = 5)

                if data[2] == "image":
                    type = ctk.CTkLabel(infoLabel, width = 77, height = 30, text = "Image", anchor = "center", font = ("Inter", 20, "bold"), text_color = "#007AFF", bg_color = ("#FAF9FE", "#12141B"), fg_color = "#FF8A1D", corner_radius= 10)
                elif data[2] == "video":
                    type = ctk.CTkLabel(infoLabel, width = 77, height = 30, text = "Video", anchor = "center", font = ("Inter", 20, "bold"), text_color = "#007AFF", bg_color = ("#FAF9FE", "#12141B"), fg_color = "#0BDE40", corner_radius = 10)
                type.place(x = 10, y = 7)

                mediaNameLabel = ctk.CTkLabel(infoLabel, text = self.getMediaNameFromPath(data[3]), font = ("Inter", 20), width = 492, height = 30, anchor = "w")
                mediaNameLabel.place(x = 104, y = 7)

                openInFileExplorerIcon = ctk.CTkLabel(infoLabel, width = 24, height = 24, image = Icons().openInFileIcon, fg_color = ("#FAF9FE", "#12141B"), bg_color = ("#FAF9FE", "#12141B"))
                openInFileExplorerIconToolTip = CTkToolTip(openInFileExplorerIcon, message = "Open In File Explorer")
                openInFileExplorerIcon.place(x = 613, y = 10)
                openInFileExplorerIcon.bind("<Button-1>", lambda event, file = data[3] : self.openInFileExplorer(event, file))

                removeLabel = ctk.CTkLabel(infoLabel, width = 45, height = 30, bg_color = ("#FAF9FE", "#12141B"), fg_color = "#FF0000", corner_radius = 10)
                removeDBIcon = ctk.CTkLabel(removeLabel, width = 24, height = 24, image = Icons().deleteFromDatabase, bg_color = "#FF0000")
                removeDBIcon.place(x = 11, y = 3)
                removeDBIcon.bind("<Button-1>", lambda event, file = data[3] : self.removeFileFromDB(event, file))
                removeLabel.place(x = 650, y = 7)
                removeDBToolTip = CTkToolTip(removeDBIcon, message = "Remove Image/Video from Database")
        except Exception as e:
            print(e)

    def removeFileFromDB(self, event, name : str) -> None:
        try:
            with sqlite3.connect(self.dbPath) as db:
                db.execute("DELETE FROM media WHERE path = ?", (name,))
                db.execute("DELETE FROM likedMedia WHERE filePath = ?", (name,))
                db.commit()
                self.displayFolderFrame()
        except Exception as e:
            print(e)

    def getMediaNameFromPath(self, path: str) -> str:
        return os.path.basename(path)

    def openInFileExplorer(self, event, filePath: str):
        if os.path.exists(filePath):
            try:
                absolutePath = os.path.abspath(filePath)
                absolutePath = absolutePath.replace("/", "\\")
                subprocess.run(f'explorer /select,"{absolutePath}"', shell = True)
            except Exception as e:
                print(f"Error opening file: {e}")
        else:
            pass

    def startMovingWindow(self, event) -> None:
        self.xOffSet = event.x
        self.yOffSet = event.y

    def dragWindow(self, event) -> None:
        if self.xOffSet is not None and self.yOffSet is not None:
            self.geometry(f'+{event.x_root - self.xOffSet}+{event.y_root - self.yOffSet}')

    def openWindowCentreOfScreen(self, width : int, height : int) -> None:
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        x = (screenWidth - width) // 2
        y = (screenHeight - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()