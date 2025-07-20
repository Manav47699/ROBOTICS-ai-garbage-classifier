# ♻️ AI Garbage Classifier | TechnoMorph Hackathon 🛠️

This repository contains all the **python code**, **TinkerCAD circuit simulations**, and our **final presentation** for the TechnoMorph Hackathon, where our project — an AI-powered smart garbage classifier — proudly won **🏆 2nd Runner-up**!

---

## 🚀 Project Summary

Our system uses a combination of **AI**, **computer vision**, **serial communication** and **IoT** to classify waste as **plastic** or **paper**, and automatically dispose it into the correct bin using servo motors. It's an end-to-end automation solution that merges software intelligence with hardware control.

---

## 🧠 Software Overview

| Technology     | Purpose                                         |
|----------------|--------------------------------------------------|
| `TensorFlow / Keras` | Custom image classification model |
| `YOLOv5`       | Real-time object detection (e.g. plastic vs paper) |
| `MediaPipe`    | Hand gesture detection & tracking                |
| `OpenCV`       | Webcam input & frame processing                  |
| `com0com`      | Virtual serial communication between Python & Arduino |

> 🔧 We’ve structured the codebase into multiple experimental scripts — each exploring different combinations of these technologies.

---

## 🔌 Hardware Overview

| Component            | Role                                                      |
|----------------------|-----------------------------------------------------------|
| `Arduino UNO`        | Main microcontroller                                      |
| `Bluetooth Module`   | Wireless communication (alternative to USB)              |
| `IR Sensor`          | Detects user's hand after garbage is thrown              |
| `Ultrasonic Sensors` | Detects if the bin is full                                |
| `Servo Motors`       | Controls the lid of garbage bins                          |
| `LED`                | Visual signal indicators (success, overflow, etc.)       |

---

## 🧭 System Workflow

<img width="1350" height="569" alt="workflow" src="https://github.com/user-attachments/assets/2ff5c47e-d707-4c71-b14c-f877bc2b64af" />

---

## 🔬 TinkerCAD Simulation (Circuit)

▶ **[Click to Open Simulation](https://www.tinkercad.com/things/2TMN1thgRsH-techo-morph-project)**  
Simulates the hardware control logic of our smart bin.

---

## 🖼️ Gallery

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/642c3965-8cd8-41f3-bcb4-14a1f8772d29" width="100%"/></td>
    <td><img src="https://github.com/user-attachments/assets/4b3ec6b8-e9c1-46fa-940e-908d196245f1" width="100%"/></td>
    <td><img src="https://github.com/user-attachments/assets/79e1d0a3-d133-4418-8b9b-99314439d7be" width="100%"/></td>
  </tr>
</table>

---

## 🏁 Achievements

✅ 2nd Runner-Up at **TechnoMorph Hackathon 2025**  
✅ Integrated real-time AI + hardware  
✅ Hands-free, gesture-enabled interaction  
✅ Full-cycle automation — from classification to disposal

---

## 💡 Future Enhancements

- [ ] Add voice feedback using Text-to-Speech (TTS)
- [ ] Integrate overflow detection with real IR sensors
- [ ] Deploy a web dashboard for monitoring and reporting

---

> Made with 💚 by [TEAM BINFINITY].
