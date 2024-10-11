#!/usr/bin/env python3
"""Python Script to Classify Free Text Indications
This tool will perform the following actions given a collection of indications
1. Convert the indications to lowercase and create a de-duplicated copy
2. Perform classification (inference)
3. Expand back to the original size and order

Usage:
    python inferrence.py --input_file <path_to_input_file> --output_path <path_to_output_dir> --model_path <path_to_model_dir>

"""

import pandas as pd
import argparse
from pathlib import Path
from tqdm.auto import tqdm

# Transformers (Huggingface) and PyTorch Imports
from datasets import Dataset
from transformers import AutoTokenizer, pipeline, AutoModelForSequenceClassification
from transformers.pipelines.pt_utils import KeyDataset


def main(args):
    # --- Configuration ---
    input_file = Path(args.input_file)
    indication_column = args.indication_column
    output_file = Path(args.output_file)
    model_path = Path(args.model_path)

    # --- Import Data ---
    print(f"Reading input file from {input_file}")
    input_df = (
        pd.read_csv(
            input_file,
            dtype={indication_column: str},
        )
    )

    # --- Unique Output ---
    if args.unique_output:
        input_df = (input_df
                    .loc[:, [indication_column]]
                    .drop_duplicates()
        )

    # --- Preprocess Data ---
    # Convert to lower case, as the model was trained on uncased data
    input_df[f"_Input_String"] = input_df[indication_column].str.lower()

    # Create the inference dataset (HF Dataset) with unique entries and no NAs
    inference_dataset = Dataset.from_pandas(
        input_df
        .loc[:, ["_Input_String"]]
        .drop_duplicates()
        .dropna()
    )
    print(f"Inference dataset size: {len(inference_dataset)} unique entries from {len(input_df)} total")

    # --- Loading Model & Inference ---
    print(f"Loading model from {model_path}")
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    inference_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None,
                                  device=args.device)

    print("Performing inference")
    pred_output = []
    for out in tqdm(inference_pipeline(KeyDataset(inference_dataset, "_Input_String"), batch_size=args.batch_size)):
        pred_output.append(out)

    # --- Postprocess Data ---
    # Convert the predictions to a DataFrame
    row_dicts = [{x["label"]: x["score"] for x in prediction} for prediction in pred_output]
    inference_classified_unique_probs = pd.DataFrame.from_dict(row_dicts)
    inference_classified_unique_probs.index = inference_dataset["_Input_String"]

    # Binarise the predictions
    inference_classified_unique_binarised = (inference_classified_unique_probs > args.pred_threshold) * 1

    # Expand back to the original size and order
    inference_classified_binarised = input_df.merge(
        inference_classified_unique_binarised, left_on="_Input_String", right_index=True, how="left",
        validate="many_to_one")

    inference_classified_binarised = (
        inference_classified_binarised
        .drop(columns=["_Input_String"])
        .set_index(indication_column)
    )

    # Save results to output path
    inference_classified_binarised.to_csv(output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify Free Text Indications")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input files")
    parser.add_argument("--output_file", type=str, required=True, help="Path to save the output results")
    parser.add_argument("--model_path", type=str, required=True,
                        help="Path to the directory containing the model and tokenizer")
    parser.add_argument("--indication_column", default="Indication", type=str,
                        help="Name of the column in the input file containing the indications")
    # Optional Arguments
    parser.add_argument("--unique_output", action="store_true", help="Returns the result for just the distinct subset of indications.")
    parser.add_argument("--device", type=str, default="cpu",
                        help="Device to run the model on ('cpu' or '0', '1',... for GPU)")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for inference")
    parser.add_argument("--pred_threshold", type=float, default=0.5, help="Threshold for binarizing the predictions")

    args = parser.parse_args()
    main(args)
