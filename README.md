# 🎞️ Video Frame Extractor

A simple Streamlit web application that allows users to upload a video file, extract frames at regular customizable intervals (every 10, 20, 30, 40, or 50 frames), and preview them. You can download individual frames or download all extracted frames bundled together as a ZIP file.

## ✨ Features

- **Upload Video**: Supports common formats like MP4, MOV, AVI, and MKV.
- **Customizable Extraction Interval**: Choose to extract 1 frame every 10, 20, 30, 40, or 50 frames.
- **Adjustable Preview Grid**: View the extracted frames in different sizes (Super Small, Small, Medium, Large) using an interactive grid layout.
- **Download Options**: Download frames individually or all at once in a convenient `.zip` file.

---

## ☁️ Run in the Cloud

The easiest way to use the app is to run it directly in your browser without having to install anything!

👉 **[Access the App Here](https://exctractxframes.streamlit.app/)**

---

## 💻 Run Locally

If you prefer to run the application on your own machine, follow these steps:

### Prerequisites

Make sure you have Python installed. You will also need the following Python packages:
- `streamlit`
- `opencv-python-headless`
- `pillow`

### Installation

1. Clone or download this project to your computer.
2. Open your terminal or command prompt and navigate to the project folder.
3. Install the required dependencies by running:
   ```bash
   pip install streamlit opencv-python-headless pillow
   ```

### Running the Application

#### Using the Batch File (Windows only)
You can simply double-click the `run_app.bat` file. This will automatically open a command prompt and launch the local Streamlit server.

#### Using the Terminal (All Platforms)
Run the following command in your terminal:
```bash
python -m streamlit run app.py
```

The application will automatically open in your default web browser (usually at `http://localhost:8501`).
