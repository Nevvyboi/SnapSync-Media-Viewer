import customtkinter as ctk
from PIL import Image
import os, sys

def getBasePath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def getImagePath(fileName) -> str:
    components_folder = os.path.join(getBasePath(), "Icons")
    return os.path.join(components_folder, fileName)

class Icons():
    def __init__(self):
        #Left Navigation Bar Icons
        self.snapSync = ctk.CTkImage(Image.open(getImagePath("snapSync.jpg")), size = (60, 60))

        self.homePage = ctk.CTkImage(Image.open(getImagePath("homeIcon.png")), size = (60, 60))
        self.homeLightHoverPage = ctk.CTkImage(Image.open(getImagePath("homeIconLightHover.png")), size = (60, 60))
        self.homeDarkHoverPage = ctk.CTkImage(Image.open(getImagePath("homeIconDarkHover.png")), size = (60, 60))

        self.favouritePage = ctk.CTkImage(Image.open(getImagePath("favouriteIcon.png")), size = (60, 60))
        self.favouriteLightHoverPage = ctk.CTkImage(Image.open(getImagePath("favouriteIconLightHover.png")), size = (60, 60))
        self.favouriteDarkHoverPage = ctk.CTkImage(Image.open(getImagePath("favouriteIconDarkHover.png")), size = (60, 60))

        self.folderPage = ctk.CTkImage(Image.open(getImagePath("folderIcon.png")), size = (60, 60))
        self.folderLightHoverPage = ctk.CTkImage(Image.open(getImagePath("folderIconLightHover.png")), size = (60, 60))
        self.folderDarkHoverPage = ctk.CTkImage(Image.open(getImagePath("folderIconDarkHover.png")), size = (60, 60))

        self.settingsPage = ctk.CTkImage(Image.open(getImagePath("settingsIcon.png")), size = (60, 60))
        self.settingsLightHoverPage = ctk.CTkImage(Image.open(getImagePath("settingsIconLightHover.png")), size = (60, 60))
        self.settingsDarkHoverPage = ctk.CTkImage(Image.open(getImagePath("settingsIconDarkHover.png")), size = (60, 60))

        self.lightMode = ctk.CTkImage(Image.open(getImagePath("lightMode.png")), size = (60, 60))
        self.lightModeHover = ctk.CTkImage(Image.open(getImagePath("lightModeHover.png")), size = (60, 60))
        self.darkMode = ctk.CTkImage(Image.open(getImagePath("darkMode.png")), size = (60, 60))
        self.darkModeHover = ctk.CTkImage(Image.open(getImagePath("darkModeHover.png")), size = (60, 60))

        self.close = ctk.CTkImage(Image.open(getImagePath("closeIcon.png")), size = (30, 30))
        self.closeHover = ctk.CTkImage(Image.open(getImagePath("closeIconHover.png")), size = (30, 30))

        self.add = ctk.CTkImage(Image.open(getImagePath("addIcon.png")), size = (30, 30))
        self.addHover = ctk.CTkImage(Image.open(getImagePath("addIconHover.png")), size = (30, 30))

        self.refresh = ctk.CTkImage(Image.open(getImagePath("refresh.png")), size = (25, 25))
        self.refreshHover = ctk.CTkImage(Image.open(getImagePath("refreshHover.png")), size = (25, 25))

        self.closeMedia = ctk.CTkImage(Image.open(getImagePath("closeMediaIcon.png")), size = (108, 32))
        self.closeMediaHover = ctk.CTkImage(Image.open(getImagePath("closeMediaIconHover.png")), size = (108, 32))

        self.likedIcon = ctk.CTkImage(Image.open(getImagePath("liked.png")), size = (32, 32))
        self.likedUIcon = ctk.CTkImage(Image.open(getImagePath("likedU.png")), size = (32, 32))
        self.likedIconHover = ctk.CTkImage(Image.open(getImagePath("likedHover.png")), size = (32, 32))

        self.imagesLabel = ctk.CTkImage(Image.open(getImagePath("imagesLabel.png")), size = (23, 135))
        self.videosLabel = ctk.CTkImage(Image.open(getImagePath("videosLabel.png")), size = (23, 135))

        self.deleteFromDatabase = ctk.CTkImage(Image.open(getImagePath("deleteFromDB.png")), size = (24, 24))
        self.openInFileIcon = ctk.CTkImage(Image.open(getImagePath("openInFile.png")), size = (24, 24))

