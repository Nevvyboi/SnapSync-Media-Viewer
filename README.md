# 📸 SnapSync Media Viewer

SnapSync is an elegant and user-friendly application designed to display images and videos in a customizable media viewer. Built with Python and CustomTkinter, this application ensures a seamless experience for managing and viewing your favorite media files.

---

## ✨ Features

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
_Add a screenshot here showing the main interface._

### Media Viewer:
_Add a screenshot here showing image or video playback._

---

## 🐞 Known Issues

- 🖼️ Some images may not resize properly for extremely small window sizes.

---

## 🎉 Acknowledgments

Special thanks to the open-source community and the developers of the libraries used in this project:

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Pillow](https://python-pillow.org/)
- [VLC Python Bindings](https://wiki.videolan.org/Python_bindings/)
- [CTkToolTip](https://github.com/TomSchimansky/CTkToolTip)

---

Enjoy using SnapSync! 🎉

