import gradio as gr
from gtts import gTTS
import os
import tempfile
from pydub import AudioSegment 
import google.generativeai as genai

#fecth API key from environment variable
GEMEINI_API_KEY = os.getenv("GEMEINI_API_KEY")

if not GEMEINI_API_KEY:
    raise ValueError("GEMEINI_API_KEY environment variable is not set. Please set it to your Google Generative AI API key.")

genai.configure(api_key=GEMEINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

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

def get_llm_response(question):
    if not question:
        return "Please enter a question."

    try:
        response = model.generate_content(contents=question)
        llm_response_text = response.text
        return llm_response_text, "LLM response generated successfully!" #, response.status

    except Exception as e:
        return f"Error generating response: {e}"
    
def ask_llm_and_convert_to_audio(question):
    llm_response_text, llm_status, *_ = get_llm_response(question)

    audio_file_path, audio_status = text_to_audio(llm_response_text)

    if not llm_response_text:
        return None, llm_status
    
    audio_file_path, audio_status = text_to_audio(llm_response_text)
    if not audio_file_path:
        return None, audio_status
    
    return llm_response_text, audio_file_path, f"LLM response: {llm_response_text}\n{audio_status}"


with gr.Blocks() as demo:
    gr.Markdown("""

    # LLM response to Audio Converter
    # Ask  a question to LLM and get its response in audio format to hear""")

    with gr.Row():
        with gr.Column(scale=2):
            question_input = gr.Textbox(lines=3, label="Enter your question:", placeholder="Type your question here...")
            submit_button = gr.Button("Get LLM Response and Convert to Audio")
        
        with gr.Column():
            llm_response_output = gr.Textbox(lines=5, label="LLM Response", interactive=False)
            audio_output = gr.Audio(label="Generated Audio", type="filepath")
            status_output = gr.Textbox(label="Status", interactive=False)

        submit_button.click(
            fn=ask_llm_and_convert_to_audio,
            inputs=[question_input],
            outputs=[llm_response_output, audio_output, status_output]
        )
# Gradio Interface
'''iface = gr.Interface(
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
'''
# Launch the Gradio app
if __name__ == "__main__":
    print("Launching Gradio app...")
    demo.launch(share=True)
    print("Gradio app launched. Open the URL in your browser.")