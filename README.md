# 📸 SnapSync Media Viewer

SnapSync is an elegant and user-friendly application designed to display images and videos in a customizable media viewer. Built with Python and CustomTkinter, this application ensures a seamless experience for managing and viewing your favorite media files.

---

## ✨ Features

- 📂 **Folder Integration**: Select a folder to add all images and videos automatically to the viewer.

- 🎞️ **Video Playback**: Effortlessly play videos with synchronized audio using VLC.
- 🖼️ **Image Display**: Showcase images in a responsive frame with adaptive resizing.
- 💖 **Like Button**: Mark your favorite media with a single click.
- 📂 **File Explorer Integration**: Open files directly in your system's file explorer.
- 🎛️ **Customizable UI**: Enjoy a sleek and modern interface powered by CustomTkinter.

---

## 📂 Folder Structure

```
SnapSync/
├── Src/
│   ├── Utility/
│   │   ├── iconLoader.py   # Icon management
│   │   ├── mediaViewer.py  # Media viewer implementation
│   ├── Database/
│   │   ├── media.db        # SQLite database for liked media
│   ├── main.py             # Entry point
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

---

## 🛠️ Usage

1. Launch the application by running `main.py`.
2. Choose an image or video file to view in the media viewer.
3. Interact with the media viewer:
   - 🖱️ Click on the like button to mark media as favorite.
   - 📂 Use the file explorer integration to locate media on your system.

---

## 📸 Screenshots

### Home Screen:
![{1B4E06E6-3174-48C5-83D4-CB60EF11A613}](https://github.com/user-attachments/assets/fcef9f3b-fe42-4676-b8d8-982f33f6d707)


### Media Viewer:
![{529A4DFF-B386-4170-9B93-35BBAF9639D6}](https://github.com/user-attachments/assets/d47846b9-d400-4029-a2d7-f27d69232df3)



---


## 🐞 Known Issues

- 🔇 No sound on video playback when VLC dependencies are missing.
- 🖼️ Some images may not resize properly for extremely small window sizes.

---

## 🎉 Acknowledgments

Special thanks to the open-source community and the developers of the libraries used in this project:

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Pillow](https://python-pillow.org/)
- [VLC Python Bindings](https://wiki.videolan.org/Python_bindings/)
- [CTkToolTip](https://github.com/TomSchimansky/CTkToolTip)

---




