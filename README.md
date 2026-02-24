# PreAnalysis Automation

A simple GUI tool for automating pre-analysis of Excel data files.  
This project provides a user interface to select a folder and process `.xlsx` Excel files using the internal automation logic in the `app` module.

---

## 🚀 Features

- 📁 Select a directory containing Excel (`.xlsx`) files  
- ⚙️ Automatically runs processing logic on all `.xlsx` files found  
- 📊 Displays a message upon successful or failed processing  
- 🪟 Simple GUI built with `tkinter`  

---

## 📦 Repository Structure

```
PreAnalysis-Automation/
├── app/                    # Main automation logic
├── build/AlphaV1.9/        # Build output (PyInstaller)
├── dist/                   # Distribution files
├── sample_data/            # Example Excel files for testing
├── start.py                # Entry point (GUI)
├── AlphaV1.9.spec          # PyInstaller spec file
├── requirements.txt        # Python dependencies
└── .gitignore              # Ignored files
```

---

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/RohitSingh-04/PreAnalysis-Automation.git
cd PreAnalysis-Automation
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🟢 Usage

Run the application using:

```bash
python start.py
```

- A folder selection dialog will appear.
- Choose a directory containing Excel (`.xlsx`) files.
- The application processes all valid Excel files.
- A success or error message is displayed once processing completes.

---

## ❓ Expected Input

- A directory containing one or more `.xlsx` Excel files.
- Processing logic is handled internally by the `app` module.

---

## 🧠 How It Works

1. Launches a Tkinter-based GUI
2. Accepts a folder path from the user
3. Identifies all Excel files in the folder
4. Passes files to the automation engine in `app.main`
5. Displays execution status to the user

---

## 🗂 Distribution

Executable builds are generated using PyInstaller.  
Build and distribution artifacts are stored in the `build/` and `dist/` directories.

---
