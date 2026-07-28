import json
import os
import shutil
import ollama

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# Update this path if your dataset location changes
INPUT_FOLDER = r"C:\Users\codin\Downloads\archive (1)\kaggle\train\2. Ekzama"

# Output folder for sorted Teachable Machine classes
OUTPUT_FOLDER = "./teachable_machine_dataset"

# Ollama vision model
MODEL_NAME = "llama3.2-vision"

# System Prompt with SCORAD rules
PROMPT = """
You are an expert dermatological vision classifier. Analyze this skin image for all 6 SCORAD intensity factors.
Grade each factor on a scale from 0 (absent/none) to 3 (severe):
- redness
- swelling
- oozing_crusting
- scratch_marks
- skin_thickening
- dryness

Respond STRICTLY with a valid JSON object only. Do NOT include markdown code blocks, extra text, or explanations.
Example output format:
{"redness": 2, "swelling": 1, "oozing_crusting": 0, "scratch_marks": 1, "skin_thickening": 0, "dryness": 2}
"""


# -----------------------------------------------------------------------------
# Core Sorting Function
# -----------------------------------------------------------------------------
def process_images():
    if not os.path.exists(INPUT_FOLDER):
        print(
            f"❌ Folder '{INPUT_FOLDER}' not found. Please check your path."
        )
        return

    # Filter for image files
    image_files = [
        f
        for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    total_files = len(image_files)

    if total_files == 0:
        print(f"⚠️ No images found in '{INPUT_FOLDER}'.")
        return

    print(
        f"🚀 Starting sorting for {total_files} images using customized SCORAD prompt...\n"
    )

    for index, filename in enumerate(image_files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)

        # ---------------------------------------------------------------------
        # ⏩ SKIP CHECK: See if image was already sorted in a previous run
        # ---------------------------------------------------------------------
        already_processed = False
        for sev in range(4):
            check_path = os.path.join(
                OUTPUT_FOLDER, "redness", f"severity_{sev}", filename
            )
            if os.path.exists(check_path):
                already_processed = True
                break

        if already_processed:
            print(
                f"[{index}/{total_files}] ⏩ Skipping {filename} (Already sorted)"
            )
            continue
        # ---------------------------------------------------------------------

        print(f"[{index}/{total_files}] Processing: {filename}...")

        try:
            # Query local Ollama model
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": PROMPT,
                        "images": [filepath],
                    }
                ],
            )

            # Sanitize and parse JSON response
            raw_text = response["message"]["content"].strip()
            clean_text = (
                raw_text.replace("```json", "").replace("```", "").strip()
            )
            scores = json.loads(clean_text)

            # Copy image into category and severity subfolders
            for factor, severity in scores.items():
                target_folder = os.path.join(
                    OUTPUT_FOLDER, str(factor), f"severity_{severity}"
                )
                os.makedirs(target_folder, exist_ok=True)
                shutil.copy(filepath, os.path.join(target_folder, filename))

            print(f"   ✅ Sorted: {scores}")

        except json.JSONDecodeError:
            print(f"   ⚠️ Invalid JSON format from model for {filename}")
        except Exception as e:
            print(f"   ❌ Error processing {filename}: {e}")

    print(
        f"\n🎉 Done sorting! All images are categorized in: '{os.path.abspath(OUTPUT_FOLDER)}'"
    )


if __name__ == "__main__":
    process_images()