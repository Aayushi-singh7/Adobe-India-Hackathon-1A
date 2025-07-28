import fitz  # PyMuPDF
import os
import json
from collections import Counter

# Configuration
USE_BOLD = True  # Set to False to disable bold detection
INPUT_DIR = "input"
OUTPUT_DIR = "output"

def is_bold(font_name: str) -> bool:
    return any(kw in font_name.lower() for kw in ["bold", "black", "demi"])

def extract_fonts_and_sizes(pdf_path):
    font_counts = Counter()
    font_styles = {}
    with fitz.open(pdf_path) as doc:
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                for line in b.get("lines", []):
                    for span in line["spans"]:
                        key = (span["size"], span["font"])
                        font_counts[key] += 1
                        font_styles[span["text"].strip()] = (span["size"], span["font"])
    return font_counts, font_styles

def classify_headings(font_counts):
    sorted_fonts = sorted(font_counts.items(), key=lambda x: (-x[0][0], -x[1]))
    size_rank = {}
    rank = 1
    for (size, font), _ in sorted_fonts:
        if size not in size_rank:
            size_rank[size] = f"H{rank}" if rank <= 3 else None
            rank += 1
    return size_rank

def extract_outline(pdf_path, size_rank):
    outline = []
    title = ""
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                for line in b.get("lines", []):
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text or len(text) < 2:
                            continue
                        size = span["size"]
                        font = span["font"]

                        # Font-based heading level
                        level = size_rank.get(size, None)
                        if not level:
                            continue

                        # Optional bold check
                        if USE_BOLD and not is_bold(font):
                            continue

                        # Assign Title if H1 and no title yet
                        if not title and level == "H1":
                            title = text

                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })

    return title, outline

def process_pdf(file_path, output_path):
    font_counts, _ = extract_fonts_and_sizes(file_path)
    size_rank = classify_headings(font_counts)
    title, outline = extract_outline(file_path, size_rank)

    output_json = {
        "title": title or "Untitled",
        "outline": outline
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            print(f"Processing: {filename}")
            process_pdf(input_path, output_path)
    print("✅ Processing complete. Check the output/ folder.")

if __name__ == "__main__":
    main()
