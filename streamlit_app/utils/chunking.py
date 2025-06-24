import re

# Simple markdown chunking for demo; can be improved for production

def chunk_job_post(text, max_length=350):
    # Split by paragraphs, then merge to max_length
    paras = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    chunks = []
    current = ""
    for para in paras:
        if len(current) + len(para) < max_length:
            current += ("\n\n" if current else "") + para
        else:
            if current:
                chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return chunks
