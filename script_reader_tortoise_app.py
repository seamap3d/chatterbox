"""
Script Reader with Tortoise TTS backend.
Reuses script parsing and lets users assign characters to voice samples.
"""
import inspect
import os
import tempfile
import zipfile

import gradio as gr
import numpy as np
import torch

from script_parser import ScriptParser


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEFAULT_PRESET = "high_quality"
FALLBACK_SAMPLE_RATE = 24000

script_parser = ScriptParser()
tts_model = None


def load_tortoise():
    """Lazy-load Tortoise TTS with a best-effort compatible signature."""
    global tts_model
    if tts_model is not None:
        return tts_model

    try:
        from tortoise.api import TextToSpeech
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Tortoise TTS is not available. Install tortoise-tts-fast and its deps in this environment."
        ) from exc

    kwargs = {}
    try:
        sig = inspect.signature(TextToSpeech)
        if "device" in sig.parameters:
            kwargs["device"] = DEVICE
        if "use_deepspeed" in sig.parameters:
            kwargs["use_deepspeed"] = False
    except Exception:
        pass

    tts_model = TextToSpeech(**kwargs)
    return tts_model


def load_voice_samples(audio_path, sample_rate):
    from tortoise.utils.audio import load_audio

    wav = load_audio(audio_path, sample_rate)
    return [wav]


def get_sample_rate(tts):
    return getattr(tts, "sample_rate", FALLBACK_SAMPLE_RATE)


def tts_generate(tts, text, voice_samples, preset):
    if hasattr(tts, "tts_with_preset"):
        return tts.tts_with_preset(text, voice_samples=voice_samples, preset=preset)
    return tts.tts(text, voice_samples=voice_samples)


def process_script_pdf(pdf_file):
    if pdf_file is None:
        return "Please upload a PDF file", {}

    try:
        script_data = script_parser.parse_script(pdf_file)
        if not script_data:
            return "No characters or dialogue found in the PDF.", {}

        summary = script_parser.get_script_summary(script_data)
        summary_lines = [
            "Script analysis complete.",
            "",
            f"Characters found: {summary['character_count']}",
            f"Total dialogue lines: {summary['total_dialogue_lines']}",
            "",
            "Characters:",
        ]
        for char, stats in summary["characters"].items():
            summary_lines.append(f"- {char}: {stats['line_count']} lines, {stats['total_words']} words")
        return "\n".join(summary_lines), script_data
    except Exception as exc:  # noqa: BLE001
        return f"Error processing PDF: {exc}", {}


def preview_text_for_character(character_name, script_data):
    if not character_name or character_name not in script_data:
        return ""
    lines = script_data[character_name]
    preview = "\n".join(lines[:3])
    if len(lines) > 3:
        preview += f"\n... and {len(lines) - 3} more lines"
    return preview


def default_characters(script_data, slots=3):
    characters = list(script_data.keys())
    defaults = characters[:slots]
    while len(defaults) < slots:
        defaults.append(None)
    return defaults


