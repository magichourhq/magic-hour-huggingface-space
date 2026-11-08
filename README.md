---
title: Magic Hour AI Image and Video Generator
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: mit
short_description: Generate AI images and videos with the Magic Hour API
---

# Magic Hour AI Image & Video Generator

A bring-your-own-key Gradio Space for generating images and text-to-video results with the [Magic Hour API](https://magichour.ai/api).

The app uses the official [`magic_hour`](https://pypi.org/project/magic-hour/) Python SDK. API keys are passed directly to the SDK for the active request and are not persisted by the app.

## Choose the right video workflow

| What you have | Which route to use |
| --- | --- |
| A description and no starting image | Use the **Text to video** tab in this app. |
| One product photo, illustration, or other starting image | Use the [Image-to-Video API](https://docs.magichour.ai/api-reference/video-projects/image-to-video) with `assets.image_file_path`. |
| Both a starting image and a specific closing composition | Use the same Image-to-Video endpoint with `assets.image_file_path` and `assets.end_image_file_path`. Check the selected model and resolution before submitting. |

The Gradio app in this repository generates still images and text-to-video clips. The two image-to-video workflows in the table use the API directly.

### Start with one frame or supply both

For a simple camera move around a product photo, send the photo as the first frame and describe the motion in `style.prompt`. For a reveal that needs to finish with the product centered in a specific layout, also supply an end image. The final clip still needs a visual check for label changes, shape changes, and framing.

Upload the images with the [asset upload endpoint](https://docs.magichour.ai/api-reference/files/generate-asset-upload-urls), then use the returned file paths. For example, this is a five-second, 720p LTX 2.5 request body for `POST /v1/image-to-video`.

```json
{
  "model": "ltx-2.5",
  "resolution": "720p",
  "end_seconds": 5,
  "audio": false,
  "style": {
    "prompt": "Reveal the product slowly and settle on the final composition."
  },
  "assets": {
    "image_file_path": "api-assets/id/start.png",
    "end_image_file_path": "api-assets/id/end.png"
  }
}
```

For a first-frame-only run, omit `end_image_file_path`. Replace the sample paths with your own and use media you have permission to process. Generation consumes credits from your Magic Hour account.

Save the project ID from the create response. Use [Get Video Details](https://docs.magichour.ai/api-reference/video-projects/get-video-details) to check the status and retrieve the output from `downloads` once it is `complete`. Download and play the clip before passing it to the next step.
