"""
Film Script Reader - Gradio Web Interface
Upload PDF scripts, extract characters and dialogue, and convert to speech using ChatterboxTTS
"""
import gradio as gr
import os
import tempfile
import zipfile
from io import BytesIO
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
        return "Please upload a PDF file", {}, {}
    
    try:
        # Parse the script
        script_data = script_parser.parse_script(pdf_file)
        
        if not script_data:
            return "No characters or dialogue found in the PDF. Please check the format.", {}, {}
        
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
        
        return summary_text, script_data, summary
        
    except Exception as e:
        return f"Error processing PDF: {str(e)}", {}, {}

def create_character_interface(script_data):
    """Create dynamic interface for each character"""
    if not script_data:
        return []
    
    character_components = []
    
    for character, dialogue_lines in script_data.items():
        # Create a section for each character
        with gr.Column():
            gr.Markdown(f"### 🎭 {character}")
            
            # Show sample dialogue
            sample_text = "\n".join(dialogue_lines[:3])  # First 3 lines
            if len(dialogue_lines) > 3:
                sample_text += f"\n... ({len(dialogue_lines) - 3} more lines)"
            
            gr.Textbox(
                value=sample_text,
                label=f"Dialogue Preview ({len(dialogue_lines)} total lines)",
                lines=4,
                interactive=False
            )
            
            # Reference audio upload for this character
            ref_audio = gr.Audio(
                sources=["upload", "microphone"],
                type="filepath",
                label=f"Reference Voice for {character}"
            )
            
            # Convert button for this character
            convert_btn = gr.Button(
                f"🎤 Convert {character}'s Lines to Speech",
                variant="primary"
            )
            
            # Output audio for this character
            output_audio = gr.Audio(
                label=f"{character}'s Generated Speech",
                visible=False
            )
            
            # Download button for all character's audio files
            download_btn = gr.File(
                label=f"Download {character}'s Audio Files",
                visible=False
            )
            
            character_components.append({
                'character': character,
                'dialogue': dialogue_lines,
                'ref_audio': ref_audio,
                'convert_btn': convert_btn,
                'output_audio': output_audio,
                'download_btn': download_btn
            })
    
    return character_components

def convert_character_dialogue(character, dialogue_lines, reference_audio, progress=gr.Progress()):
    """Convert all dialogue lines for a character to speech"""
    if not dialogue_lines:
        return None, None
    
    # Load TTS model
    model = load_tts_model()
    
    audio_files = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        progress(0, desc=f"Converting {character}'s dialogue...")
        
        for i, line in enumerate(dialogue_lines):
            if len(line.strip()) < 3:  # Skip very short lines
                continue
                
            progress(i / len(dialogue_lines), desc=f"Converting line {i+1}/{len(dialogue_lines)}")
            
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
        
        progress(1.0, desc="Creating download package...")
        
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

def create_app():
    """Create the main Gradio application"""
    
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
        
        with gr.Row():
            with gr.Column(scale=1):
                # PDF Upload Section
                gr.Markdown("### 📁 Step 1: Upload Script")
                pdf_input = gr.File(
                    file_types=[".pdf"],
                    label="Upload PDF Film Script"
                )
                
                process_btn = gr.Button("📖 Process Script", variant="primary")
                
                # Script Analysis Results
                gr.Markdown("### 📊 Script Analysis")
                analysis_output = gr.Markdown(value="Upload a PDF to see analysis results...")
                
            with gr.Column(scale=2):
                # Character Processing Section
                gr.Markdown("### 🎭 Step 2: Character Voice Assignment & Conversion")
                
                # This will be populated dynamically
                character_section = gr.Column(visible=False)
        
        # Hidden state to store script data
        script_data_state = gr.State({})
        summary_state = gr.State({})
        
        # Process script when uploaded
        def on_process_script(pdf_file):
            summary_text, script_data, summary = process_script_pdf(pdf_file)
            
            if script_data:
                # Show character section
                return summary_text, script_data, summary, gr.update(visible=True)
            else:
                return summary_text, {}, {}, gr.update(visible=False)
        
        process_btn.click(
            fn=on_process_script,
            inputs=[pdf_input],
            outputs=[analysis_output, script_data_state, summary_state, character_section]
        )
        
        # Dynamic character interfaces (this is a simplified version)
        # In a more complex implementation, we'd create these dynamically
        with character_section:
            gr.Markdown("Characters and their dialogue will appear here after processing the script.")
    
    return app

# For dynamic character creation (more advanced implementation)
def create_character_tab(character, dialogue_lines):
    """Create a tab for a specific character"""
    with gr.TabItem(f"🎭 {character}"):
        gr.Markdown(f"### {character} ({len(dialogue_lines)} lines)")
        
        # Show dialogue preview
        dialogue_preview = gr.Textbox(
            value="\n".join(dialogue_lines[:5]) + (f"\n... and {len(dialogue_lines)-5} more lines" if len(dialogue_lines) > 5 else ""),
            label="Dialogue Preview",
            lines=6,
            interactive=False
        )
        
        with gr.Row():
            with gr.Column():
                ref_audio = gr.Audio(
                    sources=["upload", "microphone"],
                    type="filepath",
                    label=f"Reference Voice for {character}"
                )
                
                convert_btn = gr.Button(f"🎤 Convert All Lines", variant="primary")
            
            with gr.Column():
                preview_audio = gr.Audio(label="Preview (First Line)")
                download_zip = gr.File(label="Download All Audio Files")
        
        # Set up conversion
        def convert_wrapper(ref_audio_path):
            return convert_character_dialogue(character, dialogue_lines, ref_audio_path)
        
        convert_btn.click(
            fn=convert_wrapper,
            inputs=[ref_audio],
            outputs=[preview_audio, download_zip]
        )

if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7862, share=True)