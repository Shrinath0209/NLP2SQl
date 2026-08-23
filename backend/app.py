"""
FastAPI Application — NL2SQL System
Exposes /query endpoint: takes natural language → returns SQL + results
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from backend.nlp.preprocessor import NLPreprocessor
from backend.nlp.embeddings import EmbeddingMatcher
from backend.sql_generator.generator import SQLGenerator
from backend.database.schema import init_db
from backend.database.executor import SQLExecutor

app = FastAPI(title="NL2SQL — Transformer-Based Query Generation")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# Init components
init_db()
preprocessor = NLPreprocessor()
matcher      = EmbeddingMatcher()
generator    = SQLGenerator()
executor     = SQLExecutor()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")

@app.post("/query")
def process_query(req: QueryRequest):
    preprocessed = preprocessor.preprocess(req.query)
    schema_match = matcher.get_schema_match(req.query)
    sql_result   = generator.generate(req.query, preprocessed, schema_match)
    execution    = executor.execute(sql_result["sql"])

    return {
        "query"        : req.query,
        "preprocessed" : preprocessed,
        "schema_match" : schema_match,
        "generated_sql": sql_result["sql"],
        "explanation"  : sql_result["explanation"],
        "execution"    : execution,
    }

@app.get("/schema")
def get_schema():
    from backend.utils.schema_meta import SCHEMA_META
    return SCHEMA_META

@app.get("/health")
def health():
    model_path   = os.path.abspath("models/intent_classifier.pt")
    neural_ready = os.path.exists(model_path)
    return {
        "status"         : "ok",
        "encoder_model"  : "all-MiniLM-L6-v2",
        "intent_model"   : "intent_classifier.pt (fine-tuned)" if neural_ready else "rule-based fallback",
        "intent_source"  : "neural" if neural_ready else "rules",
        "neural_ready"   : neural_ready,
        "dataset"        : "b-mc2/sql-create-context (78K pairs)",
        "val_accuracy"   : "90%" if neural_ready else "N/A",
        "database"       : "academic.db · SQLite",
    }

@app.get("/model-info")
def model_info():
    return {
        "encoder"        : "all-MiniLM-L6-v2",
        "encoder_dim"    : 384,
        "classifier_arch": "Linear(384→128) → ReLU → Linear(128→7)",
        "trainable_params": "50,183",
        "frozen_params"  : "22,713,216",
        "intent_classes" : ["COUNT", "AVERAGE", "TOP_N", "BOTTOM_N", "FILTER_LT", "FILTER_GT", "SELECT"],
        "training_data"  : "b-mc2/sql-create-context (HuggingFace, 78K NL→SQL pairs)",
        "domain_boost"   : "56 academic examples × 10",
        "epochs"         : 40,
        "batch_size"     : 32,
        "optimizer"      : "Adam (lr=2e-4)",
        "loss"           : "CrossEntropyLoss",
        "val_accuracy"   : "90%",
        "device_trained" : "CUDA (Google Colab T4)",
    }
