"""
Simplified Film Script Reader - Fixed Gradio Web Interface
Upload PDF scripts, extract characters and dialogue, and convert to speech using ChatterboxTTS
"""
import gradio as gr
import tempfile
import zipfile
import os
from script_parser import ScriptParser
from chatterbox.tts import ChatterboxTTS
import torch

# Initialize components
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
script_parser = ScriptParser()
tts_model = None

def load_tts_model():
    """Load TTS model once"""
    global tts_model
    if tts_model is None:
        tts_model = ChatterboxTTS.from_pretrained(DEVICE)
    return tts_model

def process_script_pdf(pdf_file):
    """Process uploaded PDF and extract characters/dialogue"""
    if pdf_file is None:
        return "Please upload a PDF file", {}
    
    try:
        # Parse the script
        script_data = script_parser.parse_script(pdf_file)
        
        if not script_data:
            return "No characters or dialogue found in the PDF. Please check the format.", {}
        
        # Get summary
        summary = script_parser.get_script_summary(script_data)
        
        # Create summary text
        summary_text = f"""
📚 **Script Analysis Complete!**

**📊 Summary:**
- **Characters Found:** {summary['character_count']}
- **Total Dialogue Lines:** {summary['total_dialogue_lines']}

**👥 Characters:**
"""
        for char, stats in summary['characters'].items():
            summary_text += f"- **{char}**: {stats['line_count']} lines, {stats['total_words']} words\n"
        
        return summary_text, script_data
        
    except Exception as e:
        return f"Error processing PDF: {str(e)}", {}

