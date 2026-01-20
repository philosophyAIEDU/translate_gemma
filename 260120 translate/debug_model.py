import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import traceback
import sys

def test_image_translation():
    model_id = "google/translategemma-4b-it"
    print(f"Loading model: {model_id}...")
    try:
        processor = AutoProcessor.from_pretrained(model_id)
        if processor.tokenizer.pad_token is None:
            processor.tokenizer.pad_token = processor.tokenizer.eos_token
            
        model = AutoModelForImageTextToText.from_pretrained(
            model_id, 
            device_map="auto",
            torch_dtype=torch.bfloat16
        )
        print("Model loaded.")
        
        # Create a dummy image (red square)
        image = Image.new('RGB', (896, 896), color = 'red')
        
        source_lang = "en"
        target_lang = "es"
        
        messages = [{
            "role": "user",
            "content": [{
                "type": "image",
                "source_lang_code": source_lang,
                "target_lang_code": target_lang,
            }]
        }]
        
        print("Applying chat template for image...")
        inputs = processor.apply_chat_template(
            messages,
            images=[image],
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(model.device)

        # Explicitly cast pixel_values to bfloat16 if present, as the model expects it
        if 'pixel_values' in inputs:
            inputs['pixel_values'] = inputs['pixel_values'].to(dtype=torch.bfloat16)
        
        print("Generating...")
        input_len = len(inputs['input_ids'][0])
        with torch.inference_mode():
            generation = model.generate(**inputs, do_sample=False, max_new_tokens=100)
            
        generation = generation[0][input_len:]
        decoded = processor.decode(generation, skip_special_tokens=True)
        print(f"Image Translation: {decoded}")
        
    except Exception:
        print("An error occurred!")
        traceback.print_exc()

if __name__ == "__main__":
    test_image_translation()
