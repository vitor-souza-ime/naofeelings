# NAO Feelings

Real-time emotion detection system using the **NAO robot**, combining YOLO-based person detection and facial emotion analysis with DeepFace.

Repository: [https://github.com/vitor-souza-ime/naofellings](https://github.com/vitor-souza-ime/naofellings)

---

## Overview

This repository contains a Python implementation that connects to a NAO robot, captures camera images, detects people, and classifies their dominant emotion. The system can optionally provide feedback via TTS (text-to-speech) when the confidence is high.

---

## Features

1. Connects to the NAO robot via IP.
2. Captures video from NAO's camera (VGA resolution, RGB).
3. Detects people using YOLOv10.
4. Analyzes facial emotions using DeepFace.
5. Optional TTS feedback for high-confidence emotion detection.
6. Real-time visualization with bounding boxes and detected emotions.
7. Cooldown mechanism to avoid repeated detections.

---

## Requirements

- Python 3.10 or higher
- Python packages:
  - `qi` (NAO SDK)
  - `opencv-python`
  - `numpy`
  - `deepface`
  - `ultralytics` (YOLOv10)
  - `PyQt5`

Install dependencies with:

```bash
pip install -r requirements.txt
````

---

## Configuration

1. Update your NAO robot's IP in `main.py`:

```python
NAO_IP = "YOUR_NAO_IP"
NAO_PORT = 9559
```

2. Make sure NAO is powered on and connected to the same network as your computer.

3. To enable TTS output from NAO, uncomment the relevant line in the script:

```python
# tts_service.say(phrase)
```

---

## Running the System

Run the main script with:

```bash
python main.py
```

The system will display a window showing the camera feed, bounding boxes around detected people, and the dominant emotion. Press **`q`** to exit.

---

## Cooldown and Emotion Settings

* `DETECTION_COOLDOWN = 3.0`: Minimum time between emotion analyses of the same person.
* `EMOTION_THRESHOLD = 0.6`: Minimum confidence for triggering TTS response.

Supported emotions and associated phrases:

| Emotion  | Phrase                              |
| -------- | ----------------------------------- |
| happy    | You look happy! That's wonderful!   |
| sad      | You seem sad. Is everything okay?   |
| angry    | You look upset. Take a deep breath. |
| surprise | Oh, you look surprised!             |
| fear     | You look worried. Don't be afraid.  |
| disgust  | You seem bothered by something.     |
| neutral  | You look calm and peaceful.         |

---

## Notes

* Small regions of interest (ROIs) are automatically resized for reliable facial analysis.
* Tested under varying lighting conditions for robustness.
* Can be adapted to use a local webcam for development and testing without NAO.

---

## References

* YOLOv10: [https://ultralytics.com](https://ultralytics.com)
* DeepFace: [https://github.com/serengil/deepface](https://github.com/serengil/deepface)
* NAO SDK: [https://developer.softbankrobotics.com](https://developer.softbankrobotics.com)

---

## License

MIT License

