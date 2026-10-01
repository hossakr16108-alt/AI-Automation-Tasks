import os
from pypdf import PdfReader

def extract_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "linkedin.pdf")
    output_path = os.path.join(base_dir, "summary.txt")

    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return

    reader = PdfReader(pdf_path)
    text_content = ""

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text_content += f"\n--- Page {i+1} ---\n" + page_text

    if len(text_content.strip()) < 50:
        print("⚠️ Warning: extracted text is empty or too short. Check the PDF has a real text layer.")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text_content)

    print(f"✅ Success: Extracted {len(reader.pages)} pages ({len(text_content)} chars) into {output_path}")

if __name__ == "__main__":
    extract_pdf() 