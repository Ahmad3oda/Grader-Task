import re
import pdfplumber

def pdf_processor(pdf_path):
    questions = {}
    answers = {}

    questions_curr_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.splitlines():
                line = line.strip()

                # Check to match a question.
                q_match = re.match(r'Q(\d+):', line)
                if q_match:
                    q_num = int(q_match.group(1))
                    questions[q_num] = line.partition(':')[2].strip()
                    questions_curr_count = q_num
                    continue
                
                # Check to match an answer, numbered same as the previous q.
                a_match = re.match(r'Answer:', line)
                if a_match and questions_curr_count > 0:
                    answers[questions_curr_count] = line.partition(':')[2].strip()

    return questions, answers
