from math import sqrt
from scipy import stats

import argparse
import matplotlib.pyplot as plt
import ntpath
import numpy as np
import os
import pandas as pd
import seaborn as sns;
import sys

sns.set(color_codes=True)
sns.set_style({'axes.grid':False})

def main(args):
    # READ INPUT FILE AND GENERATE A PANDAS DATAFRAME WITH IT
    predictions_file = args.input_file
    error_type = args.error_type
    num_of_outlier = args.num_of_outlier
    predictions_file_indentifier = ntpath.basename(predictions_file).replace(".csv","")
    df_predictions = pd.read_csv(predictions_file, sep="\t", header=0)

    if error_type == 'BestFit':
        # CALCULATE SLOPE AND INTERCEPT FOR BEST FIT CURVE BASED ON ACTUAL AND PREDICTION
        slope, intercept, r_value, p_value, std_err = stats.linregress(df_predictions['actual'], df_predictions['predicted'])
        # CALCULATE DISTANCE TO BEST FIT CURVE FOR ALL ITEMS IN THE DATAFRAME USING SLOPE AND INTERCEPT
        df_predictions['dist_to_bestfit'] = abs((slope * df_predictions['actual']) - df_predictions['predicted'] + intercept) / sqrt(pow(slope, 2) + 1)
        # GENERATE NEW DATAFRAME WITH DISTANCES TO BEST FIT CURVE
        df_predictions_sorted = df_predictions.sort_values(['dist_to_bestfit'])

    else:
        # CALCULATE DISTANCE TO ABSOLUTE LINE (y=x)
        df_predictions['dist_to_absolute'] = abs(df_predictions['actual'] - df_predictions['predicted'])
        # GENERATE NEW DATAFRAME WITH DISTANCES TO ABSOLUTE LINE AND SAVE IT TO A NEW .csv
        df_predictions_sorted = df_predictions.sort_values(['dist_to_absolute'])
    
    # SAVE NEW DATAFRAME TO A NEW .csv
    df_predictions_sorted.to_csv("{}_{}_distances.csv".format(predictions_file_indentifier,error_type),index=False)
    # CALCULATES THE AMOUNT OF DATA POINTS TO REMOVE. (DEFAULT IS 10%)
    amount_2_remove = int(round(len(df_predictions)*(num_of_outlier/100)))
    # SEPARATE OUTLIERS FROM REGULAR ENTRIES
    df_non_outliers = df_predictions_sorted[:-amount_2_remove]
    df_outliers = df_predictions_sorted[-amount_2_remove:]

    # DEFINE FIGURE SIZE FOR PLOTTING
    plt.figure(figsize=(9,7), dpi=300)

    # PLOT OUTLIERS
    ax = sns.regplot(x='actual', y='predicted', data=df_outliers, color="red", fit_reg=False, marker="o", label="outliers")
    # PLOT REGULAR DATA

    if error_type == 'Absolute':
        # DRAW SCATTER PLOT WITHOUT REGRESSION LINE BASED ON WHOLE DATAPOINTS
        ax = sns.regplot(x='actual', y='predicted', data=df_predictions_sorted, color="black", fit_reg=False, marker="o", scatter_kws={'alpha':0.3}, label='regular')
        # SET POINTS FOR DRAWING ABSOLUTE LINE (y=x)
        lims = [np.min([ax.get_xlim(), ax.get_ylim()]),np.max([ax.get_xlim(), ax.get_ylim()])]
        # DRAW ABSOULTE LINE (y=x)
        ax.plot(lims,lims, 'k-',alpha=0.75, zorder=0)

    else:
        # DRAW SCATTER PLOT WITH REGRESSION LINE BASED ON WHOLE DATAPOINTS
        ax = sns.regplot(x='actual', y='predicted', data=df_predictions_sorted, color="black", fit_reg=True, marker="o", scatter_kws={'alpha':0.3}, label='regular')

    # SET PLOT LABELS AND TITLE
    ax.set_ylabel('Predicted', fontsize=20, fontweight='bold', color="black")
    ax.set_xlabel('Actual', fontsize=20, fontweight='bold', color="black")
    ax.axhline([0], linestyle=':', color='#aca7a7') # horizontal lines
    ax.axvline([0], linestyle=':', color='#aca7a7') # vertical lines
    ax.patch.set_facecolor("1")
    ax.yaxis.label.set_color('0')
    ax.xaxis.label.set_color('0')
    plt.title('Regression Plot({})'.format(error_type), fontsize=28, fontweight='bold')
    plt.tight_layout()
    # SAVE PLOT TO FILE
    plt.savefig('{}_{}_regression_plot.png'.format(predictions_file_indentifier,error_type),format="png")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SINTAX:\tpython outliers.py data.csv')
    parser.add_argument('-i', dest='input_file', required=True, help='.csv file containing at least two columns separated by tab: | actual | predicted |')
    parser.add_argument('-o', dest='num_of_outlier', help='Set the number of outliers. 20 for 20%% of dataset, 10%% is default.', default=10, type=int)
    parser.add_argument('-e', dest='error_type', help='Choose outliers based on Absolute line (y=x) or BestFit curve: Absolute or BestFit(default)', default='BestFit')
    args = parser.parse_args()
    main(args)