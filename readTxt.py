def load_and_split_document(file_path):
    with open(r'convinceai-LLM\products.txt', "r", encoding="utf-8") as file:
        document_text = file.read()
    sections = document_text.split("\n\n")
    return sections

if __name__ == "__main__":
    sections = load_and_split_document(r"convinceai-LLM\products.txt")
    for section in sections:
        print(section, "\n")
