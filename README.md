# 🔐 Bank CAPTCHA Recognition

This project is a Python-based system for recognizing CAPTCHA images from MB Bank using deep learning (PyTorch). It includes image scraping, dataset handling, model training, and prediction through a simple server.

---

## 📁 Project Structure

```
.
├── __pycache__/                # Python cache files
├── mbbank_dataset/            # (Likely) contains training/testing image sets
├── CONFIG.py                  # Configuration for model and dataset (char set, image size, etc.)
├── MAIN.py                    # Main script for training and testing the model
├── datasets.py                # Custom PyTorch dataset classes
├── mbbank_scrapping.py        # Script to scrape CAPTCHA images from MB Bank
├── model.pth                  # Trained PyTorch model
├── requirements.txt           # Python dependencies
├── server.py                  # Flask API for inference
└── temp.png                   # Temp file used during prediction
```

---

## 🚀 Features

* ✅ Download CAPTCHA images directly from the bank site
* ✅ Train a CNN model using PyTorch
* ✅ Evaluate and predict CAPTCHA text
* ✅ Serve predictions via a Flask API (`server.py`)
* ✅ Save base64 images or decode them directly for inference

---

## 📦 Installation

```bash
git clone <repo-url>
cd <project-folder>
pip install -r requirements.txt
```

---

## 📥 Download CAPTCHA Images

You can collect images using:

```bash
python mbbank_scrapping.py
```

Images will be saved (likely) into `mbbank_dataset/` or a similar folder. Adjust inside `mbbank_scrapping.py` if needed.

---

## 🏋️ Train the Model

Make sure the training images are in the correct format (image name = label, e.g., `ABC123.jpg`).

```bash
python MAIN.py
```

> This will train a CNN on the dataset and save the model as `model.pth`.

---

## 🔍 Predict CAPTCHA (Batch or Single)

To predict all CAPTCHA images in a folder:

```bash
python MAIN.py
# Internally calls `check_all()` to run inference on `./data/test/`
```

---

## 🌐 Run the API Server

Start a local Flask server to handle image prediction requests:

```bash
python server.py
```

### Example API Usage

**POST /predict**

* Form-data: `image` (file)
* JSON: `image_base64` (string)

```bash
curl -X POST -F "image=@temp.png" http://localhost:8001/predict
```

OR

```json
{
  "image_base64": "data:image/png;base64,iVBORw0KG..."
}
```

---

## 🔠 Character Set

The model supports the following characters:

```
123456789ABDEFGHJMNRTYabdefghjmnqrty
```

---

## 🖼 Image Format

* Width: `200px`
* Height: `35px`
* CAPTCHA Length: `6`

---

## 🧪 Example Output

The prediction system uses softmax and argmax over CNN outputs and maps indices to characters defined in `CONFIG.py`.

---

## 📄 Requirements

Install dependencies via:

```bash
pip install -r requirements.txt
```

You may find:

```
torch
torchvision
flask
Pillow
shortuuid
numpy
```

---

## 🛠️ Notes

* `model.pth` is the trained model and will be loaded during inference.
* `temp.png` is used as a staging file during predictions via API or script.
* Adjust `CONFIG.py` for different CAPTCHA sources or configurations.

---

## 📧 License

This project is provided for educational purposes only. Use responsibly.

---

Let me know if you want the README file exported or modified to support Docker, advanced usage, or model visualization.
