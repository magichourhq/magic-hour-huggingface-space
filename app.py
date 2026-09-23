import tempfile
from pathlib import Path

import gradio as gr
from magic_hour import Client


def _key(value: str) -> str:
    value = (value or "").strip()
    if not value:
        raise gr.Error("Enter a Magic Hour API key.")
    return value


def generate_image(api_key: str, prompt: str, aspect_ratio: str, resolution: str):
    if not (prompt or "").strip():
        raise gr.Error("Enter an image prompt.")

    output_dir = tempfile.mkdtemp(prefix="magic-hour-image-")
    try:
        result = Client(token=_key(api_key)).v1.ai_image_generator.generate(
            image_count=1,
            style={"prompt": prompt.strip(), "tool": "general"},
            aspect_ratio=aspect_ratio,
            model="default",
            name="Hugging Face Space image",
            resolution=resolution,
            wait_for_completion=True,
            download_outputs=True,
            download_directory=output_dir,
        )
    except Exception as exc:
        raise gr.Error(f"Magic Hour request failed: {exc}") from exc

    paths = [str(path) for path in (result.downloaded_paths or [])]
    if not paths:
        raise gr.Error(f"Project {result.id} finished without a downloadable image.")
    return paths[0], f"Project `{result.id}` — {result.status}"


def generate_video(
    api_key: str,
    prompt: str,
    duration: int,
    aspect_ratio: str,
    resolution: str,
    include_audio: bool,
):
    if not (prompt or "").strip():
        raise gr.Error("Enter a video prompt.")

    output_dir = tempfile.mkdtemp(prefix="magic-hour-video-")
    try:
        result = Client(token=_key(api_key)).v1.text_to_video.generate(
            end_seconds=float(duration),
            style={"prompt": prompt.strip()},
            aspect_ratio=aspect_ratio,
            audio=include_audio,
            model="default",
            name="Hugging Face Space video",
            resolution=resolution,
            wait_for_completion=True,
            download_outputs=True,
            download_directory=output_dir,
        )
    except Exception as exc:
        raise gr.Error(f"Magic Hour request failed: {exc}") from exc

    paths = [str(path) for path in (result.downloaded_paths or [])]
    if not paths:
        raise gr.Error(f"Project {result.id} finished without a downloadable video.")
    return paths[0], f"Project `{result.id}` — {result.status}"


with gr.Blocks(title="Magic Hour AI Image & Video Generator") as demo:
    gr.Markdown(
        """
# Magic Hour AI Image & Video Generator

Generate media with the [Magic Hour API](https://magichour.ai/api). Your API key is used only for this request and is not stored by this Space. Generations consume credits from your Magic Hour API account.
"""
    )
    api_key = gr.Textbox(
        label="Magic Hour API key",
        type="password",
        placeholder="Create a key at magichour.ai/developer",
    )

    with gr.Tab("Image"):
        image_prompt = gr.Textbox(
            label="Prompt",
            lines=3,
            placeholder="A glass greenhouse floating above a cloud city at sunrise",
        )
        with gr.Row():
            image_aspect = gr.Dropdown(
                ["1:1", "16:9", "9:16", "4:3", "3:4"], value="1:1", label="Aspect ratio"
            )
            image_resolution = gr.Dropdown(
                ["640px", "1k", "2k"], value="1k", label="Resolution"
            )
        image_button = gr.Button("Generate image", variant="primary")
        image_output = gr.Image(label="Generated image")
        image_status = gr.Markdown()
        image_button.click(
            generate_image,
            [api_key, image_prompt, image_aspect, image_resolution],
            [image_output, image_status],
        )

    with gr.Tab("Text to video"):
        video_prompt = gr.Textbox(
            label="Prompt",
            lines=3,
            placeholder="A paper dragon unfolds and flies across an illustrator's desk",
        )
        with gr.Row():
            duration = gr.Slider(1, 10, value=5, step=1, label="Duration (seconds)")
            video_aspect = gr.Dropdown(
                ["16:9", "9:16", "1:1"], value="16:9", label="Aspect ratio"
            )
            video_resolution = gr.Dropdown(
                ["480p", "720p"], value="480p", label="Resolution"
            )
        include_audio = gr.Checkbox(value=False, label="Include audio when supported")
        video_button = gr.Button("Generate video", variant="primary")
        video_output = gr.Video(label="Generated video")
        video_status = gr.Markdown()
        video_button.click(
            generate_video,
            [api_key, video_prompt, duration, video_aspect, video_resolution, include_audio],
            [video_output, video_status],
        )

    gr.Markdown(
        "[API documentation](https://docs.magichour.ai) · [Pricing](https://magichour.ai/api) · [Get an API key](https://magichour.ai/developer)"
    )


demo.queue(default_concurrency_limit=2).launch()
