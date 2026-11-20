---
title: Magic Hour AI Image and Video Generator
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: static
app_file: index.html
pinned: false
license: mit
short_description: Generate AI images and videos with the Magic Hour API
---

# Magic Hour AI Image and Video Generator

Generate images and text-to-video clips with the [Magic Hour API](https://magichour.ai/api), using your own API key.

The page is a single `index.html` that uses [`@magichourhq/browser-client`](https://www.npmjs.com/package/@magichourhq/browser-client). Your key goes straight from your browser to `api.magichour.ai`; the page doesn't store it or send it anywhere else. Generations use credits from your Magic Hour account.

Source: [magichourhq/magic-hour-huggingface-space](https://github.com/magichourhq/magic-hour-huggingface-space). Every push to `main` deploys to this Space.
