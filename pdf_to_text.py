import fitz  # pip install pymupdf

def get_text(pdf_path):
    paragraphs = []

    # open the file
    with fitz.open(pdf_path) as file:
        # iterate through file
        for n in range(file.page_count):
            page = file[n]
            text = page.get_text("text")

            # split the text by newlines to get paragraphs
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            paragraphs.extend(paragraphs)
    return paragraphs

if __name__ == "__main__":
    # test run
    pdf_path = 'file_path.pdf'  # replace with your file path
    paragraphs = get_text(pdf_path)

    # show data, manipulate it, whatever
    # for i, paragraph in enumerate(paragraphs, 1):
    #     print(f"Paragraph {i}:\n{paragraph}\n")