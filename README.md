# 🧹 Data Review Tool

A powerful and user-friendly **Streamlit app** for customizing reports, reviewing Excel data, and highlighting changes — all in one streamlined workflow.  
Perfect for collaborative review teams dealing with messy Excel files, batch updates, or audit trails.

## 🚀 Features

### 📊 1. Report Customizer
- Reorder columns based on a provided template.
- Standardize Excel reports to match required format.
- Preview and download a **customized report** instantly.

### ✅ 2. Data Review Panel
- Upload and **edit data** in an Excel sheet.
- Add structured **comments** like: `Approved`, `Needs Change`, etc.
- Detect and **highlight modified cells** for transparent review.
  - 🟡 **Yellow** — changed cell  
  - 🟢 **Light Green** — approved rows  
  - 🔴 **Light Coral** — suspicious rows
- Download updates in a multi-sheet Excel file with:
  - Original Data
  - Edited Data
  - Pending / Approved / Approved with Changes / Needs Change sheets

### 🎯 3. Changes Highlighter
- Compare two Excel files (before vs after).
- Highlight changed cells in Yellow

## 📦 Installation

### 1. Install Python  
Download and install Python from [python.org](https://www.python.org/downloads).  
Make sure to check ✅ **"Add Python to PATH"** during installation.

### 2. Download This Repository (For Beginners)

- Go to the repo in your browser:  
   👉 [https://github.com/Charlie-lpy/photo-master](https://github.com/Charlie-lpy/photo-master)

- Click the green **"Code"** button, then select **"Download ZIP"**

- After downloading, **extract the ZIP file** to a folder on your computer (e.g., `D:\photo-master`)

- Open a terminal (Command Prompt), and navigate to that folder:
   ```bash
   cd path\to\your\photo-master
   ```

Once you're in the project folder, you're ready to set up the environment!

### 3. Create and Activate a Virtual Environment

```bash
python -m venv venv
```
Activate it:

```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

## 🌐 Usage with Streamlit Web App

Run the app using Streamlit:

```bash
streamlit run app.py
```

A web interface will open in your browser.  
Upload your Excel file and process photos in just a few clicks!
