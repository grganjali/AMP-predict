## Installation


**Step 1** - Virtual environment management system
Install [Anaconda](https://www.anaconda.com/distribution/) or [miniconda](https://docs.conda.io/en/latest/miniconda.html).

**Step 2** - Create virtual environment with all dependencies

```shell
conda env create -f requirements.yml
```

**Step 3** - Activate environment

```shell
conda activate data_analysis
```

# Running outliers.py script

After activating the anaconda environment you simply have to run:

```shell
python outliers.py data.csv
```

**Notes**
* Make sure your .csv file has at least two columns "actual" and "prediction"
* We are currently using \\t as a separator character (hard-coded in the script), but you are free to use whatever suits you better. 

# Running boxplots.ipynb script

Run jupyter notebooks:

```shell
jupyter notebook
```
and click on the **boxplots.ipynb** file.
