import numpy as np
import pandas
from scipy.stats import t, norm
from math import atanh, pow
from numpy import tanh

features = ["accurate", "adequate", "concise", "similarity",  "bleu", "b1" ,"b2"  ,"b3"  ,"b4"]
p = pandas.read_csv("results_bleu.csv")

stats = p["bleu"].describe(percentiles=[.219, .557, .786])
print(stats)
bleu_cat = []
for score in p["bleu"]:
    if score < stats["21.9%"]:
        bleu_cat.append(1)
    elif score < stats["55.7%"]:
        bleu_cat.append(2)
    elif score < stats["78.6%"]:
        bleu_cat.append(3)
    else:
        bleu_cat.append(4)
p["bleu_cat"] = bleu_cat 

for i, row in p.iterrows():
    if abs(row["similarity"]-row["bleu_cat"]) >= 2:
        print("Sim: %f, BleuQuad: %f, bleu: %f, Accuracy: %f, Adequate: %f, Concise: %f"%(row["similarity"],row["bleu_cat"], row["bleu"], row["accurate"], row["adequate"], row["concise"]))
        print(row["source"])
        print(row["text"])
        print(row["text.1"])
        print()

print(len(p.loc[((p["similarity"] < 3) & (p["bleu_cat"] >2)) | ((p["similarity"] >= 3) & (p["bleu_cat"]<= 2))]))

print(p.describe())
print(p.loc[((abs(p["similarity"]-p["bleu_cat"]) >= 2) & (p["source"] == "alex1"))].describe())

print(len(p.loc[p["similarity"] == 1]))
print(len(p.loc[p["similarity"] == 2]))
print(len(p.loc[p["similarity"] == 3]))
print(len(p.loc[p["similarity"] == 4]))