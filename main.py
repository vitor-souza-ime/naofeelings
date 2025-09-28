import qi
import cv2
import numpy as np
from deepface import DeepFace
from ultralytics import YOLO
import time

# Configuração da sessão com o NAO
NAO_IP = "172.15.1.29"   # altere para o IP do seu NAO
NAO_PORT = 9559

session = qi.Session()
try:
    session.connect(f"tcp://{NAO_IP}:{NAO_PORT}")
    print("Conectado ao NAO!")
except RuntimeError as e:
    print(f"Erro: não foi possível conectar ao NAO: {e}")
    exit(1)

# Serviços do NAO
video_service = session.service("ALVideoDevice")
tts_service = session.service("ALTextToSpeech")

# Inscrição na câmera do NAO (resolução: VGA, colorspace: RGB)
try:
    subscriber_id = video_service.subscribeCamera(
        "emotion_detection", 0, 2, 11, 10  # resolução VGA (640x480)
    )
    print("Câmera inscrita com sucesso!")
except Exception as e:
    print(f"Erro ao inscrever câmera: {e}")
    exit(1)

# Carregar modelo YOLO para detecção de pessoas
try:
    yolo_model = YOLO("yolov10n.pt")
    print("Modelo YOLO carregado!")
except Exception as e:
    print(f"Erro ao carregar YOLO: {e}")
    exit(1)

# Configurações
EMOTION_THRESHOLD = 0.6  # Reduzido para 60%
DETECTION_COOLDOWN = 3.0  # Cooldown de 3 segundos entre detecções

# Controle de tempo e estado
last_emotion = None
last_detection_time = 0
frame_count = 0

# Frases associadas a cada emoção
emotion_phrases = {
    "happy": "You look happy! That's wonderful!",
    "sad": "You seem sad. Is everything okay?",
    "angry": "You look upset. Take a deep breath.",
    "surprise": "Oh, you look surprised!",
    "fear": "You look worried. Don't be afraid.",
    "disgust": "You seem bothered by something.",
    "neutral": "You look calm and peaceful."
}

print("Sistema iniciado! Pressione 'q' para sair.")
print("Procurando por pessoas...")

try:
    while True:
        frame_count += 1
        current_time = time.time()
        
        # Obter imagem da câmera
        try:
            nao_image = video_service.getImageRemote(subscriber_id)
            if nao_image is None:
                print("Nenhuma imagem recebida")
                continue
        except Exception as e:
            print(f"Erro ao capturar imagem: {e}")
            continue

        # Extrair dados da imagem
        width, height = nao_image[0], nao_image[1]
        array = nao_image[6]

        # Converter para array numpy
        try:
            # NAO retorna imagem em RGB
            frame = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Erro na conversão da imagem: {e}")
            continue

        # Debug: mostrar frame a cada 30 frames
        if frame_count % 30 == 0:
            print(f"Frame {frame_count} - Resolução: {width}x{height}")

        # Detectar pessoas com YOLO
        try:
            results = yolo_model(frame_bgr, classes=[0], verbose=False)  # classe 0 = pessoa
            person_detected = False

            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Extrair coordenadas da caixa delimitadora
                        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                        conf = float(box.conf[0].cpu().numpy())
                        
                        # Filtrar detecções com baixa confiança
                        if conf < 0.5:
                            continue
                            
                        person_detected = True
                        
                        # Extrair região da pessoa
                        person_roi = frame_bgr[y1:y2, x1:x2]
                        
                        # Verificar se a ROI é válida
                        if person_roi.size == 0:
                            continue
                            
                        # Desenhar caixa da pessoa
                        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame_bgr, f"Person ({conf:.2f})", (x1, y1 - 30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                        # Analisar emoção apenas se passou o cooldown
                        if current_time - last_detection_time > DETECTION_COOLDOWN:
                            try:
                                # Redimensionar ROI se muito pequena
                                if person_roi.shape[0] < 50 or person_roi.shape[1] < 50:
                                    person_roi = cv2.resize(person_roi, (100, 100))
                                
                                # Analisar emoção
                                analysis = DeepFace.analyze(
                                    person_roi, 
                                    actions=['emotion'], 
                                    enforce_detection=False,
                                    silent=True
                                )
                                
                                # Tratar caso de múltiplas faces ou uma face
                                if isinstance(analysis, list):
                                    analysis = analysis[0]
                                
                                dominant_emotion = analysis['dominant_emotion']
                                emotion_scores = analysis['emotion']
                                emotion_conf = emotion_scores[dominant_emotion]
                                
                                # Mostrar emoção na imagem
                                emotion_text = f"{dominant_emotion}: {emotion_conf:.1f}%"
                                cv2.putText(frame_bgr, emotion_text, (x1, y1 - 10),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                                
                                print(f"Emoção detectada: {dominant_emotion} ({emotion_conf:.1f}%)")
                                
                                # Falar se confiança alta e emoção diferente
                                if (emotion_conf >= EMOTION_THRESHOLD * 100 and 
                                    dominant_emotion != last_emotion):
                                    
                                    phrase = emotion_phrases.get(dominant_emotion.lower(), "Hello there!")
                                    print(f"Falando: {phrase}")
                                    
                                    try:
                                        #tts_service.say(phrase)
                                        last_emotion = dominant_emotion
                                        last_detection_time = current_time
                                    except Exception as e:
                                        print(f"Erro no TTS: {e}")
                                        
                            except Exception as e:
                                print(f"Erro na análise de emoção: {e}")
                                # Mostrar erro na imagem
                                cv2.putText(frame_bgr, "Emotion: Error", (x1, y1 - 10),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        except Exception as e:
            print(f"Erro na detecção YOLO: {e}")

        # Reset da última emoção se nenhuma pessoa detectada
        if not person_detected:
            if last_emotion is not None:
                print("Nenhuma pessoa detectada - resetando estado")
            last_emotion = None

        # Mostrar frame
        try:
            cv2.imshow("NAO Emotion Detection", frame_bgr)
        except Exception as e:
            print(f"Erro ao mostrar imagem: {e}")

        # Verificar tecla para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Saindo...")
            break

except KeyboardInterrupt:
    print("Interrompido pelo usuário")

finally:
    # Limpeza
    try:
        video_service.unsubscribe(subscriber_id)
        print("Câmera desinscrita")
    except:
        pass
    
    try:
        cv2.destroyAllWindows()
    except:
        pass
    
    print("Finalizado!")
