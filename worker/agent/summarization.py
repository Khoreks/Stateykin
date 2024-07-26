from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


def get_len(text):
    return len(text.split())


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
    length_function=get_len,
    is_separator_regex=False,
)


def combine_chunks(chunks, max_words=settings.chunk_max_words):
    combined_chunks = []
    current_chunk = ""

    for chunk in chunks:
        words_in_chunk = chunk.split()
        current_chunk_words = current_chunk.split()

        if len(current_chunk_words) + len(words_in_chunk) <= max_words:
            if current_chunk:
                current_chunk += " " + chunk
            else:
                current_chunk = chunk
        else:
            if current_chunk:
                combined_chunks.append(current_chunk)
            current_chunk = chunk

            if len(words_in_chunk) > max_words:
                split_chunks = text_splitter.create_documents([chunk])
                combined_chunks.extend(split_chunks)
                current_chunk = ""
            else:
                current_chunk = chunk

    if current_chunk:
        combined_chunks.append(current_chunk)

    return combined_chunks


def query_summarization(input_dict: dict, web_pages: list, chain):
    web_pages = [eval(p) if isinstance(p, str) else p for p in web_pages]
    num_iters = 0
    chunks_batch = []
    for page in web_pages:
        page_chunks = page.get("paragraphs", None)
        if page_chunks:
            chunks = [" ".join(chunk.split()) for chunk in page_chunks if len(chunk.split()) > 3]
            if len(chunks) == 0:
                continue
            chunks_batch.extend(chunks)
    while (len(chunks_batch) > 1) | (num_iters == 4):
        num_iters += 1
        chunks_batch = combine_chunks(chunks_batch)
        batch = []
        for chunk in chunks_batch:
            input_dict["page"] = chunk
            batch.append(input_dict)
        chunks_batch = chain.batch(batch)
    return " ".join(chunks_batch)
