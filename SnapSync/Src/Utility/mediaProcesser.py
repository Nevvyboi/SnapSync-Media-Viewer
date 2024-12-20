from PIL import Image, ImageDraw
import cv2
import os
from Src.Utility.database import MediaDatabase
import hashlib
import customtkinter as ctk

def generateFileHashCode(filePath: str) -> str:
    try:
        hashCode = hashlib.sha256()
        with open(filePath, "rb") as f:
            while chunk := f.read(8192):
                hashCode.update(chunk)
        return hashCode.hexdigest()
    except Exception as e:
        print(e)

def processImage(database : MediaDatabase, filePath : str) -> None:
    try:
        with Image.open(filePath) as img:
            size = os.path.getsize(filePath)
            resolution = f"{img.width}x{img.height}"
            name = os.path.basename(filePath)
            fileHash = generateFileHashCode(filePath)
            database.insertMediaIntoDatabase(name, "image", filePath, size, resolution, None, fileHash)
    except Exception as e:
        print(f"Error processing image {filePath}: {e}")
        return None

def processVideo(database : MediaDatabase, filePath : str) -> None:
    try:
        cap = cv2.VideoCapture(filePath)
        if not cap.isOpened():
            raise Exception("Cannot open video")
        size = os.path.getsize(filePath)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = f"{width}x{height}"
        duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        name = os.path.basename(filePath)
        fileHash = generateFileHashCode(filePath)
        cap.release()
        database.insertMediaIntoDatabase(name, "video", filePath, size, resolution, duration, fileHash)
    except Exception as e:
        print(f"Error processing video {filePath}: {e}")
        return None

def findImagesAndVideos(files : list[str]) -> tuple[list[str], list[str]]:
    try:
        imageFiles = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        videoFiles = [f for f in files if f.lower().endswith((".mp4", ".avi", ".mkv"))]
        print(f"Found {len(imageFiles)} images and {len(videoFiles)} videos!")
        print(imageFiles)
        return imageFiles, videoFiles
    except Exception as e:
        print(e)

def storeIntoDatabase(images : list[str], videos : list[str]) -> None:
    try:
        print("Storing images and videos in database...")
        database = MediaDatabase()
        for image in images:
            processImage(database, image)
        for video in videos:
            processVideo(database, video)
    except Exception as e:
        print(e)

def getThumbNail(pathOfMedia: str, mediaType: str, sizeOfMedia: tuple[int, int]) -> ctk.CTkImage:
    try:
        if mediaType == "image":
            image = Image.open(pathOfMedia)
            image.thumbnail(sizeOfMedia, Image.Resampling.LANCZOS)
            return ctk.CTkImage(image, size = sizeOfMedia)

        elif mediaType == "video":
            thumbnail = extractVideoFrame(pathOfMedia, sizeOfMedia)
            return ctk.CTkImage(thumbnail, size = sizeOfMedia)

    except Exception as e:
        return ctk.CTkImage(Image.new("RGB", sizeOfMedia, color = "black"), size = sizeOfMedia)


def createVideoPlaceholderWithIcon(size: tuple[int, int]) -> Image:
    placeholder = Image.new("RGB", size, color = "gray")
    draw = ImageDraw.Draw(placeholder)

    buttonSize = min(size) // 3
    centreX, centreY = size[0] // 2, size[1] // 2
    triangle = [
        (centreX - buttonSize // 2, centreY - buttonSize // 2),
        (centreX - buttonSize // 2, centreY + buttonSize // 2),
        (centreX + buttonSize // 2, centreY),
    ]
    draw.polygon(triangle, fill = "white")
    return placeholder

def extractVideoFrame(path: str, size: tuple[int, int]) -> Image:
    try:
        cap = cv2.VideoCapture(path)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image.thumbnail(size, Image.Resampling.LANCZOS)
            return image
        else:
            print(f"Failed to extract frame from video: {path}")
    except Exception as e:
        print(f"Error extracting frame from video: {e}")
    return createVideoPlaceholderWithIcon(size)