def convert_character_dialogue(character, dialogue_lines, reference_audio, preset):
    if not dialogue_lines or not reference_audio:
        return None, None

    tts = load_tortoise()
    sample_rate = get_sample_rate(tts)
    voice_samples = load_voice_samples(reference_audio, sample_rate)

    audio_files = []
    temp_dir = tempfile.mkdtemp()
    for idx, line in enumerate(dialogue_lines):
        if len(line.strip()) < 3:
            continue
        wav = tts_generate(tts, line, voice_samples=voice_samples, preset=preset)
        if torch.is_tensor(wav):
            wav = wav.squeeze(0).detach().cpu().numpy()
        else:
            wav = np.asarray(wav).squeeze()
        audio_path = os.path.join(temp_dir, f"{character}_line_{idx + 1:03d}.wav")
        import soundfile as sf

        sf.write(audio_path, wav, sample_rate)
        audio_files.append(audio_path)

    if not audio_files:
        return None, None

    zip_path = os.path.join(temp_dir, f"{character}_all_lines.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for audio_file in audio_files:
            zipf.write(audio_file, os.path.basename(audio_file))

    return audio_files[0], zip_path


def convert_slot(character_name, reference_audio, preset, script_data):
    if not script_data:
        return "Please process a script first.", None, gr.update(visible=False), gr.update(visible=False)
    if not character_name or character_name not in script_data:
        return "Please select a character.", None, gr.update(visible=False), gr.update(visible=False)
    if not reference_audio:
        return "Please upload a reference voice.", None, gr.update(visible=False), gr.update(visible=False)

    try:
        preview_audio, download_zip = convert_character_dialogue(
            character_name, script_data[character_name], reference_audio, preset
        )
        if preview_audio and download_zip:
            return (
                f"Generated {len(script_data[character_name])} lines for {character_name}.",
                preview_audio,
                gr.update(visible=True),
                gr.update(visible=True),
            )
        return "Conversion failed.", None, gr.update(visible=False), gr.update(visible=False)
    except Exception as exc:  # noqa: BLE001
        return f"Error: {exc}", None, gr.update(visible=False), gr.update(visible=False)


def on_process_script(pdf_file):
    summary_text, script_data = process_script_pdf(pdf_file)
    if not script_data:
        return [summary_text, {}] + [gr.update(visible=False)] * 15

    defaults = default_characters(script_data, slots=3)
    choices = list(script_data.keys())
    updates = [
        summary_text,
        script_data,
    ]
    for default in defaults:
        updates.extend(
            [
                gr.update(visible=True, choices=choices, value=default),
                gr.update(visible=True, value=preview_text_for_character(default, script_data)),
                gr.update(visible=True),
                gr.update(visible=True, value=DEFAULT_PRESET),
                gr.update(visible=True, value="Convert lines"),
            ]
        )
    return updates


def on_character_change(character_name, script_data):
    return preview_text_for_character(character_name, script_data)


with gr.Blocks(title="Script Reader (Tortoise TTS)") as app:
    gr.Markdown(
        "Upload a PDF script, select characters, assign reference voices, and generate speech with Tortoise TTS."
    )

    gr.Markdown("Step 1: Upload Script")
    with gr.Row():
        pdf_input = gr.File(file_types=[".pdf"], label="Upload PDF Film Script")
        process_btn = gr.Button("Process Script", variant="primary")

    gr.Markdown("Script Analysis")
    analysis_output = gr.Textbox(value="Upload a PDF to see analysis results...", lines=8, interactive=False)

    gr.Markdown("Step 2: Character Voice Assignment & Conversion")

    def slot_ui(title):
        with gr.Group():
            gr.Markdown(title)
            character_dropdown = gr.Dropdown(label="Character", choices=[], visible=False)
            dialogue_preview = gr.Textbox(label="Dialogue Preview", lines=4, interactive=False, visible=False)
            ref_audio = gr.Audio(
                sources=["upload", "microphone"], type="filepath", label="Reference Voice", visible=False
            )
            preset = gr.Dropdown(
                label="Preset",
                choices=[
                    "high_quality",
                    "standard",
                    "fast",
                    "very_fast",
                    "ultra_fast",
                    "ultra_fast_old",
                ],
                value=DEFAULT_PRESET,
                visible=False,
            )
            convert_btn = gr.Button("Convert lines", variant="primary", visible=False)
            status = gr.Textbox(label="Status", value="Ready", interactive=False)
            preview_audio = gr.Audio(label="Preview", visible=False)
            download = gr.File(label="Download Audio Files", visible=False)
        return (
            character_dropdown,
            dialogue_preview,
            ref_audio,
            preset,
            convert_btn,
            status,
            preview_audio,
            download,
        )

    (
        char1_dropdown,
        char1_dialogue,
        char1_ref_audio,
        char1_preset,
        char1_convert_btn,
        char1_status,
        char1_preview,
        char1_download,
    ) = slot_ui("Slot 1")

    (
        char2_dropdown,
        char2_dialogue,
        char2_ref_audio,
        char2_preset,
        char2_convert_btn,
        char2_status,
        char2_preview,
        char2_download,
    ) = slot_ui("Slot 2")

    (
        char3_dropdown,
        char3_dialogue,
        char3_ref_audio,
        char3_preset,
        char3_convert_btn,
        char3_status,
        char3_preview,
        char3_download,
    ) = slot_ui("Slot 3")

    script_data_state = gr.State({})

    process_btn.click(
        fn=on_process_script,
        inputs=[pdf_input],
        outputs=[
            analysis_output,
            script_data_state,
            char1_dropdown,
            char1_dialogue,
            char1_ref_audio,
            char1_preset,
            char1_convert_btn,
            char2_dropdown,
            char2_dialogue,
            char2_ref_audio,
            char2_preset,
            char2_convert_btn,
            char3_dropdown,
            char3_dialogue,
            char3_ref_audio,
            char3_preset,
            char3_convert_btn,
        ],
    )

    char1_dropdown.change(
        fn=on_character_change,
        inputs=[char1_dropdown, script_data_state],
        outputs=[char1_dialogue],
    )
    char2_dropdown.change(
        fn=on_character_change,
        inputs=[char2_dropdown, script_data_state],
        outputs=[char2_dialogue],
    )
    char3_dropdown.change(
        fn=on_character_change,
        inputs=[char3_dropdown, script_data_state],
        outputs=[char3_dialogue],
    )

    char1_convert_btn.click(
        fn=convert_slot,
        inputs=[char1_dropdown, char1_ref_audio, char1_preset, script_data_state],
        outputs=[char1_status, char1_preview, char1_preview, char1_download],
    )
    char2_convert_btn.click(
        fn=convert_slot,
        inputs=[char2_dropdown, char2_ref_audio, char2_preset, script_data_state],
        outputs=[char2_status, char2_preview, char2_preview, char2_download],
    )
    char3_convert_btn.click(
        fn=convert_slot,
        inputs=[char3_dropdown, char3_ref_audio, char3_preset, script_data_state],
        outputs=[char3_status, char3_preview, char3_preview, char3_download],
    )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=False,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
        ssl_verify=False,
    )
