# Electornic Health Records - Indication Processing

Tools and pipeline to process, classify and analyse free-text medication prescription indications. 

---

> Code accompanying the paper:
> "Transformers and large language models are efficient feature extractors for electronic health record studies"


<details>
<summary>Abstract</summary>

While free-text data is abundant in electronic health records, challenges in accurate and scalable information extraction mean less specific clinical codes are often used instead. 
 
We investigated the efficacy of modern natural language processing methods (NLP) and large language models (LLMs) for extracting features from 938,150 hospital antibiotic prescriptions from Oxfordshire, UK. Specially we tried to infer the type of infection or infections being treated from a free-text box completed by clinicians describing the reason (indication) for antibiotics being given.  A subset of the 4000 most frequent unique indications for antibiotic use (representing 692,310 prescriptions) were used for model training. Text was labelled by clinical researchers into 11 categories, describing the infection source/clinical syndrome, and models trained to determine the binary presence/absence of these infection types, and any uncertainty expressed by clinicians. 
>
On separate internal (n=2000 prescriptions) and external test datasets (n=2000 prescriptions), a fine-tuned domain-specific Bio+Clinical BERT model averaged an F1 score of 0.97 and 0.98 respectively across the 11 categories and outperformed traditional regex (F1=0.71 and 0.74) and n-grams/XGBoost (F1=0.86 and 0.84) models. A zero-shot OpenAI GPT4 model achieved F1 scores of 0.71 and 0.86 without using labelled training data and a fine-tuned GPT3.5 model F1 scores of 0.95 and 0.97. Hence, finetuned BERT-based transformer models and fine-tined LLMs performed best, while zero-shot LLMs matched the performance of traditional NLP without the need for labelling. Comparing infection sources obtained from free-text indications to those inferred from ICD-10 codes, free-text indications revealed specific infection sources 31% more often. 

Modern transformer-based models have the potential to be used widely throughout medicine to extract information from structured free-text records, providing more granular information than clinical codes to facilitate better research and patient care.
</details>


## Repo Structure
Short description of the folder structure in this repository. Please consult the the `README.md` in each subfolder for more details.
```
.
├── 00_Data
│   └── ... # Data folder (input and output files)
├── 01_Preprocessing
│   └── ... # Pre-processing scripts for the raw indication and patient data
├── 02_Models
│   └── ... # Model declarations, code training and testing each model
├── 03_Evaluation
│   └── ... # Scripts to evaluate the performance the model's predictions
├── 04_Report
│   └── ... # Code to create the other plots in the paper
├── 05_Deployment
│   └── ... # Deployment scripts for pretrained (BERT based) models
└── 99_Sandbox
    └── ... # Excluded from VCS. Used to test code locally without being committed
```
## Setup
All of the required dependencies for python are listed in the `requirements.txt` file. To set up the project, create a new virtual environment and install the packages:

```bash
pip install -r requirements.txt
```


## Inferrence/Deployment of Classification Model
Check out the folder `05_Deployment` to find an example script to run inference using Bio+Clinical BERT on a list of indications. The example works with both CPUs and GPUs.


## Cite
If you use, modify, or deploy any part of the code or results from this repository, please cite the [following paper](doi.org/10.21203/rs.3.rs-4651377/v1):
```
@article{yuan2024transformers,
  title={Transformers and large language models are efficient feature extractors for electronic health record studies},
  author={Yuan, Kevin and Yoon, Chang Ho and Gu, Qingze and Munby, Henry and Walker, Sarah and Zhu, Tingting and Eyre, David},
  year={2024}
}
```