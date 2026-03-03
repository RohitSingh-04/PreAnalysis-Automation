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
├── sample_data/            # Example Excel files for testing
├── start.py                # Entry point (GUI)
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

Executable builds can be generated using PyInstaller or Nuitka.  

# Spec file mandatory changes for pyinstaller

1. while generating the dist make sure to include hidden imports as well specially handle selenium

    ```
    import importlib.metadata
    import pkg_resources

    all_deps = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]

    all_deps.extend([
        'selenium.webdriver', 'selenium.webdriver.chrome.webdriver', 'selenium.webdriver.chrome.service', 'webdriver_manager', 'webdriver_manager.chrome'
    ])
    ```
    - at Analysis() update the hiddenimports and set to all_deps
    ```
    a = Analysis(
        ['start.py'],
        pathex=[],
        binaries=[],
        datas=[],
        hiddenimports=all_deps,
        hookspath=[],
        hooksconfig={},
        runtime_hooks=[],
        excludes=[],
        noarchive=False,
        optimize=0,
    )
    ```

# if using nuitka use the below command to build the exe

```
python -m nuitka --standalone --onefile --enable-plugin=tk-inter --include-package=selenium --include-package=webdriver_manager --windows-icon-from-ico=favicon/favicon_ico.ico --windows-company-name="Rohiyaa" --windows-console-mode=disable --windows-product-version="2.0.1" --assume-yes-for-downloads -o Alpha.exe start.py 
```
---
