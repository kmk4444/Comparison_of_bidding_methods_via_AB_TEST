import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Without a grounding in Statistics, a Data Scientist  is a Data Lab Assistant.
################################ TASK 1 ###############################################

# Step 1: read the ab_testing_data.xlsx data consists of control and test group.
# Give different variables for control and test group data

df_control = pd.read_excel("WEEK_4/ÖDEVLER/AB_Testing/ab_testing.xlsx", sheet_name = "Control Group" )
df_test = pd.read_excel("WEEK_4/ÖDEVLER/AB_Testing/ab_testing.xlsx", sheet_name = "Test Group" )

df_control.columns = ["Impression_control", "Click_control", "Purchase_control", "Earning_control"]
df_test.columns = ["Impression_test", "Click_test", "Purchase_test", "Earning_test"]

#Step 2: Control and test group data is analyzed.

def check_df(dataframe, head=5):
    print("############### shape #############")
    print(dataframe.shape)
    print("############### types #############")
    print(dataframe.dtypes)
    print("############### head #############")
    print(dataframe.head)
    print("############### tail #############")
    print(dataframe.tail)
    print("############### NA #############")
    print(dataframe.isnull().sum())
    print("############### Quantiles #############")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


check_df(df_control)
check_df(df_test)


# Step 3: Combine control and test group data by the means of concat function.
df = pd.concat([df_test, df_control],axis=1)

################################ TASK 2 ###############################################

#Step 1: Describe hypothesis testing
# H0: M1=M2 => average of the purchase of control and test group is equal.
# H1: M1!=M2

#Step 2: Analyze the average of purchase_test and purchase_control.
df[["Purchase_test","Purchase_control"]].mean()
#it seems that purchase_test is better than purchase_control, nevertheless, we should prove that in statistical ways including AB test.

################################ TASK 3 ###############################################

# Step 1: Check the assumption of normality and variance homogeneity

# Assumption of normality
# HO:Assumption of normality is provided.
# H1:.... not.

test_stat, pvalue = shapiro(df.loc[:,"Purchase_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# pvalue(0.1541) > 0.05;that is to say, assumption of normality could be provided for purchase_test.

test_stat, pvalue = shapiro(df.loc[:,"Purchase_control"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# pvalue(0.5891) > 0.05;that is to say, assumption of normality could be provided for purchase_control.

# variance homogeneity
# HO: Variances are homogeneous
# H1:.... not.

test_stat, pvalue = levene(df.loc[:, "Purchase_test"],
                           df.loc[:,"Purchase_control"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# pvalue (0.1983) > 0.05;namely, variances are homogeneous.

# Step 2: select the optimal test according to the results of Step 1. We have to select ttest.

# Step 3: Apply ttest.

test_stat, pvalue = ttest_ind(df.loc[:,"Purchase_test"],
                              df.loc[:,"Purchase_control"],
                              equal_var = True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


################################ TASK 4 (Analysis of the results) ###############################################

# Step 1: Which test did you utilize, explain reasons.
# We have used ttest on the grounds that assumption of normality as well as variance was ensured.

# Step 2: give advice to customers in accord with the results of test.
# pvalue (0.3493) > 0.05; namely, we cannot reject ho (average of the purchase of control and test group is equal.)
# we recommend to customer that the rate of investment for average bidding should be removed because it could not rise the rate of purchase.
