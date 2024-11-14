def load_and_split_document(file_path):
    with open('products.txt', "r", encoding="utf-8") as file:
        document_text = file.read()
    sections = document_text.split("\n\n")
    return sections

if __name__ == "__main__":
    sections = load_and_split_document("produtos.txt")
    for section in sections:
        print(section, "\n")
