from nltk.translate.bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction
import pandas
import scipy.stats as s

smoothing = SmoothingFunction()

p = pandas.read_csv("results.csv")

refs = [a.split() if source=="reference" else b.split() for a,b,source in zip(p['text'], p['text.1'], p["source"])]
preds = [a.split() if source=="alex1" else b.split() for a,b,source in zip(p['text'], p['text.1'], p['source'])]

scores = [sentence_bleu([rr], pr) for rr, pr in zip(refs, preds)]
b1 = [corpus_bleu([[rr]], [pr], weights=(1,0,0,0)) for rr, pr in zip(refs, preds)]
b2 = [corpus_bleu([[rr]], [pr], weights=(0,1,0,0)) for rr, pr in zip(refs, preds)]
b3 = [corpus_bleu([[rr]], [pr], weights=(0,0,1,0)) for rr, pr in zip(refs, preds)]
b4 = [corpus_bleu([[rr]], [pr], weights=(0,0,0,1)) for rr, pr in zip(refs, preds)]

print(b4)

# p['bleu'] = scores
# p['b1'] = b1
# p['b2'] = b2
# p['b3'] = b3
# p['b4'] = b4

# stats = p["bleu"].describe(percentiles=[.25, .50, .75])
# bleu_cat = []
# print(stats["25%"], stats["50%"], stats["75%"])
# for score in p["bleu"]:
#     if score < stats["25%"]:
#         bleu_cat.append(1)
#     elif score < stats["50%"]:
#         bleu_cat.append(2)
#     elif score < stats["75%"]:
#         bleu_cat.append(3)
#     else:
#         bleu_cat.append(4)
# p["bleu_cat"] = bleu_cat 

# print(s.kendalltau(p["similarity"], p['bleu']))
# print(s.kendalltau(p["similarity"], p['bleu_cat']))
# print(s.kendalltau(p["similarity"].loc[p["user_id"]==1], p['bleu'].loc[p["user_id"]==1]))
# print(s.kendalltau(p["similarity"].loc[p["user_id"]==1], p['bleu_cat'].loc[p["user_id"]==1]))
# print(s.kendalltau(p["similarity"].loc[p["user_id"]==3], p['bleu'].loc[p["user_id"]==1]))
# print(s.kendalltau(p["similarity"].loc[p["user_id"]==3], p['bleu_cat'].loc[p["user_id"]==1]))
# print(s.kendalltau(p["bleu"], p['bleu_cat']))
# print(s.kendalltau(p["similarity"].loc[p["user_id"]==1], p["similarity"].loc[p["user_id"]==3]))

# p.to_csv("results_bleu_cat.csv", index=False)