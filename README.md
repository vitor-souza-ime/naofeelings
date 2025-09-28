# NAO Feelings

Sistema de detecção de emoções em tempo real utilizando o robô **NAO**, combinando detecção de pessoas via YOLO e análise facial com DeepFace.

O repositório inclui a implementação em Python que captura imagens da câmera do NAO, detecta pessoas e classifica a emoção predominante, emitindo respostas por TTS (texto para fala) caso a confiança seja alta.

Repositório: [https://github.com/vitor-souza-ime/naofellings](https://github.com/vitor-souza-ime/naofellings)

---

## Conteúdo

- **main.py**: Script principal que conecta ao NAO, captura imagens, detecta pessoas e analisa emoções.
- **requirements.txt**: Dependências necessárias para executar o projeto.
- **README.md**: Documentação do projeto.

---

## Funcionalidades

1. Conexão com o robô NAO via IP.
2. Captura de vídeo da câmera do NAO (resolução VGA, RGB).
3. Detecção de pessoas usando modelo YOLOv10.
4. Análise de emoções faciais com DeepFace.
5. Feedback por TTS (opcional) quando a confiança da detecção é alta.
6. Visualização em tempo real das caixas delimitadoras e emoções na tela.
7. Controle de fluxo com cooldown entre detecções para evitar repetição excessiva.

---

## Requisitos

- Python 3.10 ou superior
- Bibliotecas:
  - `qi` (SDK do NAO)
  - `opencv-python`
  - `numpy`
  - `deepface`
  - `ultralytics` (YOLOv10)
  - `PyQt5`

Instalação das dependências:

```bash
pip install -r requirements.txt
````

---

## Configuração

1. Atualize o IP do seu robô NAO no arquivo `main.py`:

```python
NAO_IP = "SEU_IP_DO_NAO"
NAO_PORT = 9559
```

2. Certifique-se de que o NAO esteja ligado e conectado à mesma rede do computador.

3. Caso queira usar TTS do NAO, habilite a função:

```python
# tts_service.say(phrase)
```

---

## Execução

Para iniciar o sistema, execute:

```bash
python main.py
```

O sistema exibirá uma janela com a imagem da câmera, caixas delimitadoras para pessoas detectadas e a emoção predominante. Pressione **`q`** para sair.

---

## Estrutura de Cooldown e Emoções

* `DETECTION_COOLDOWN = 3.0`: Tempo mínimo entre análises de emoção da mesma pessoa.
* `EMOTION_THRESHOLD = 0.6`: Confiança mínima da detecção para emissão de resposta.

Emoções suportadas e frases associadas:

| Emoção   | Frase                               |
| -------- | ----------------------------------- |
| happy    | You look happy! That's wonderful!   |
| sad      | You seem sad. Is everything okay?   |
| angry    | You look upset. Take a deep breath. |
| surprise | Oh, you look surprised!             |
| fear     | You look worried. Don't be afraid.  |
| disgust  | You seem bothered by something.     |
| neutral  | You look calm and peaceful.         |

---

## Observações

* O script redimensiona automaticamente regiões de interesse pequenas para garantir boa análise facial.
* Testado com imagens do NAO em condições de iluminação variadas para avaliar robustez.
* Para desenvolvimento e testes locais sem NAO, pode-se adaptar o script para usar webcam.

---

## Referências

* YOLOv10: [https://ultralytics.com](https://ultralytics.com)
* DeepFace: [https://github.com/serengil/deepface](https://github.com/serengil/deepface)
* SDK do NAO: [https://developer.softbankrobotics.com](https://developer.softbankrobotics.com)

---

## Licença

MIT License


