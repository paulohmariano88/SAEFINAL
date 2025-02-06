import cv2
from ultralytics import YOLO
import threading

def run_segmentation(model_path, source=0, conf_threshold=0.879):
    """
    Executa a segmentação em tempo real usando o modelo YOLOv8-Seg com confiança mínima de 87.9%.

    Args:
        model_path (str): Caminho para o modelo YOLOv8-Seg treinado (ex: 'best.pt').
        source (int or str): 0 para webcam, ou caminho para arquivo de vídeo.
        conf_threshold (float): Limiar de confiança para filtrar as detecções (default: 0.879).
    """

    # Carrega o modelo YOLOv8-Seg
    model = YOLO(model_path)

    # Abre a fonte de vídeo (webcam ou arquivo de vídeo)
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Erro: Não foi possível abrir a fonte de vídeo.")
        return

    # Reduz a resolução do vídeo para aumentar a velocidade
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Cria uma janela fixa
    cv2.namedWindow("Segmentação YOLOv8-Seg", cv2.WINDOW_NORMAL)

    def process_frame():
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro: Não foi possível capturar o quadro.")
                break

            # Realiza a inferência com o limiar de confiança especificado
            results = model(frame, conf=conf_threshold)

            # Desenha os resultados da segmentação no frame
            annotated_frame = results[0].plot()

            # Exibe o frame anotado na janela fixa
            cv2.imshow("Segmentação YOLOv8-Seg", annotated_frame)

            # Pressione 'q' para sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Usa threading para processar os frames
    thread = threading.Thread(target=process_frame)
    thread.start()
    thread.join()

    # Libera os recursos
    cap.release()
    cv2.destroyAllWindows()

# Caminho para o modelo YOLOv8-Seg treinado
model_path = "weights/best2.pt"  # Substitua pelo caminho correto do seu modelo

# Fonte de vídeo: 0 para webcam, ou caminho para um arquivo de vídeo
source = 0  # Para webcam, ou 'caminho/para/video.mp4' para vídeo

# Executa o teste de segmentação com confiança mínima de 87.9%
run_segmentation(model_path, source)