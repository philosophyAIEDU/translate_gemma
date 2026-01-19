import torch
import streamlit as st
from transformers import AutoModelForImageTextToText, AutoProcessor
from PIL import Image
from typing import List, Dict, Optional
import src.image_processor as img_proc
import src.pdf_processor as pdf_proc

@st.cache_resource
def load_model_cached(model_id: str = "google/translategemma-4b-it"):
    """
    Load the TranslateGemma model and processor.
    Cached to avoid reloading on every interaction.
    """
    print(f"Loading model: {model_id}...")
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForImageTextToText.from_pretrained(
        model_id, 
        device_map="auto",
        torch_dtype=torch.bfloat16
    )
    print("Model loaded successfully.")
    if processor.tokenizer.pad_token is None:
        processor.tokenizer.pad_token = processor.tokenizer.eos_token
    return processor, model

class TranslateGemmaWrapper:
    def __init__(self, model_id: str = "google/translategemma-4b-it"):
        self.model_id = model_id
        # We access the cached model via the global cache function to ensure we get the same instance
        self.processor, self.model = load_model_cached(model_id)

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text using the model."""
        messages = [{
            "role": "user",
            "content": [{
                "type": "text",
                "source_lang_code": source_lang,
                "target_lang_code": target_lang,
                "text": text
            }]
        }]
        
        inputs = self.processor.apply_chat_template(
            messages, 
            tokenize=True, 
            add_generation_prompt=True, 
            return_dict=True, 
            return_tensors="pt"
        ).to(self.model.device)
        
        input_len = len(inputs['input_ids'][0])
        
        with torch.inference_mode():
            generation = self.model.generate(**inputs, do_sample=False, max_new_tokens=1024)
        
        generation = generation[0][input_len:]
        decoded = self.processor.decode(generation, skip_special_tokens=True)
        return decoded

    def translate_image(self, image: Image.Image, source_lang: str, target_lang: str) -> str:
        """Extract and translate text from image."""
        # Resize image
        resized_image = img_proc.resize_image_for_model(image)
        
        messages = [{
            "role": "user",
            "content": [{
                "type": "image",
                "source_lang_code": source_lang,
                "target_lang_code": target_lang,
                # Image is passed separately to apply_chat_template
            }]
        }]
        
        inputs = self.processor.apply_chat_template(
            messages,
            images=[resized_image],
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)
        
        # Explicitly cast pixel_values to bfloat16 if present, as the model expects it
        if 'pixel_values' in inputs:
            inputs['pixel_values'] = inputs['pixel_values'].to(dtype=torch.bfloat16)
        
        with torch.inference_mode():
            generation = self.model.generate(**inputs, do_sample=False, max_new_tokens=1024)
        
        input_len = len(inputs['input_ids'][0])
        generation = generation[0][input_len:]
        decoded = self.processor.decode(generation, skip_special_tokens=True)
        return decoded

    def translate_pdf(self, pdf_file, source_lang: str, target_lang: str) -> List[Dict[str, str]]:
        """
        Translate a PDF by converting pages to images and translating each.
        Returns a list of dicts with 'page' number and 'translated_text'.
        """
        images = pdf_proc.convert_pdf_to_images(pdf_file)
        results = []
        for i, img in enumerate(images):
            # Report progress via callback or just return structure?
            # Since this class is logic, better to return data. 
            # The UI will handle the loop and progress bar if possible, 
            # but wrapping logic here is cleaner.
            # Let's just translate.
            translated_text = self.translate_image(img, source_lang, target_lang)
            results.append({
                "page": i + 1,
                "translated_text": translated_text
            })
        return results
