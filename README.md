# Text-to-Audio Converter Gradio App

A simple Gradio web application that converts text input into an audio file.

## Features

* Converts text to speech using Google Text-to-Speech (`gTTS`).
* Outputs audio in WAV if `ffmpeg` and `pydub` are installed.
* User-friendly web interface powered by Gradio.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/danchou99/text-to-audio-gradio.git
    cd text-to-audio-gradio
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows (PowerShell):
    .venv\Scripts\Activate.ps1
    # On Windows (Command Prompt):
    .venv\Scripts\activate.bat
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    * **Note for WAV output:** If you intend to use the WAV output version, you also need to install `ffmpeg` on your system and ensure it's in your system's PATH. Refer to [FFmpeg website](https://ffmpeg.org/download.html) for installation instructions.

## How to Run

1.  Activate your virtual environment (if not already active).
2.  Run the Gradio application:
    ```bash
    python app.py
    ```
3.  Open the provided URL (e.g., `http://127.0.0.1:7860`) in your web browser.

## Usage

1.  Enter your desired text in the input box.
2.  Click the "Submit" button.
3.  The generated audio will appear below, which you can play or download.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests.

## License

NAM
