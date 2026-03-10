# Deployment of the model
Pre-trained model ready to be used in an production environment.

Two options are available: 
1. Run via standalone Python version via CLI
2. Standalone deployment via Docker (recommended)

## Standalone Python/Bash
The model can be run via the CLI. The following steps are required to run the model:
1. Install the required packages (from within `05_Deployment/`):
   - **uv (recommended):** `uv sync`
   - **pip:** `pip install .` (or `pip install ./05_Deployment` from the repo root)
2. Download the pretrained model weights into a path of your choice (`<path_to_model>`)

```
Classify Free Text Indications

optional arguments:
  -h, --help            show this help message and exit
  
  --input_file INPUT_FILE
                        Path to the input files
                        
  --output_file OUTPUT_FILE
                        Path to save the output results
                        
  --model_path MODEL_PATH
                        Path to the directory containing the model and tokenizer
                        
  --indication_column INDICATION_COLUMN
                        Name of the column in the input file containing the indications
                        
  --unique_output       Returns the result for just the distinct subset of indications.
  
  --device DEVICE       Device to run the model on ('cpu' or '0', '1',... for GPU)
  
  --batch_size BATCH_SIZE
                        Batch size for inference
                        
  --pred_threshold PRED_THRESHOLD
                        Threshold for binarizing the predictions
```

**Basic Usage Example:**
```bash
python3 inferrence.py --input_file data/abx_prescriptions.csv --output_file data/abx_prescriptions_classified.csv --model_path data/Bio_ClinicalBERT_5615.pth

```
-> This will return the original input dataframe with added columns for the model predictions.

**Indication Column**

By default, the model will look for the column named `Indication` in the input file.
If you have a different column name, use the `--indication_column` flag to specify the column name.

```bash
python3 inferrence.py --input_file <input_file> --output_file <output_file> --model_path <model_path> --indication_column "My Column"
```

**Unique Output**

To return the result for just the distinct subset of indications, use the `--unique_output` flag. 
This will return only the indications column + the model predictions.

```bash
python3 inferrence.py --input_file <input_file> --output_file <output_file> --model_path <model_path> --unique_output
```

**Usage GPU or MPS**

By default the model will run on the CPU. To run the model on the GPU, use the `--device` flag. 
This is passed on to pytorch as the device to use.
For a GPU, the device should be set to the GPU number, on Apple Silicon, this should be set to `mps`
For example, to run the model on GPU 0, use the following command:
```bash
python3 inferrence.py --input_file <input_file> --output_file <output_file> --model_path <model_path> --device 0
```

## Spot Checking / Interactive Mode

The `inferrence_spot_check.py` script loads the model once and lets you classify individual indications without processing an entire CSV file. Useful for quick sanity checks and demos.

**Interactive mode** — type indications one at a time:
```bash
python3 inferrence_spot_check.py --model_path <path_to_model>
```

**Single query mode** — classify one indication and exit:
```bash
python3 inferrence_spot_check.py --model_path <path_to_model> --query "pneumonia"
```

Options: `--device` (default `cpu`), `--pred_threshold` (default `0.5`).

## Standalone Docker
TODO, add docker wrapper for the model
