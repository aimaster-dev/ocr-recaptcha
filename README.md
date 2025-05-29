# 🔐 OCR ReCaptcha Solver (MB Bank CAPTCHA)

This project is an end-to-end OCR system designed to recognize CAPTCHA images—specifically from MB Bank (Vietnam). It includes tools to **scrape**, **train**, and **serve** a model that can decode distorted characters from CAPTCHA images using deep learning.

---

## 📸 Overview

![example](https://github.com/aimaster-dev/ocr-recaptcha/raw/main/temp.png)

---

## 🧠 Features

* 🚀 **CNN-based CAPTCHA recognition** using PyTorch
* 🛠 **Custom Dataset loader** with multi-label classification
* 📥 **CAPTCHA scraper** from MB Bank login page
* 🌐 **Flask API server** for real-time predictions
* 📦 Clean and modular structure for training + inference

---

## 🗂️ Project Structure

```bash
ocr-recaptcha/
├── __pycache__/                # Python cache
├── mbbank_dataset/            # Folder for training/test CAPTCHA images
├── CONFIG.py                  # Configuration (image size, char set, model path)
├── MAIN.py                    # Main script to train or test the model
├── datasets.py                # Custom PyTorch Dataset class
├── mbbank_scrapping.py        # Script to scrape new CAPTCHA images
├── model.pth                  # Trained CNN model
├── requirements.txt           # Python dependencies
├── server.py                  # Flask server for API-based prediction
├── temp.png                   # Temporary file used for API testing
```

---

## ⚙️ Installation

```bash
git clone https://github.com/aimaster-dev/ocr-recaptcha.git
cd ocr-recaptcha
pip install -r requirements.txt
```

---

## 📥 Scrape CAPTCHA Images

Run the scraping script to download new CAPTCHA images:

```bash
python mbbank_scrapping.py
```

Images are saved into `mbbank_dataset/` (you can modify this inside the script).

---

## 🏋️ Train the Model

Ensure your image filenames represent the correct CAPTCHA labels (e.g., `AB12cd.jpg`):

```bash
python MAIN.py
```

This will train the CNN and save the weights to `model.pth`.

---

## 🔍 Test the Model

To test the model on all CAPTCHA images in a folder:

```bash
# Inside MAIN.py, you can call:
CrackLettesInt4().check_all('mbbank_dataset/test')
```

This will:

* Predict each CAPTCHA
* Print the result
* Move it to `./test/<prediction>.jpg`

---

## 🌐 Run the Flask API

Start a REST API server for inference:

```bash
python server.py
```

### 🧪 Test API

Send a file:

```bash
curl -X POST -F "image=@mbbank_dataset/sample.jpg" http://localhost:8001/predict
```

Send base64:

```json
POST /predict
{
  "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

Response:

```json
{
  "prediction": ["4Hd6Rf"]
}
```

---

## 🔠 Character Set

Supported characters (from `CONFIG.py`):

```
123456789ABDEFGHJMNRTYabdefghjmnqrty
```

* CAPTCHA Length: 6
* Image Size: `200x35`

---

## 🧾 Requirements

```txt
torch
torchvision
flask
Pillow
numpy
shortuuid
```

Install via:

```bash
pip install -r requirements.txt
```

---

## ✅ Tips

* Customize CAPTCHA source URLs in `mbbank_scrapping.py`.
* Update image paths or save logic in `MAIN.py` and `datasets.py` if needed.
* To extend: Add beam search, augmentations, or use CRNN with CTC for harder CAPTCHAs.

---

## 🧑‍💻 Author

Maintained by **[aimaster-dev](https://github.com/aimaster-dev)**.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
