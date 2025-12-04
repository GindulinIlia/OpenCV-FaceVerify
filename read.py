import cv2 as cv

# Путь к модели для детекции лиц YuNet
model_path = 'face_detection_yunet_2023mar.onnx'

# Создание детекцтора лиц YuNet
detector = cv.FaceDetectorYN.create(
    model_path,
    '',
    (320, 320),
    score_threshold=0.8,
    nms_threshold=0.4,
    top_k=50
)

# Проверка загруженности модели
if detector is None:
    print('Ошибка: не удалось загрузить модель для детекции лиц YuNet!')
    exit()

# Выбор камеры
cap = cv.VideoCapture(0)


# Проверка подключения к камере
if not cap.isOpened():
    print('Ошибка: не удалось подключиться к камере!')
    exit()

# Создание окна
windows_name = 'Camera'
cv.namedWindow(windows_name)

while True:
    ret, frame = cap.read()
    if not ret:
        print('Ошибка: не удалось получить кадр')
        exit()

    # Установка размера входного изображения для детектора
    detector.setInputSize((frame.shape[1], frame.shape[0]))

    # Детекция лиц
    _, faces = detector.detect(frame) # faces содержит [x, y, w, h, conf] для каждого лица
    
    # Создание прямоугольника вокруг лиц
    if faces is not None:
        for face in faces: # faces уже содержит [x, y, w, h, conf] для каждого лица
            x, y, w, h = map(int, face[:4]) # Извлечение координат
            confidence = face[4] # Уверенность детекции

            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, f'Face', (x, y-10),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Создание надписи сколько лиц в кадре
    cv.putText(frame, f'Face detected: {len(faces) if faces is not None else 0}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv.imshow(windows_name, frame)

    # Добавление возможности выйты
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv.getWindowProperty(windows_name, cv.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv.destroyAllWindows()