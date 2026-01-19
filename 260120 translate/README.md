# TranslateGemma Educator App

This is a Streamlit-based web application designed for educators, powered by Google's **TranslateGemma** model. It provides robust translation capabilities for text, images, and PDF documents, along with features specific to educational workflows like glossary management and history tracking.

## Features

- **Text Translation**: Translate text between 55+ languages.
- **Image Translation**: Upload images and get translated text extraction using TranslateGemma's multimodal capabilities.
- **PDF Translation**: Upload PDFs, convert pages to images, and translate them.
- **Glossary Management**: Maintain a consistent terminology database.
- **History Tracking**: Automatically save translation history for review and export.

## Requirements

- Python 3.10+
- CUDA-enabled GPU (Highly Recommended for 4B model)
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) (Required for PDF processing on Windows)

## Installation

1.  **Clone the repository** (if applicable).
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Pytorch with CUDA support is recommended. You might need to install it separately via `pip install torch --index-url https://download.pytorch.org/whl/cu118` or similar.*

3.  **Install Poppler**:
    - Download the latest binary from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/).
    - Extract the zip file.
    - Add the `bin` folder to your system `PATH` environment variable.

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your default web browser (usually at `http://localhost:8501`).

## Model

This app defaults to `google/translategemma-4b-it`. The first run will download the model (approx 8GB+ depending on format), so ensure you have a stable internet connection and sufficient disk space.

## Structure

- `app.py`: Main entry point.
- `src/`: Core logic (Translator wrapper, processors).
- `components/`: UI components for each tab.
- `data/`: Storage for languages, history, and glossary.
