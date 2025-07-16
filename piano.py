import os
import cv2
import mediapipe as mp
import pygame


# --- Initialize pygame mixer ---
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Pygame mixer initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Pygame mixer: {e}")

# --- Define piano keys ---
KEYS = [
    {"note": "C4", "x1": 0,   "x2": 90,  "color": (255,255,255)},
    {"note": "D4", "x1": 90,  "x2": 180, "color": (255,255,255)},
    {"note": "E4", "x1": 180, "x2": 270, "color": (255,255,255)},
    {"note": "F4", "x1": 270, "x2": 360, "color": (255,255,255)},
    {"note": "G4", "x1": 360, "x2": 450, "color": (255,255,255)},
    {"note": "A4", "x1": 450, "x2": 540, "color": (255,255,255)},
    {"note": "B4", "x1": 540, "x2": 630, "color": (255,255,255)},
]

# --- Load sounds ---
SOUNDS = {}
for key in KEYS:
    path = os.path.join("sounds", key["note"] + ".wav")
    if os.path.isfile(path):
        SOUNDS[key["note"]] = pygame.mixer.Sound(path)

# --- MediaPipe setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# --- Webcam setup ---
cap = cv2.VideoCapture(0)
WIDTH, HEIGHT = 630, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# --- Finger tips landmarks for all five fingers ---
FINGER_TIPS = {
    'thumb': 4,
    'index': 8,
    'middle': 12,
    'ring': 16,
    'pinky': 20
}

# Track active notes
playing_notes = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Draw piano keys
    for key in KEYS:
        cv2.rectangle(frame, (key["x1"], HEIGHT-100), (key["x2"], HEIGHT), key["color"], -1)
        cv2.putText(frame, key["note"], (key["x1"]+15, HEIGHT-40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)

    notes_this_frame = set()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Check all five fingers
            for finger in FINGER_TIPS.values():
                x = int(hand_landmarks.landmark[finger].x * WIDTH)
                y = int(hand_landmarks.landmark[finger].y * HEIGHT)
                
                # Visual feedback for finger positions
                cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)
                
                # Check key activation
                if HEIGHT-100 < y < HEIGHT:
                    for idx, key in enumerate(KEYS):
                        if key["x1"] < x < key["x2"]:
                            notes_this_frame.add(key["note"])
                            if key["note"] not in playing_notes:
                                pygame.mixer.Channel(idx).play(SOUNDS[key["note"]])
                            break

    # Update playing notes
    playing_notes = notes_this_frame.copy()

    cv2.imshow("Multi-Finger Piano", frame)
    if cv2.waitKey(1) == 27:  # Exit on ESC
        break

cap.release()
cv2.destroyAllWindows()


