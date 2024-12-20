import sqlite3
import subprocess
from Src.Utility.iconLoader import Icons
import customtkinter as ctk
from CTkToolTip import CTkToolTip
import cv2
import os
from PIL import Image, ImageTk
import threading
import vlc

class MediaViewer(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, pathToMedia: str, mediaType: str, id: int, frame: str):
        super().__init__(master)
        self.root = master
        self.pathToMedia = pathToMedia
        self.mediaType = mediaType
        self.idNo = id
        self.frameName = frame

        # VLC player for sound
        self.vlc_player = None

        # Disabling the default window; to enable app customization
        self.overrideredirect(True)
        self.openWindowCentreOfScreen(850, 600)
        self.xOffSet = None
        self.yOffSet = None

        self.isMediaLiked = self.checkIfMediaIsLiked(pathToMedia, self.idNo)

        # Loading up the widgets for the main window
        self.setupMainWindow()

    def setupMainWindow(self) -> None:
        # Setting the label which will act as the background image
        self.backgroundImageLabel = ctk.CTkLabel(self, text="", fg_color=("#FAF9FE", "#12141B"))
        self.backgroundImageLabel.pack(fill = "both", expand=True)
        self.backgroundImageLabel.bind("<Button-1>", self.startMovingWindow)
        self.backgroundImageLabel.bind("<B1-Motion>", self.dragWindow)

        # Setting up the top navigation bar
        self.topNavBar = ctk.CTkFrame(self.backgroundImageLabel, width=850, height=60, fg_color=("#FFFFFF", "#1C1C24"), border_color=("#E2E2EA", "#292A32"), corner_radius=0)
        self.topNavBar.place(x = 0, y = 0)
        self.topNavBar.bind("<Button-1>", self.startMovingWindow)
        self.topNavBar.bind("<B1-Motion>", self.dragWindow)

        self.mainFrame = ctk.CTkFrame(self.backgroundImageLabel, width=850, height=540, corner_radius=0, fg_color=("#FFFFFF", "#1C1C24"))
        self.mainFrame.place(x = 0, y = 61)

        self.closeMedia = ctk.CTkLabel(self.topNavBar, width = 108, height = 32, image = Icons().closeMedia)
        self.closeMedia.place(x = 726, y = 14)
        closeMediaToolTip = CTkToolTip(self.closeMedia, message = "Close Media Viewer")
        self.closeMedia.bind("<Button-1>", self.closeMediaViewer)
        self.closeMedia.bind("<Enter>", lambda event, typeOfIcon="closeMedia": self.iconHoverEnter(event, typeOfIcon))
        self.closeMedia.bind("<Leave>", lambda event, typeOfIcon="closeMedia": self.iconHoverExit(event, typeOfIcon))

        if self.mediaType == "image":
            self.displayImage()
        elif self.mediaType == "video":
            self.displayVideo()

        if self.frameName == "home":
            self.setupLikeButton()
        elif self.frameName == "favourite":
            pass

    def displayImage(self):
        fileLocation = ctk.CTkLabel(self.topNavBar, text = self.pathToMedia, fg_color=("#FAF9FE", "#12141B"), font=("Inter", 20), corner_radius=10)
        fileLocation.place(x = 70, y = 14)
        fileLocation.bind("<Button-1>", lambda e: self.openInFileExplorer(self.pathToMedia))

        img = Image.open(self.pathToMedia)
        frameWidth, frameHeight = 850, 540

        if img.size[0] > frameWidth or img.size[1] > frameHeight:
            img.thumbnail((frameWidth, frameHeight), Image.Resampling.LANCZOS)

        updatedWidth, updatedHeight = img.size
        mediaImage = ctk.CTkImage(img, size = (updatedWidth, updatedHeight))

        label = ctk.CTkLabel(self.mainFrame, image = mediaImage, text = "", compound = "center")
        label.place(relx = 0.5, rely = 0.5, anchor = "center")

    def displayVideo(self):
        self.videoLabel = ctk.CTkLabel(self.mainFrame, text = "")
        self.videoLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.cap = cv2.VideoCapture(self.pathToMedia)
        self.playing = True

        self.vlcPlayer = vlc.MediaPlayer(self.pathToMedia)
        self.vlcPlayer.play()

        threading.Thread(target = self.playVideo, daemon = True).start()

    def playVideo(self):
        self.update_idletasks()

        frameWidth = self.mainFrame.winfo_width() or 850
        frameHeight = self.mainFrame.winfo_height() or 540

        while self.cap.isOpened() and self.playing:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            videoWidth, videoHeight = img.size
            scalingFactor = min(frameWidth / videoWidth, frameHeight / videoHeight)
            newWidth = max(1, int(videoWidth * scalingFactor))
            newHeight = max(1, int(videoHeight * scalingFactor))

            resizedImage = img.resize((newWidth, newHeight), Image.Resampling.LANCZOS)
            ctkImage = ctk.CTkImage(resizedImage, size = (newWidth, newHeight))

            self.videoLabel.configure(image = ctkImage)
            self.videoLabel.image = ctkImage
            self.videoLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

            self.videoLabel.update()
            cv2.waitKey(30)

    def closeMediaViewer(self, event) -> None:
        if self.mediaType == "video":
            self.playing = False
            if hasattr(self, "cap") and self.cap:
                self.cap.release()
            if self.vlcPlayer:
                self.vlcPlayer.stop()
        self.destroy()
        self.root.deiconify()

    def setupLikeButton(self):
        icon = Icons().likedUIcon if self.isMediaLiked else Icons().likedIcon
        self.like = ctk.CTkLabel(self.topNavBar, width = 32, height = 32, image = icon)
        self.like.place(x = 17, y = 14)
        self.like.bind("<Button-1>", lambda event, typeOfIcon = "liked": self.iconPressed(event, typeOfIcon))

    def checkIfMediaIsLiked(self, mediaPath: str, idNo: int) -> bool:
        try:
            with sqlite3.connect(self.root.dbPath) as db:
                likedMedia = db.execute("SELECT * FROM likedMedia WHERE filePath = ? and mediaID = ?", (mediaPath, idNo)).fetchone()
                return likedMedia is not None
        except Exception as e:
            print(f"Error checking if media is liked: {e}")
            return False

    def iconPressed(self, event, typeOfIcon: str) -> None:
        if typeOfIcon == "liked":
            try:
                with sqlite3.connect(self.root.dbPath) as db:
                    if self.isMediaLiked is True:
                        db.execute("DELETE FROM likedMedia WHERE filePath = ? AND mediaID = ?", (self.pathToMedia, self.idNo))
                        db.commit()
                        self.isMediaLiked = False
                        self.like.configure(image = Icons().likedIcon)
                    elif self.isMediaLiked is False:
                        db.execute("INSERT INTO likedMedia (mediaID, filePath, mediaType) VALUES (?, ?, ?)", (self.idNo, self.pathToMedia, self.mediaType))
                        self.isMediaLiked = True
                        self.like.configure(image = Icons().likedUIcon)
            except Exception as e:
                print(e)

    def iconHoverEnter(self, event, typeOfIcon: str) -> None:
        if typeOfIcon == "closeMedia":
            self.closeMedia.configure(image = Icons().closeMediaHover)
        elif typeOfIcon == "liked":
            self.like.configure(image = Icons().likedIconHover)

    def iconHoverExit(self, event, typeOfIcon: str) -> None:
        if typeOfIcon == "closeMedia":
            self.closeMedia.configure(image = Icons().closeMedia)
        elif typeOfIcon == "liked":
            if self.isMediaLiked is True:
                self.like.configure(image = Icons().likedUIcon)
            elif self.isMediaLiked is False:
                self.like.configure(image = Icons().likedIcon)

    def openInFileExplorer(self, filePath: str):
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

    def openWindowCentreOfScreen(self, width: int, height: int) -> None:
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        x = (screenWidth - width) // 2
        y = (screenHeight - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
