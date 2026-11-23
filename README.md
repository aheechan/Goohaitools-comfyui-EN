# Goohai Tools for ComfyUI

A practical 70+ node toolkit for batch processing, print layout, mask work and ID-photo production in ComfyUI.

[![GitHub](https://img.shields.io/badge/GitHub-Goohaitools--comfyui--EN-1E90FF?style=flat-square)](https://github.com/aheechan/Goohaitools-comfyui-EN)
[![Bilibili](https://img.shields.io/badge/Bilibili-GoohaiFOTO-FF69B4?style=flat-square&logo=bilibili)](https://space.bilibili.com/1194488958)

> **Unofficial English fork.** This repository is an unofficial English-language fork of [Goohaitools-comfyui](https://github.com/goohai/Goohaitools-comfyui) by **goohai (孤海)**. The original project is released under **GPL-3.0**. This fork is maintained at [aheechan/Goohaitools-comfyui-EN](https://github.com/aheechan/Goohaitools-comfyui-EN). Because GitHub Issues are disabled on the fork, please report bugs and translation problems to the [upstream issue tracker](https://github.com/goohai/Goohaitools-comfyui/issues) (mention that you are using the English fork) or via Bilibili.

## 🎬 Video tutorials

### 👉 [Watch all tutorials on the Bilibili channel](https://space.bilibili.com/1194488958)

[![Bilibili video tutorials](https://img.shields.io/badge/Bilibili-Video%20Tutorials-FF69B4?style=for-the-badge&logo=bilibili)](https://space.bilibili.com/1194488958)

---
## 🧩 RunningHub workflows

### 👉 [Visit my RunningHub profile](https://www.runninghub.cn/user-center/1959241033525714946/webapp?inviteCode=rh-v1557)

<a href="https://vibex.runninghub.cn/p/app-5b97e951de8d47aab61ce3e9731f50a9/?inviteCode=rh-v1557" target="_blank">
  <img src="https://www.runninghub.cn/assets/images/logo.png" alt="RunningHub" height="28" align="middle" />
  <span style="display:inline-block;margin-left:8px;font-size:15px;font-weight:600;color:#1E90FF;vertical-align:middle;">RH Vibex homepage · run AI apps online</span>
</a>

---

Goohai (孤海) is a collection of **70+** practical nodes for ComfyUI. It covers fast folder-based batch loading, DPI-aware saving, mask analysis and compositing, automatic face correction and alignment, automatic straightening and layout of ID cards and ID photos, automatic print layout, frontend JS helpers, colour pickers, numeric expression evaluation, and visual outfit/hairstyle selection for ID photos. It is aimed at ID-photo, portrait and batch-production workflows.

## 🌐 Translation in this fork

Node titles and menu categories are **English in the code itself**, so they show up in English regardless of the interface language.

Input labels, tooltips and node descriptions are provided through [`locales/en/nodeDefs.json`](locales/en/nodeDefs.json) using ComfyUI's built-in custom-node translation system. Set **Settings → Language → English** in ComfyUI to see them; with another interface language you will still get the original Chinese labels.

Dropdown option values are English too. `i18n_options.py` wraps each node's `INPUT_TYPES()` so the combo lists are shown in English, and maps the chosen English value back to the original internal value right before the node runs. [`locales/en/option_values.json`](locales/en/option_values.json) holds the value table.

Compatibility notes:

- Workflows saved by the upstream (Chinese) pack still load: validation accepts both the English labels and the original Chinese values.
- Workflows saved by this fork store the English option values, so passing them back to the upstream pack is not supported without re-selecting the options.
- Node class names, input keys and the workflow format are unchanged.

## 📦 Node overview

All nodes live under the `Goohai Tools` toolbox category (translated from `🔵孤海/`), with a few grouped into functional subcategories such as `Goohai Tools/Image`, `Goohai Custom` and `Goohai/Marriage Registration`.

### Goohai Tools (80)

| Node | Description |
|------|-------------|
| **Goohai Load Batch Images** | Loads images from a folder in single or increment mode, with format filtering, subfolder support and index outputs. |
| **📁Goohai Folder Image Count** | Counts the images in a folder, optionally including subfolders. |
| **Goohai Subfolder Count** | Counts the subfolders inside a folder. |
| **Goohai Folder Index** | Reads a subdirectory by index and returns its path and the total directory count. |
| **Goohai Batch Switch** | Summarises batch settings (batch mode, subfolders, headroom ratio, face ratio) into boolean and float outputs. |
| **Goohai Batch Progress 🐋** | Renders a live progress-bar image from a total count and the current index. |
| **Goohai Auto Create Folder** | Creates the output directory automatically from the input and output path rules. |
| **Goohai Auto Slash Converter** | Converts path separators so folder paths work on Windows, macOS and Linux. |
| **Ignore Extra Groups Goohai** | Toggles the ignore/bypass state of workflow groups that produce extra outputs. |
| **Split String by Type Goohai** | Splits a string at the boundary between two character types (for example Chinese and digits) using a chosen delimiter. |
| **Save Image JPG Goohai** | Saves images as very small JPG files while keeping visual quality; filenames support date, time and batch-index variables. |
| **Goohai Image Save** | Advanced saving for batch work: output path, filename rules, automatic index, DPI, quality and format. |
| **Goohai Preset Size** | Outputs width, height and resolution for common print, ID-photo and social-media sizes, in pixels, centimetres or inches. |
| **Image Scale V2 Goohai** | High-quality scaling with long-edge, short-edge or custom modes, padding and fill options, selectable interpolation and a mask output. |
| **Long/Short Edge** | Outputs the long edge, short edge and their ratio from an image or explicit width and height. |
| **Goohai Image Scale by Pixels** | Scales an image to a target edge length or total pixel count, with crop/pad modes, auto rotation and mask handling. |
| **Image Scale (Range) Goohai** | Constrains image and mask size to a minimum/maximum range using long edge, short edge, width, height or both. |
| **Goohai Image Crop by Ratio** | Crops or pads an image to a target width/height ratio while optionally keeping the original pixel count, width or height. |
| **Goohai Image Crop (Subject Protection)** | Crops to a target size while keeping the protection-mask area fully visible, with fill modes and an extension flag. |
| **Goohai Image Rotate** | Rotates an image by a preset angle (−90°, 0°, 90° or 180°). |
| **Goohai Outpaint Canvas (Target Size)** | Extends the canvas to a target width and height, with per-side ratios, feathering, fill colour and an outpaint mask. |
| **Goohai Outpaint Canvas (Ratio)** | Extends the canvas to a target aspect ratio, with per-side ratios, feathering and an outpaint mask. |
| **Goohai Outpaint Canvas (Direction)** | Extends the canvas by a pixel or percentage amount on each of the four sides, with feathering and an outpaint mask. |
| **Outpaint Canvas (Visual)** | Outpaint canvas with a visual on-node editor for per-side extension and a maximum output edge limit. |
| **Goohai Single-size Layout** | Tiles one photo size onto a paper size at a chosen DPI, with spacing, safe margin, caption and stroke options. |
| **Goohai Multi-size Mixed Layout** | Arranges several photo sizes on one canvas (pixels, centimetres or inches at a set DPI), with rows, rotation, spacing, stroke and caption controls. |
| **Goohai Batch Auto Layout** | Processes a folder of images and lays them out onto sheets automatically, with format filtering, canvas and photo size, spacing, captions and save options. |
| **Goohai ID Card Auto Straighten & Layout** | Straightens front/back ID card images and lays them out on a printable sheet with shadows, auto contrast/tone, watermark and background colour. |
| **Goohai Mask Detect** | Detects whether a mask contains a valid region above a minimum filter value. |
| **Goohai Mask Analysis** | Reports the mask bounding box, size and centre together with optional percentage expansion. |
| **Goohai Mask Ratio Calculate** | Converts mask-relative extension and blur percentages into integer and float pixel amounts. |
| **Goohai Mask Align v2** | Aligns masks to each other or to a reference mask horizontally and vertically, with optional BBOX merging. |
| **Goohai Mask Center Align** | Moves a subject mask so that its centre matches a reference mask. |
| **Goohai Mask Crop** | Crops the image to the mask bounding box with per-side extension and reports out-of-bounds areas. |
| **Goohai Mask Crop V2** | Crops by mask and outputs a seam record so the result can be restored, avoiding sampling pixel offsets. |
| **Goohai Crop Restore** | Pastes a cropped/processed image back at its original coordinates using the seam record, with expansion, feathering and colour restoration. |
| **Goohai Mask Blur & Grow by Ratio** | Grows, blurs and fills a mask by percentage, with an inverted-mask output and a rounded-corner mode. |
| **Goohai Mask Blend Operations** | Combines two masks with add, subtract, intersect, exclude or side-picking modes, BBOX sizing and alignment. |
| **Goohai Head-top Mask** | Expands a mask upward by X/Y amounts to create headroom for outfit or hairstyle changes. |
| **Goohai Mask Corner Rounding Fix** | Removes rounded mask corners, keeping the four edges and restoring the corners. |
| **Goohai Seg Order Filter** | Sorts and filters SEGS or mask batches by area, edge length or position, with an optional discard factor and merged output. |
| **Image & Mask Preview Goohai** | Overlays each mask in a batch on the image with a configurable colour, opacity and index labels. |
| **Goohai Image & Mask Outline** | Draws an outline along a mask edge in pixel or percentage units, outside, centred or inside. |
| **Image/Video Comparer GH** | Compares two images or videos inside the node with a slider, side-by-side or top/bottom split view. |
| **Goohai Remove Background Outside Mask** | Keeps the mask area and removes everything outside it, with mask hole filling, cropping and an optional outline. |
| **Goohai Image Merge (Mask)** | Composites an overlay image onto a background image through a mask, with opacity, mask expansion and blur. |
| **Goohai Image Difference to Mask** | Turns the difference between two images into a mask, with threshold, minimum area, fill, expansion and feathering. |
| **Goohai Image Watermark** | Adds text or image watermarks with size, opacity, position, offset, colour, tiling, angle and spacing controls. |
| **Goohai Image Embed** | Embeds an image into the mask region of a background, for watermark and photo-frame style templates. |
| **Goohai Image Batch Combine** | Combines up to five image inputs or batches into one batch, cropping or padding to a uniform size. |
| **Goohai Auto Split Image** | Splits an image into a grid of tiles, optionally trimming canvas edges and outlines, and saves them as PNG or JPG. |
| **Goohai Image Brightness Compare** | Compares the brightness of one or two images, optionally through masks, and outputs the comparison result. |
| **Goohai Skin Tone Difference** | Compares colour differences between two images, optionally masked, and outputs the difference plus a saturation boolean. |
| **Goohai Dominant Color (Multi-version)** | Extracts the dominant colour of an image as a HEX value, with downsampling and colour-tolerance controls. |
| **Color Converter Goohai** | Converts colours between HEX, RGB and HSL and outputs a string plus a colour control. |
| **Goohai 🎨 Color Picker** | Colour picker with HEX, RGB and HSL output modes. |
| **Goohai Color Picker (Dual)** | Dual colour picker for solid, vertical-gradient or centre-gradient fills, outputting the mode, main and secondary colours. |
| **Goohai Custom Color** | Generates a solid or gradient colour image at a given size, with scaling and grain. |
| **👤 Goohai Auto Face Correction** | Detects facial landmarks with dlib and rotates the image to correct head tilt, with optional edge cropping. |
| **Goohai Face Alignment** | Detects faces with MediaPipe and aligns them eye-to-eye against a reference; compatible with MediaPipe 0.10.21- and 0.10.30+. |
| **Goohai ID Photo Crop** | Detects the face with MediaPipe and crops an ID photo from a face ratio and vertical offset, with face correction, preset sizes, DPI and fill modes. |
| **ID Photo Outfit & Hairstyle Goohai** | Selects an ID-photo outfit and hairstyle style and outputs a ready-to-use prompt. |
| **Goohai ID Photo Simple Prompt** | Builds ID-photo prompts from dropdowns for framing, nationality, gender, body type, hair, outfit, makeup, expression, background and accessories. |
| **Goohai ID Info** | Collects name, gender, ethnicity, birth date, address and ID number, and outputs the personal-info bundle plus a prompt for the card generator. |
| **Goohai ID Card Generator** | Composites a portrait and personal-info bundle onto an ID card template, with an optional transparent background. |
| **Goohai Universal Slider** | Integer/float slider with a dynamic range and a compact custom UI. |
| **Goohai Float Slider** | Float slider with a 0–1 range and a custom UI. |
| **Goohai Float Slider 0-2** | Float slider with a 0–2 range. |
| **Boolean Goohai** | Boolean switch with a custom on-node toggle. |
| **Goohai Effect Switcher** | Switches between effect branches (similarity, micro-beauty, random variants) and can lock the current effect for repeatable results. |
| **Math Operations Goohai** | Evaluates arithmetic expressions with optional `a`–`f` inputs, supporting mixed operations and ternary expressions. |
| **Universal Any Exists (GH)** | Checks whether an Any input is connected and supplies a typed placeholder plus a boolean when it is empty. |
| **Route Blocker** | Passes an Any value through, outputs an empty value, or interrupts the downstream branch depending on the toggle. |
| **Any Switch GH** | Routes one of several Any inputs to a single output. |
| **Display Any GH** | Displays any input (text, image, mask, audio, video or latent) and passes it through unchanged; runs on demand when a downstream node is connected. |
| **Goohai Kontext LoRA Switch** | Outputs the LoRA filename and prompt picked from the two dropdown menus for Kontext workflows. |
| **Goohai Kontext Aspect Ratio** | Outputs width and height for a selected Kontext generation size. |
| **Goohai Kontext Aspect Ratio \| List** | Provides preset Kontext generation aspect ratios and outputs the selected ratio string. |
| **Aspect Ratio & Resolution** | Computes output width and height from a target ratio and mode (fixed edge, megapixels, custom, rounded to a multiple). |
| **Goohai Custom PNG Auto Template** | Automatically fits a portrait image into the transparent region of a PNG template. |

### Goohai Tools/Image (1)

| Node | Description |
|------|-------------|
| **Restore Qwen Image 2.1 GH** | Removes the black canvas added by the fill mode of Qwen Image 2.1 Text Encode GH. |

### Goohai Tools/Prompt (1)

| Node | Description |
|------|-------------|
| **Qwen Image 2.1 Prompt Optimizer** | Rewrites a user prompt for Qwen Image 2.1 text-to-image and image-to-image models, with output-language, transparent-background, seed and model-unload controls plus an optional custom skill. |

### Goohai Tools/Conditioning (1)

| Node | Description |
|------|-------------|
| **Qwen Image 2.1 Text Encode GH** | Qwen Image 2.1 conditioning with stable reference slots and aspect-safe reference sizing; supports crop/fill modes, an optional VAE and a local sampling mask. |

### Goohai Custom (10)

| Node | Description |
|------|-------------|
| **Goohai Custom Kids Sticker Template - Round** | Outputs the round-template image path and size selected by the two dropdown menus. |
| **Goohai Custom Kids Sticker Template - Square** | Outputs the square-template image path and size selected by the two dropdown menus. |
| **Goohai Custom Kids Sticker Template - Long** | Outputs the long-template image path and size selected by the two dropdown menus. |
| **Goohai Custom Kids Sticker Layout - Round** | Arranges kids sticker templates into a printable round sheet and saves the result. |
| **Goohai Custom Kids Sticker Layout - Square** | Arranges kids sticker templates into a printable square sheet and saves the result. |
| **Goohai Custom Kids Sticker Layout - Long** | Arranges kids sticker templates into a printable long sheet and saves the result. |
| **Goohai Extract Code Custom** | Extracts a code identifier from a text string. |
| **Goohai Size from Filename** | Parses width, height, size name and canvas size from a filename, with unit and DPI settings. |
| **Goohai Remove Solid Background v2** | Detects the dominant background colour and removes it, outputting a transparent image and mask. |
| **Goohai ID Photo Layout (A5 Custom)** | Lays out ID photos on A5 sheets using preset mixes (1-inch, 2-inch and combined options) at a chosen DPI. |

### Goohai Custom/Layout (1)

| Node | Description |
|------|-------------|
| **Goohai Custom Layout 18x6** | Lays an image out 18×6 times on a millimetre canvas at a given DPI, with border offsets and an optional logo. |

### Goohai/Marriage Registration (1)

| Node | Description |
|------|-------------|
| **Marriage Registration Outfit Goohai** | Switches the outfit of a marriage registration photo from the bundled template set. |

### GoohaiTools/Video (1)

| Node | Description |
|------|-------------|
| **Save Video** | Merges an image sequence and audio into an H.264 MP4 (speed-optimised), with frame rate, quality and a save toggle. |

### 🔵Goohai/Utilities (1)

| Node | Description |
|------|-------------|
| **Common Colors 🔵Goohai** | Picks a preset colour or a custom colour and outputs a hex colour string such as `#FFFFFF`. |

### image (1)

| Node | Description |
|------|-------------|
| **Load Image Goohai** | Single-image loader with alpha-channel preservation, crop info and file-name output. |

---

## ✨ Feature highlights

### 📁 Folder batch processing
- Load an entire folder of images at once, with automatic indexing and counting
- Pair it with **Goohai Batch Progress 🐋** to see the current position in the run
- Creates output folders automatically and fixes path slashes across platforms

### 💾 Smart saving
- **JPG with a specified DPI** (300 dpi is typical for print and ID photos)
- The advanced save node supports custom compression, metadata and naming rules

### 🎨 Automatic layout
- Three layout modes: **single size, mixed sizes, batch automatic**
- Fits A4, A5 and 6-inch paper and tiles photos to print specifications
- ID cards are straightened automatically and composed onto a standard template

### 👤 Face and ID-photo pipeline
- Face detection → face alignment → ID-photo crop → outfit/hairstyle replacement → automatic layout, end to end
- Dozens of built-in outfit templates (women's and men's suits, vests, shirts, casual tops, marriage registration outfits and more — see `image/ID_Photo/`)
- Auto face correction, skin-tone difference and head-top mask expansion keep outfit and hairstyle changes natural

### 🎭 Complete mask toolkit
- Detect → analyse → grow → blur → align → crop → restore → blend, covering most mask workflows
- Advanced options include subject-protected cropping, background removal outside a mask and difference-to-mask

### 🌈 Colour and colour picking
- Colour pickers, preset palettes, colour-space conversion and dominant-colour extraction for palette matching and colour-cast correction

### 🖼️ Image/video comparison
- Slider comparison, automatic side-by-side, left/right side-by-side and top/bottom side-by-side
- Image and video previews, with video play/pause and progress control
- Side-by-side mode supports Alt+wheel zoom and Alt+drag panning inside the frame; videos support full-screen comparison
- Batch inputs let you compare the first 10 images individually
- Previews are taken directly from the input files, so no extra files are written to the temp directory

---

## ⚙️ Installation

### Method 1: Git clone (recommended, easier to update later)

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/aheechan/Goohaitools-comfyui-EN.git
cd Goohaitools-comfyui-EN
pip install -r requirements.txt
```

Then restart ComfyUI.

### Method 2: Manual download

Download the ZIP of this repository, extract it into `ComfyUI/custom_nodes/` and make sure the folder is named `Goohaitools-comfyui-EN`, then run `pip install -r requirements.txt` inside that folder and restart ComfyUI.

Main dependencies in `requirements.txt`:

- `opencv-python`, `scipy`, `scikit-image`, `matplotlib` — core image processing
- `mediapipe>=0.10.20` — face and landmark detection
- `dlib-bin>=19.24.6` — 5-point facial landmark model; the repository already includes `shape_predictor_5_face_landmarks.dat` (the line is commented out in the shipped `requirements.txt`, so uncomment it if `import dlib` fails)

If `pip` is slow, note that `requirements.txt` comes preconfigured with the Tsinghua mirror (`-i https://pypi.tuna.tsinghua.edu.cn/simple`). Users outside China can remove that `-i` option to use their default index.

## 🔧 Frontend extensions

The pack ships several frontend widget enhancements under `web/js/`:

- `BOOLEAN.js` — boolean toggle widget
- `GoohaiNote.js` — node notes and sticky notes
- `goohai_color_widget.js` — colour picker widget
- `goohai_universal_slider.js` — universal slider interaction
- `gh_image_video_comparer.js` — image/video comparison preview
- `id_photo_clothing.js` / `marry.js` — outfit pickers for ID photos and marriage registration photos

With these enabled, nodes such as the colour pickers, the universal slider and the outfit selectors get a friendlier interactive UI.

## 📝 License

This project is released under the **GNU General Public License v3.0 (GPL-3.0)**. The original work is copyright its author, **goohai (孤海)**; see [LICENSE](LICENSE) for the full text. Stars, forks and pull requests are welcome.

💬 Feedback and contact
📺 Bilibili (video tutorials / workflow demos): [Goohai on Bilibili](https://space.bilibili.com/1194488958)
🐛 GitHub Issues: [upstream issue tracker](https://github.com/goohai/Goohaitools-comfyui/issues) (Issues are disabled on this fork)
💡 If you have questions, want a new feature or a node suggestion, open an issue on GitHub or send a message on Bilibili. If the toolkit saves you time, a Star on the repository is always appreciated ⭐.
