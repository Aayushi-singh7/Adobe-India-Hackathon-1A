# Adobe Hackathon 2025 - Round 1A  
## 🧠 PDF Heading Structure Extractor

This project extracts a structured outline (Title, H1, H2, H3) from a given PDF using font size, font style, and boldness cues. The output is a clean, hierarchical JSON file as per Adobe's expected format.

---

## 🛠 Features

- Accepts any `.pdf` file (up to 50 pages)
- Outputs headings with:
  - Level (H1/H2/H3)
  - Text content
  - Page number
- Uses:
  - Font size ranking
  - Optional boldness detection
  - Font style variation for context
- Modular design for reuse in Round 1B

---

## 📁 Folder Structure

.
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
├── input/
│ └── sample.pdf
└── output/
└── sample.json

yaml
Copy
Edit

---

## 🚀 How to Build & Run (Expected Execution)

### Step 1: Build Docker Image

```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
Step 2: Run the Container
bash
Copy
Edit
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolutionname:somerandomidentifier
📦 Output Format
json
Copy
Edit
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
⚙️ Config
In main.py:

Set USE_BOLD = True to only include bold headings.

You can disable bold-only detection for broader heading identification.

📌 Constraints Followed
Constraint	Status
≤ 50 pages	✅
Model size ≤ 200MB	✅ (no model used)
CPU-only	✅
No internet	✅
Execution ≤10s	✅ Fast PyMuPDF parsing

🏁 Scoring Criteria Addressed
Criterion	Covered
Heading detection	✅
Font size-based accuracy	✅
Bold/style handling	✅
Multilingual (optional)	✅