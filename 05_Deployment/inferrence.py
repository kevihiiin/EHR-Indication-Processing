#!/usr/bin/env python3
"""Python Script to Classify Free Text Indications
This tool will perform the following actions given a collection of indications
1. Convert the indications to lowercase and create a de-duplicated copy
2. Perform classification (inference)
3. Expand back to the original size and order
"""

import pandas as pd
import torch

from pathlib import Path
from tqdm.auto import tqdm

# Transformers (Huggingface) and PyTorch Imports
from datasets import Dataset
from transformers import AutoTokenizer, pipeline, AutoModelForSequenceClassification
from transformers.pipelines.pt_utils import KeyDataset

# --- Configuration ---
base_data_path = Path("/home/kevin/DPhil/Projects/EHR-Indication-Processing/98_Testing")  # Path to the model & data
saved_model_name = "Bio_ClinicalBERT_4346.pth"  # Saved model name
model_hf_id = "emilyalsentzer/Bio_ClinicalBERT"  # Currently required for the correct tokenizer
cuda_device = "cpu"  # Change to "0" for the first GPU, or "cpu" for CPU

batch_size = 8  # Batch size for inference, we used 8 for the training of this model, keep it at 8
pred_threshold = 0.5  # Threshold for binarising the predictions, we choose 0.5 for training, can be changed

# --- Import Data ---
# Import the data
inference_input_df = pd.read_csv(base_data_path / "test_data_2000.csv", dtype={"Indication": str}) \
    .dropna()
# Pick the column of interest
inference_indication_cased = inference_input_df.Indication

# --- Preprocess Data ---
# Convert to lower case and make unique
inference_df = pd.DataFrame({"Input_String": inference_indication_cased.str.lower().drop_duplicates()})
# Create a Huggingface Dataset
inference_dataset = Dataset.from_pandas(inference_df)
print(f"Inference dataset size: {len(inference_dataset)} unique entries from {len(inference_indication_cased)} total")

# --- Loading Model & Inference ---
# Load the model and tokeniser
model = AutoModelForSequenceClassification.from_pretrained(base_data_path / saved_model_name)
tokenizer = AutoTokenizer.from_pretrained(model_hf_id)
# Set up the pipeline
inference_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None, device=cuda_device)

# Classify the infections, runs in batches
pred_output = []
for out in tqdm(
        inference_pipeline(
            KeyDataset(inference_dataset, "Input_String"),
            batch_size=batch_size)
):
    pred_output.append(out)

# --- Postprocess Data ---
# Convert batched predictions into one Pandas DataFrame again
row_dicts = []
for prediction in pred_output:
    row_dicts.append({
        x["label"]: x["score"] for x in prediction
    })

inference_classified_unique_probs = pd.DataFrame.from_dict(row_dicts)
inference_classified_unique_probs.index = inference_df.Input_String

# Expand to original size and labels
inference_classified_probs = inference_indication_cased.to_frame() \
    .merge(inference_classified_unique_probs,
           left_on="Indication",
           right_index=True,
           how="left",
           validate="many_to_one")

inference_classified_probs = inference_classified_probs.set_index("Indication")

# Binarise the output
inference_classified_binarised = (inference_classified_probs > pred_threshold) * 1

print(inference_classified_binarised)
