
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(pages):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for page in pages:

        page_text = page["content"]
        page_number = page["page_number"]

        split_texts = text_splitter.split_text(page_text)

        for index, chunk in enumerate(split_texts):

            chunks.append({
                "chunk_id": len(chunks) + 1,
                "page_number": page_number,
                "chunk_index": index + 1,
                "content": chunk
            })

    return chunks
