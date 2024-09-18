# Data Folder
Training, validation and testing data, as well as generated data.
Files stored in this directory are excluded from the VCS.

Contains a mixture of generated data (model weights, metrics, predictions) and training/testing data.

Example structure
```
.
├── consensus_labels
│   ├── Changelog.md
│   ├── consensus_labels_2022-11-02.csv
│   ├── consensus_labels_2023-04-11.csv
│   ├── consensus_labels_2023-08-14_1.csv
│   └── consensus_labels_2023-08-14_2.csv
├── data_sets
│   ├── Banbury
│   │   ├── Full_Banbury_Data_Set.csv
│   │   ├── Info.txt
│   │   └── Test_Set_2000.csv
│   ├── Oxford
│   │   ├── Full_Oxford_Data_Set.csv
│   │   ├── Test_Set_2000.csv
│   │   ├── Test_Set_Full.csv
│   │   ├── Train_Set_4000.csv
│   │   └── Train_Set_Full.csv
│   └── README.md
├── LUTs
│   └── NHS_Main_Speciality_Code.csv
├── model_output
│   └── ...
├── publication_ready
│   ├── consensus_labels_full_2023-08-23.csv
│   ├── testing_banbury_2023-08-23.csv
│   ├── testing_oxford_2023-08-23.csv
│   └── training_oxford_2023-08-23.csv
└── README.md
```

## Folder `consensus_labels/`
Contains the raw labelled data before merging. All the pre-preprocessed and sharable files (required for training & testing) are saved under the `publication_ready` folder.

## Folder `data_sets/`
Raw datasets, containing the full prescribing data from each centre, randomly sampled ones and more.
Input for the pre-processing step.

Data is split by centre, with subfolder for each site `Oxford` and `Banbury`

## Folder `LUTs`
Look up tables for various scripts (e.g. ICD10 -> Infection source mapping)

## Folder `publication_ready/`
Pre-processed raw data, direct input for training and validation/testing. All files in this folder are shareable.

## Filder `model_output`
Generated files by each model/method. Contains weights, parameters, prediction output and metrics.
