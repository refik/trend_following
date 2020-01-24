# Project 15: Trend following, momentum crashes and high correlations

1. Kai BANTO ECKERT - kai.bantoeckert@unil.ch
2. Refik TURKELI - refik.turkeli@unil.ch
3. Karel VAN DER BEN - karel.vanderben@unil.ch

### How to run this project

After installing python, required package has to be installed with the command:

```
# pip install requirements.txt 
```

Results can be explored using Jupyer notebooks on the file `Interactive Results.ipynb`. The easiest way to explore the results in through the [web application](https://tsmom.herokuapp.com/).

The web application can be run locally using:

```
# python app.py 
```

### Description of files

- `dataset.py` Functions for clean access to all the data used in the project. 
- `calculate.py` Calculations for portfolio statistics.
- `strategy.py` Weight and price transformation calculations for all employed strategies.
- `viz.py` Plots of portfolio statistics.
- `report.py` LaTeX table generating function for the report.
- `app.py` The code for the [web application](https://tsmom.herokuapp.com/).
- `Interactive Results.ipynb` Jupyter notebook for local interactive testing of strategies.
- `data/` Data files of the project.
- `requirements.txt` Packages that are required to be installed for this project.