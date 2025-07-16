# 🖐️ Virtual Hand-Tracking Piano 🎹

A fun and interactive Python project that lets you **play piano notes with your fingers in the air**, using your **webcam** and **MediaPipe's hand tracking**!

---

## ✨ Features

- Detects real-time hand landmarks using your webcam
- Plays musical notes when your fingers touch virtual piano keys
- Supports multi-finger interaction (multiple notes at once)
- Uses `.wav` sound files for realistic key sounds
- Pygame handles audio output
- OpenCV draws a virtual piano on the screen

---

## 🛠 Tech Stack

- Python 3.x
- OpenCV
- MediaPipe
- Pygame

---

## 🎯 How It Works

- The app uses `MediaPipe` to detect hands and finger tips in real time.
- A piano layout is drawn on the screen using `OpenCV`.
- If your finger tip crosses into a piano key area, a corresponding `.wav` file is played using `pygame`.

---

## 🚀 Getting Started

### 1. Install Dependencies
Make sure Python is installed. Then run:

```bash
pip install pygame opencv-python mediapipe
