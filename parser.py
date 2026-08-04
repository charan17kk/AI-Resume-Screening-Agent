import fitz
import os


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF resume.
    """

    text = ""

    try:
        document = fitz.open(pdf_path)

        for page in document:
            text += page.get_text()

        document.close()

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return text


def load_all_resumes(folder_path):
    """
    Reads every PDF inside resumes folder.
    Returns dictionary.
    """

    resumes = {}

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            full_path = os.path.join(folder_path, file)

            resumes[file] = extract_text_from_pdf(full_path)

    return resumes


if __name__ == "__main__":

    resumes = load_all_resumes("resumes")

    print(f"\nFound {len(resumes)} resumes.\n")

    for name, text in resumes.items():

        print("=" * 80)
        print(name)
        print("=" * 80)

        print(text[:700])

        print("\n")