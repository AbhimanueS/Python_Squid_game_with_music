import cv2
import numpy as np
import time
import threading
import pygame
import random
import winsound

# Initialize pygame mixer
pygame.mixer.init()

# Function to play a random song for random duration less than 20 seconds
def play_music():
    # List of song paths
    songs = [""]  # Add your song paths here

    # Select a random song
    song_path = random.choice(songs)

    # Load the selected song
    pygame.mixer.music.load(song_path)

    # Play the song
    pygame.mixer.music.play()

    # Random duration between 5 and 20 seconds
    duration = random.randint(5, 20)
    time.sleep(duration)

    # Stop the song after the random duration
    pygame.mixer.music.stop()

# Function to play sound when motion is detected
def play_sound():
    frequency = 2500  # Set frequency (2500 Hz)
    duration = 1000  # Set duration (1000 ms = 1 second)
    winsound.Beep(frequency, duration)

# Function to detect motion
def detect_motion():
    global prev_frame

    # Capture video from webcam
    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)  # Change the argument to the appropriate index if you have multiple webcams

    # Initialize variables
    prev_frame = None

    start_time = time.time()
    motion_detected = False
   
    while time.time() - start_time < 5:  # Random duration between 3 and 10 seconds...random.randint(3, 10):
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise and improve motion detection
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Initialize previous frame (first frame)
        if prev_frame is None:
            prev_frame = gray
            continue

        # Compute absolute difference between current frame and previous frame
        frame_delta = cv2.absdiff(prev_frame, gray)

        # Apply thresholding to identify regions with significant changes (motion)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours of motion regions
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Iterate through contours
        for contour in contours:
            # If contour area is smaller than a certain threshold, ignore it (noise)
            if cv2.contourArea(contour) < 1000:
                continue

            # Draw rectangle around the contour (motion region)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Play sound when motion is detected
            play_sound()
            motion_detected = True

        # Show video feed
        cv2.imshow('Motion Detection', frame)

        # Update previous frame
        prev_frame = gray

        # Break the loop if motion is detected
        if motion_detected:
            break

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    cap.release()

# Main function
if __name__ == "__main__":
    # Main loop
    while True:
        # Initialize previous frame
        prev_frame = None

        # Play music for random duration less than 15 seconds
        play_music()

        # Detect motion
        motion_detected = detect_motion()
        
        # Clear the previous frame
        prev_frame = None
        
        # Wait for a key press to start the next iteration
        cv2.waitKey(0)
        
        # Clear the OpenCV window
        cv2.destroyAllWindows()
    
    
    