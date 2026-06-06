import docx

def extract_docx_text(uploaded_file):

    doc = docx.Document(uploaded_file)

    full_text = []

    for para in doc.paragraphs:
        full_text.append(para.text)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text.append(cell.text)

    return "\n".join(full_text)