def convert_character_dialogue(character, dialogue_lines, reference_audio):
    """Convert all dialogue lines for a character to speech"""
    if not dialogue_lines or not reference_audio:
        return None, None
    
    # Load TTS model
    model = load_tts_model()
    
    audio_files = []
    temp_dir = tempfile.mkdtemp()
    
    try:        
        for i, line in enumerate(dialogue_lines):
            if len(line.strip()) < 3:  # Skip very short lines
                continue
            
            # Generate speech for this line
            wav = model.generate(
                line,
                audio_prompt_path=reference_audio,
                exaggeration=0.5,
                temperature=0.8,
            )
            
            # Save to temporary file
            audio_path = os.path.join(temp_dir, f"{character}_line_{i+1:03d}.wav")
            import soundfile as sf
            sf.write(audio_path, wav.squeeze(0).numpy(), model.sr)
            audio_files.append(audio_path)
        
        # Create zip file with all audio
        zip_path = os.path.join(temp_dir, f"{character}_all_lines.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for audio_file in audio_files:
                zipf.write(audio_file, os.path.basename(audio_file))
        
        # Return first audio file for preview and zip for download
        first_audio = audio_files[0] if audio_files else None
        
        return first_audio, zip_path
        
    except Exception as e:
        print(f"Error converting dialogue: {e}")
        return None, None

def update_character_display(script_data):
    """Update the character display based on script data"""
    if not script_data:
        return [gr.update(visible=False)] * 12
    
    characters = list(script_data.keys())
    updates = []
    
    # Character 1
    if len(characters) >= 1:
        char_name = characters[0]
        dialogue_lines = script_data[char_name]
        preview_text = "\n".join(dialogue_lines[:3])
        if len(dialogue_lines) > 3:
            preview_text += f"\n... and {len(dialogue_lines) - 3} more lines"
        
        updates.extend([
            gr.update(visible=True, value=f"### 🎭 {char_name} ({len(dialogue_lines)} lines)"),
            gr.update(visible=True, value=preview_text),
            gr.update(visible=True),  # ref_audio
            gr.update(visible=True, value=f"🎤 Convert {char_name}'s Lines")
        ])
    else:
        updates.extend([gr.update(visible=False)] * 4)
    
    # Character 2
    if len(characters) >= 2:
        char_name = characters[1]
        dialogue_lines = script_data[char_name]
        preview_text = "\n".join(dialogue_lines[:3])
        if len(dialogue_lines) > 3:
            preview_text += f"\n... and {len(dialogue_lines) - 3} more lines"
        
        updates.extend([
            gr.update(visible=True, value=f"### 🎭 {char_name} ({len(dialogue_lines)} lines)"),
            gr.update(visible=True, value=preview_text),
            gr.update(visible=True),  # ref_audio
            gr.update(visible=True, value=f"🎤 Convert {char_name}'s Lines")
        ])
    else:
        updates.extend([gr.update(visible=False)] * 4)
    
    # Character 3
    if len(characters) >= 3:
        char_name = characters[2]
        dialogue_lines = script_data[char_name]
        preview_text = "\n".join(dialogue_lines[:3])
        if len(dialogue_lines) > 3:
            preview_text += f"\n... and {len(dialogue_lines) - 3} more lines"
        
        updates.extend([
            gr.update(visible=True, value=f"### 🎭 {char_name} ({len(dialogue_lines)} lines)"),
            gr.update(visible=True, value=preview_text),
            gr.update(visible=True),  # ref_audio
            gr.update(visible=True, value=f"🎤 Convert {char_name}'s Lines")
        ])
    else:
        updates.extend([gr.update(visible=False)] * 4)
    
    return updates

def convert_char_1(ref_audio, script_data):
    """Convert character 1's dialogue"""
    if not script_data or not ref_audio:
        return "❌ Please upload reference audio", None, gr.update(visible=False), gr.update(visible=False)
    
    characters = list(script_data.keys())
    if len(characters) < 1:
        return "❌ No character found", None, gr.update(visible=False), gr.update(visible=False)
    
    char_name = characters[0]
    dialogue_lines = script_data[char_name]
    
    try:
        preview_audio, download_zip = convert_character_dialogue(char_name, dialogue_lines, ref_audio)
        if preview_audio and download_zip:
            return f"✅ Generated {len(dialogue_lines)} audio files for {char_name}!", preview_audio, gr.update(visible=True), gr.update(visible=True)
        else:
            return "❌ Conversion failed", None, gr.update(visible=False), gr.update(visible=False)
    except Exception as e:
        return f"❌ Error: {str(e)}", None, gr.update(visible=False), gr.update(visible=False)

def convert_char_2(ref_audio, script_data):
    """Convert character 2's dialogue"""
    if not script_data or not ref_audio:
        return "❌ Please upload reference audio", None, gr.update(visible=False), gr.update(visible=False)
    
    characters = list(script_data.keys())
    if len(characters) < 2:
        return "❌ No character found", None, gr.update(visible=False), gr.update(visible=False)
    
    char_name = characters[1]
    dialogue_lines = script_data[char_name]
    
    try:
        preview_audio, download_zip = convert_character_dialogue(char_name, dialogue_lines, ref_audio)
        if preview_audio and download_zip:
            return f"✅ Generated {len(dialogue_lines)} audio files for {char_name}!", preview_audio, gr.update(visible=True), gr.update(visible=True)
        else:
            return "❌ Conversion failed", None, gr.update(visible=False), gr.update(visible=False)
    except Exception as e:
        return f"❌ Error: {str(e)}", None, gr.update(visible=False), gr.update(visible=False)

def convert_char_3(ref_audio, script_data):
    """Convert character 3's dialogue"""
    if not script_data or not ref_audio:
        return "❌ Please upload reference audio", None, gr.update(visible=False), gr.update(visible=False)
    
    characters = list(script_data.keys())
    if len(characters) < 3:
        return "❌ No character found", None, gr.update(visible=False), gr.update(visible=False)
    
    char_name = characters[2]
    dialogue_lines = script_data[char_name]
    
    try:
        preview_audio, download_zip = convert_character_dialogue(char_name, dialogue_lines, ref_audio)
        if preview_audio and download_zip:
            return f"✅ Generated {len(dialogue_lines)} audio files for {char_name}!", preview_audio, gr.update(visible=True), gr.update(visible=True)
        else:
            return "❌ Conversion failed", None, gr.update(visible=False), gr.update(visible=False)
    except Exception as e:
        return f"❌ Error: {str(e)}", None, gr.update(visible=False), gr.update(visible=False)

# Create the Gradio interface
with gr.Blocks(title="🎬 Film Script Reader & TTS Converter", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🎬 Film Script Reader & TTS Converter
    
    Upload a PDF film script to extract characters and their dialogue, then convert each character's lines to speech using AI voice synthesis.
    
    ## How it works:
    1. **Upload** your PDF film script
    2. **Review** extracted characters and dialogue
    3. **Upload reference audio** for each character's voice
    4. **Convert** dialogue to speech for each character
    """)
    
    # Step 1: Upload and Process Script
    gr.Markdown("### 📁 Step 1: Upload Script")
    with gr.Row():
        pdf_input = gr.File(file_types=[".pdf"], label="Upload PDF Film Script")
        process_btn = gr.Button("📖 Process Script", variant="primary")
    
    # Script Analysis Results
    gr.Markdown("### 📊 Script Analysis")
    analysis_output = gr.Markdown(value="Upload a PDF to see analysis results...")
    
    # Step 2: Character Processing
    gr.Markdown("### 🎭 Step 2: Character Voice Assignment & Conversion")
    
    # Character 1
    with gr.Group():
        char1_name = gr.Markdown("### Character 1", visible=False)
        with gr.Row():
            with gr.Column():
                char1_dialogue = gr.Textbox(label="Dialogue Preview", lines=4, interactive=False, visible=False)
                char1_ref_audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Reference Voice", visible=False)
            with gr.Column():
                char1_convert_btn = gr.Button("🎤 Convert Lines", variant="primary", visible=False)
                char1_status = gr.Textbox(label="Status", value="Ready", interactive=False)
                char1_preview = gr.Audio(label="Preview", visible=False)
                char1_download = gr.File(label="Download Audio Files", visible=False)
    
    # Character 2
    with gr.Group():
        char2_name = gr.Markdown("### Character 2", visible=False)
        with gr.Row():
            with gr.Column():
                char2_dialogue = gr.Textbox(label="Dialogue Preview", lines=4, interactive=False, visible=False)
                char2_ref_audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Reference Voice", visible=False)
            with gr.Column():
                char2_convert_btn = gr.Button("🎤 Convert Lines", variant="primary", visible=False)
                char2_status = gr.Textbox(label="Status", value="Ready", interactive=False)
                char2_preview = gr.Audio(label="Preview", visible=False)
                char2_download = gr.File(label="Download Audio Files", visible=False)
    
    # Character 3
    with gr.Group():
        char3_name = gr.Markdown("### Character 3", visible=False)
        with gr.Row():
            with gr.Column():
                char3_dialogue = gr.Textbox(label="Dialogue Preview", lines=4, interactive=False, visible=False)
                char3_ref_audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Reference Voice", visible=False)
            with gr.Column():
                char3_convert_btn = gr.Button("🎤 Convert Lines", variant="primary", visible=False)
                char3_status = gr.Textbox(label="Status", value="Ready", interactive=False)
                char3_preview = gr.Audio(label="Preview", visible=False)
                char3_download = gr.File(label="Download Audio Files", visible=False)
    
    # Hidden state to store script data
    script_data_state = gr.State({})
    
    # Process script function
    def on_process_script(pdf_file):
        summary_text, script_data = process_script_pdf(pdf_file)
        
        if not script_data:
            return [summary_text, {}] + [gr.update(visible=False)] * 12
        
        # Update character displays
        character_updates = update_character_display(script_data)
        return [summary_text, script_data] + character_updates
    
    # Event handlers
    process_btn.click(
        fn=on_process_script,
        inputs=[pdf_input],
        outputs=[
            analysis_output, script_data_state,
            # Character outputs
            char1_name, char1_dialogue, char1_ref_audio, char1_convert_btn,
            char2_name, char2_dialogue, char2_ref_audio, char2_convert_btn,
            char3_name, char3_dialogue, char3_ref_audio, char3_convert_btn
        ]
    )
    
    # Character conversion buttons
    char1_convert_btn.click(
        fn=convert_char_1,
        inputs=[char1_ref_audio, script_data_state],
        outputs=[char1_status, char1_preview, char1_preview, char1_download]
    )
    
    char2_convert_btn.click(
        fn=convert_char_2,
        inputs=[char2_ref_audio, script_data_state],
        outputs=[char2_status, char2_preview, char2_preview, char2_download]
    )
    
    char3_convert_btn.click(
        fn=convert_char_3,
        inputs=[char3_ref_audio, script_data_state],
        outputs=[char3_status, char3_preview, char3_preview, char3_download]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0", 
        server_port=7862, 
        share=False,  # Keep private - no public tunnel
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
        ssl_verify=False
    )