#!/usr/bin/env python3
import hashlib
import json
import platform
import time

import numpy as np
import sentence_transformers
import torch
import transformers
from sentence_transformers import SentenceTransformer

MODEL_ID = "nvidia/llama-nemotron-embed-1b-v2"
REVISION = "113abe4acafa848e77ead9c0623205e511932348"

QUERY = "Which BIOS setting lets Linux access unified memory on Strix Halo?"
DOCUMENTS = [
    (
        "Set UMA Frame Buffer Size to 512MB so Linux can use GPU-accessible "
        "unified memory through GTT."
    ),
    "The weather forecast predicts rain and strong wind tomorrow afternoon.",
]


def main() -> None:
    torch.set_num_threads(16)

    load_started = time.perf_counter()
    model = SentenceTransformer(
        MODEL_ID,
        revision=REVISION,
        trust_remote_code=True,
        device="cpu",
    )
    load_seconds = time.perf_counter() - load_started

    encode_started = time.perf_counter()
    query_embedding = model.encode_query(
        [QUERY], convert_to_numpy=True, normalize_embeddings=True
    )
    document_embeddings = model.encode_document(
        DOCUMENTS, convert_to_numpy=True, normalize_embeddings=True
    )
    encode_seconds = time.perf_counter() - encode_started

    scores = model.similarity(query_embedding, document_embeddings).cpu().numpy()[0]
    vectors = np.concatenate([query_embedding, document_embeddings], axis=0)

    result = {
        "model": MODEL_ID,
        "revision": REVISION,
        "device": "cpu",
        "torch_threads": torch.get_num_threads(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "sentence_transformers": sentence_transformers.__version__,
        "embedding_dimension": int(query_embedding.shape[1]),
        "load_seconds": round(load_seconds, 6),
        "encode_seconds": round(encode_seconds, 6),
        "positive_cosine": round(float(scores[0]), 9),
        "negative_cosine": round(float(scores[1]), 9),
        "margin": round(float(scores[0] - scores[1]), 9),
        "vector_sha256": hashlib.sha256(
            vectors.astype(np.float32).tobytes()
        ).hexdigest(),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
