# 🔐 AUTHENTIC-ID

AI-powered system for detecting deepfake images and verifying user age to ensure secure access control.

---

## 📥 Download Models

Due to GitHub file size limits, model files are not included in this repository.

👉 Download models from here:
[Download Models](https://drive.google.com/drive/folders/1c0CRdq8RlzhXcxZxzla9n7IETusi4it2?usp=sharing)

📌 After downloading, place them inside the `models/` folder.

---

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/arshahmad214/AUTHENTIC-ID.git
cd AUTHENTIC-ID
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Download models

* Download from the link above
* Place inside `models/` folder

---

### 4. Run the application

```bash
python app.py
```

---

### 5. Open in browser

```
http://127.0.0.1:5000/
```

---

## 🧠 How It Works

* User uploads image
* Deepfake model checks authenticity
* If real → age model predicts age
* System decides access

---

## 📂 Project Structure

```
AUTHENTIC-ID/
│── app.py
│── requirements.txt
│── README.md
│
├── templates/
├── static/
├── models/
├── utils/
```








