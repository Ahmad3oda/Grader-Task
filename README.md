# Grader Task

A simple AI-powered grading service that:

1. Accepts a PDF file
2. Extracts questions and answers from the PDF
3. Sends each question/answer pair to an OpenAI model
4. Returns structured grading results as JSON

---

## Features

- PDF parsing using `pdfplumber`
- Question/answer extraction from simple text-based PDFs
- AI grading using OpenAI API
- JSON response with:
  - score
  - max score
  - feedback
  - missing points
  - confidence
- FastAPI endpoint for uploading PDFs

---

## Assumptions

This project assumes the PDF text follows a simple format like:

```text
Q1: What insect has 6 legs?
Answer: All insects have six legs.

Q2: What fruit is shown?
Answer: This is an apple.

```

Each question should start with `q<number>:` and each answer should start with `answer:`.

This solution is designed for **text-based PDFs**, not scanned image PDFs.

---

## Project Structure

```text
utils/
  grader.py
  pdf_processor.py
models/
  GraderResponse.py
test_pdfs/
  question.pdf
main.py
reqs.txt
README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone `https://github.com/Ahmad3oda/Grader-Task`
cd Grader-Task
```

### 2. Create and activate a virtual environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r reqs.txt
```

### 4. Set environment variable

#### Windows PowerShell
```powershell
$env:API_KEY="your_api_key_here"
```

#### macOS / Linux
```bash
export API_KEY="your_api_key_here"
```

---

## Running the API

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

Use the `/grade` endpoint to upload a PDF.

---

## API Endpoint

### `POST /grade-pdf`

Uploads a PDF, extracts questions and answers, grades each answer, and returns the results.

#### Example response

```json
{
  "results": {
    "score": 1,
    "max_score": 1,
    "feedback": "Correct answer.",
    "missing_points": [],
    "confidence": 0.98
  }
}
```

---

## Design Notes

- I kept the implementation simple and focused on correctness.
- `pdfplumber` is used to extract lines from the PDF.
- Regex is used to map `Q<number>:` lines to questions and `Answer:` lines to answers.
- Each extracted question/answer pair is graded independently using the OpenAI API.
- The model is instructed to return strict JSON only.
- The response is returned through a FastAPI endpoint for easy testing.

---

## Limitations

- Works best with clean, text-based PDFs
- Does not currently handle OCR for scanned PDFs
- Multi-line answers/questions may require additional parsing logic
