import cv2
import tkinter as tk
from PIL import Image, ImageTk

face_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

detect_smile = False
detect_face = False

# функция для обновления изображения на экране
def update_image():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    y = 0
    h = 0
    x = 0
    w = 0

    if detect_face:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if detect_smile:
            roi_gray = gray[y:y+h, x:x+w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(frame, (x+sx, y+sy), (x+sx+sw, y+sy+sh), (0, 255, 0), 2)
                cv2.putText(frame, "Smile", (x+sx, y+sy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # преобразование изображения OpenCV в изображение tkinter
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)

    # обновление изображения на экране
    canvas.imgtk = img
    canvas.itemconfig(canvas_image, image=img)

    # повторный вызов функции для обновления изображения на экране
    root.after(1, update_image)

# функция для изменения состояния флага detect_smile
def toggle_detect_smile():
    global detect_smile
    detect_smile = not detect_smile

    if detect_smile:
        button_smile.config(text="Undetect Smile")
    else:
        button_smile.config(text="Detect Smile")

# функция для изменения состояния флага detect_face
def toggle_detect_face():
    global detect_face
    detect_face = not detect_face
    
    if detect_face:
        button_smile.config(state="normal")
        button_face.config(text="Undetect Face")
    else:
        button_smile.config(state="disabled")
        button_face.config(text="Detect Face")


# создание окна и canvas для отображения изображения
root = tk.Tk()
root.title("Facial Recognition")
# root.configure(bg='black')
root.resizable(width=False, height=False)
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()
canvas_image = canvas.create_image(0, 0, anchor=tk.NW)




# создание кнопки для изменения состояния флага detect_smile
button_face = tk.Button(root, text="Detect Face", command=toggle_detect_face)
button_face.pack(side='left')

# создание кнопки для изменения состояния флага detect_smile
button_smile = tk.Button(root, text="Detect Smile", state="disabled", command=toggle_detect_smile)
button_smile.pack(side='right')



# запуск функции для обновления изображения на экране
update_image()

# запуск главного цикла tkinter
root.mainloop()

cap.release()
cv2.destroyAllWindows()
