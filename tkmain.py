import tkinter as tk
from tkinter import ttk
import cv2
from ultralytics import YOLO
import numpy as np
import pygame
import threading

MODEL_PATH = "weights/best.pt"
ALERT_SOUND = "sound/danger3.mp3"

# Variáveis globais para o tamanho do retângulo
rect_width = 100
rect_height = 200

def load_model(MODEL_PATH):
    """Carrega o YOLO"""
    return YOLO(MODEL_PATH)

def open_video_source():
    """Abre o fonte de vídeo (webCam ou arquivo)"""
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Sem fonte em 0, tentando em 1")
        cap = cv2.VideoCapture(0)
    elif not cap.isOpened():
        raise ValueError("Erro: sem fonte de vídeo")
    return cap

def process_frame(frame, model, conf_threshold):
    """Processa um único quadro e retorna o frame com a segmentação aplicada"""
    results = model(frame, conf=conf_threshold)
    masks = results[0].masks.data.cpu().numpy() if results[0].masks is not None else []
    mask_overlay = np.zeros_like(frame, dtype=np.uint8)

    for mask in masks:
        mask_binary = (mask * 255).astype(np.uint8)
        mask_binary_resized = cv2.resize(mask_binary, (frame.shape[1], frame.shape[0]))

        if len(mask_binary_resized.shape) == 2:
            mask_binary_resized = cv2.cvtColor(mask_binary_resized, cv2.COLOR_GRAY2BGR)

        color_mask = mask_binary_resized * np.array([255, 55, 0], dtype=np.uint8)
        mask_overlay = cv2.add(mask_overlay, color_mask)

    return cv2.addWeighted(frame, 0.6, mask_overlay, 0.4, 0), masks

def draw_center_rectangle(frame, change_color=False):
    """Desenha um retângulo no centro do frame."""
    global rect_width, rect_height
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2

    top_left = (center_x - rect_width // 2, center_y - rect_height // 2)
    bottom_right = (center_x + rect_width // 2, center_y + rect_height // 2)
    color = (0, 0, 255) if change_color else (0, 255, 255)

    if change_color:
        cv2.putText(frame, "PERIGO!", (center_x - 40, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    return cv2.rectangle(frame, top_left, bottom_right, color, 3)

def play_sound():
    """Função para tocar o som em uma thread separada."""
    pygame.mixer.init()
    pygame.mixer.music.load(ALERT_SOUND)
    pygame.mixer.music.play(-1)

def stop_sound():
    """Função para parar o som."""
    pygame.mixer.music.stop()

def run_segmentation(conf_threshold=0.70):
    global rect_width, rect_height

    try:
        model = load_model(MODEL_PATH)
        cap = open_video_source()

        sound_played = False

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro: não foi possível capturar o quadro")
                break

            frame, masks = process_frame(frame, model, conf_threshold)

            # Verifica se a máscara da luva está dentro do retângulo
            is_mask_inside = check_mask_inside_rectangle(masks, frame)

            if is_mask_inside and not sound_played:
                sound_thread = threading.Thread(target=play_sound)
                sound_thread.start()
                sound_played = True
            elif not is_mask_inside and sound_played:
                stop_sound()
                sound_played = False

            frame = draw_center_rectangle(frame, change_color=is_mask_inside)
            cv2.imshow("Reconhecimento de Luva", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except ValueError as e:
        print(e)

def check_mask_inside_rectangle(masks, frame):
    """Verifica se qualquer parte da máscara da luva está dentro do retângulo central."""
    global rect_width, rect_height
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2

    top_left = (center_x - rect_width // 2, center_y - rect_height // 2)
    bottom_right = (center_x + rect_width // 2, center_y + rect_height // 2)

    for mask in masks:
        mask_binary = (mask * 255).astype(np.uint8)
        mask_binary_resized = cv2.resize(mask_binary, (frame.shape[1], frame.shape[0]))

        contours, _ = cv2.findContours(mask_binary_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            for point in contour:
                x, y = point[0]
                if top_left[0] <= x <= bottom_right[0] and top_left[1] <= y <= bottom_right[1]:
                    return True

    return False

def start_tkinter_interface():
    """Cria a interface Tkinter para controlar o tamanho do retângulo."""
    global rect_width, rect_height

    def update_width(value):
        """Atualiza a largura do retângulo com o valor do slider."""
        global rect_width
        rect_width = int(float(value))  # Corrigido para lidar com valores float do slider


    def update_height(value):
        """Atualiza a altura do retângulo com o valor do slider."""
        global rect_height
        rect_height = int(float(value))  # Corrigido para lidar com valores float do slider

    root = tk.Tk()
    root.title("Configuração do Retângulo")

    tk.Label(root, text="Largura").pack()
    width_slider = ttk.Scale(root, from_=50, to=500, orient='horizontal', command=update_width)
    width_slider.set(rect_width)
    width_slider.pack()

    tk.Label(root, text="Altura").pack()
    height_slider = ttk.Scale(root, from_=50, to=500, orient='horizontal', command=update_height)
    height_slider.set(rect_height)
    height_slider.pack()

    root.mainloop()

if __name__ == "__main__":
    # Inicia a interface Tkinter em uma thread separada
    threading.Thread(target=start_tkinter_interface, daemon=True).start()

    # Inicia a segmentação em tempo real
    run_segmentation()
