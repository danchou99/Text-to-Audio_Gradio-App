import gradio as gr
from gtts import gTTS
import os
import tempfile
from pydub import AudioSegment # Add this import

def text_to_audio(text):
    if not text:
        return None, "Please enter some text."

    try:
        tts = gTTS(text=text, lang='en')

        # Save to a temporary MP3 file first
        temp_mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_mp3_file_name = temp_mp3_file.name
        temp_mp3_file.close()
        tts.save(temp_mp3_file_name)

        # Convert MP3 to WAV
        temp_wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_wav_file_name = temp_wav_file.name
        temp_wav_file.close()

        audio = AudioSegment.from_mp3(temp_mp3_file_name)
        audio.export(temp_wav_file_name, format="wav")

        # Clean up the temporary MP3 file
        os.remove(temp_mp3_file_name)

        return temp_wav_file_name, "Audio generated successfully as WAV!"

    except Exception as e:
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
            return None, f"Error: FFmpeg not found or not in PATH. Please install FFmpeg to convert to WAV. Details: {e}"
        return None, f"Error generating audio: {e}"

# Gradio Interface
iface = gr.Interface(
    fn=text_to_audio,
    inputs=gr.Textbox(lines=5, label="Enter text here:", placeholder="Type your text for audio conversion..."),
    outputs=[
        gr.Audio(type="filepath", label="Generated Audio"),
        gr.Textbox(label="Status")
    ],
    title="Text-to-Audio Converter",
    description="Type some text in the box and click 'Submit' to convert it into an audio file (.wav format). Requires FFmpeg.",
    allow_flagging="never"
)

# Launch the Gradio app
if __name__ == "__main__":
    print("Launching Gradio app...")
    iface.launch(share=True)
    print("Gradio app launched. Open the URL in your browser.")