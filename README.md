# HW-1-DataMining
系級：資工碩一\
學號：P7610 4419\
姓名：李易庭\
Report Url: [HackMD](https://hackmd.io/AlW2AiI7RPmGbmMdZcsCHg?edit)


## Run the code.
using CLI, pipenv

```bash
pipenv install
pipenv shell
python3 main.py --help
```

## Customize some Configurations and Hyperparameters.
using **config.py** to setup.
1. Configurations:
> - DISPLAY: Display the rules by STDOUT.
> - WRITE_FILE: Write relations into csv files.
> - KAG_LIMIT: The limit of data for kaggle dataset when read in data.
> - OUTPUT_DIR: The output directory for csv files.
2. Hyperparameters:
> - min_sup: The minimum for support value (The FP-Growth Algo. will transform to min_sup * number of transactions).
> - min_conf: The minimum for confidenct value.
3. Dataset:
> - ibm: The ibm 2020 dataset.
> - ibm_test_xs: A self define extra small dataset.
> - ibm_2021: The ibm 2021 dataset.
> - kaggle: A dataset provided by [Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis/data?select=departments.csv.zip).