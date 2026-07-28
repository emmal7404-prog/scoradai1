import json
import os
import shutil
import ollama

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# Path to your extracted Kaggle dataset
INPUT_FOLDER = r"C:\Users\codin\Downloads\archive (1)\kaggle\train\2. Ekzama"

# Target folder where sorted images will be copied
OUTPUT_FOLDER = "./teachable_machine_dataset"

# AI Model settings (llama3.2-vision or moondream)
MODEL_NAME = "llama3.2-vision"

# Prompt requesting strict numerical grading for SCORAD factors
PROMPT = """
You are grading SCORAD erythema. Look ONLY at redness. Ignore: - oozing - crusting - scratching - dryness - scaling - lichenification - skin thickness - background - lighting - normal skin pigmentation Score: 0 = no redness 1 = mild faint redness 2 = moderate obvious redness 3 = severe intense redness Return only: 0, 1, 2, or 3.

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

    # Find all image files
    image_files = [
        f
        for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    total_files = len(image_files)

    if total_files == 0:
        print(f"⚠️ No PNG/JPG images found in '{INPUT_FOLDER}'.")
        return

    print(f"🚀 Starting dataset sorting for {total_files} images using Ollama...\n")

    for index, filename in enumerate(image_files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        print(f"[{index}/{total_files}] Processing: {filename}...")

        try:
            # Query local Ollama vision model
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

            # Clean and parse JSON response
            raw_text = response["message"]["content"].strip()
            clean_text = (
                raw_text.replace("```json", "").replace("```", "").strip()
            )
            scores = json.loads(clean_text)

            # Copy image into factor and severity subfolders
            for factor, severity in scores.items():
                target_folder = os.path.join(
                    OUTPUT_FOLDER, str(factor), f"severity_{severity}"
                )
                os.makedirs(target_folder, exist_ok=True)
                shutil.copy(filepath, os.path.join(target_folder, filename))

            print(f"   ✅ Sorted: {scores}")

        except json.JSONDecodeError:
            print(f"   ⚠️ Invalid JSON response for {filename}")
        except Exception as e:
            print(f"   ❌ Error processing {filename}: {e}")

    print(
        f"\n🎉 Finished! Sorted images are in: '{os.path.abspath(OUTPUT_FOLDER)}'"
    )


if __name__ == "__main__":
    process_images()