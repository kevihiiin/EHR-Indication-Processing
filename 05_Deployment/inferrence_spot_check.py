#!/usr/bin/env python3
"""Quick spot-check tool for classifying single indications.

Loads the model once, then enters an interactive loop where you can type
an indication and immediately see the predicted categories.

Usage:
    python inferrence_spot_check.py --model_path <path_to_model_dir>
    python inferrence_spot_check.py --model_path <path_to_model_dir> --device 0
    python inferrence_spot_check.py --model_path <path_to_model_dir> --query "pneumonia"
"""

import argparse
import json

from transformers import AutoTokenizer, pipeline, AutoModelForSequenceClassification


def classify(pipe, text, threshold):
    text = text.strip().lower()
    raw = pipe(text)[0]
    scores = {r["label"]: round(r["score"], 4) for r in sorted(raw, key=lambda x: x["score"], reverse=True)}
    positive = {label: score for label, score in scores.items() if score >= threshold}
    return {"input": text, "predictions": positive, "all_scores": scores}


def main(args):
    print(f"Loading model from {args.model_path} ...")
    model = AutoModelForSequenceClassification.from_pretrained(args.model_path)
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    pipe = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None, device=args.device)
    print("Model loaded.\n")

    threshold = args.pred_threshold

    # Single query mode
    if args.query:
        result = classify(pipe, args.query, threshold)
        print(json.dumps(result, indent=2))
        return

    # Interactive mode
    print("Enter an indication to classify (Ctrl+C or 'q' to quit):")
    while True:
        try:
            text = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break
        if not text or text.lower() == "q":
            print("Bye!")
            break
        result = classify(pipe, text, threshold)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spot-check single indications against the classifier")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the model and tokenizer directory")
    parser.add_argument("--device", type=str, default="cpu", help="Device ('cpu' or '0', '1', ... for GPU)")
    parser.add_argument("--pred_threshold", type=float, default=0.5, help="Threshold for positive classification")
    parser.add_argument("--query", type=str, default=None, help="Single query to classify (skips interactive mode)")
    args = parser.parse_args()
    main(args)
