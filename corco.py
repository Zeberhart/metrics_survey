"""
Functions for calculating the statistical significant differences between two dependent or independent correlation
coefficients.
The Fisher and Steiger method is adopted from the R package http://personality-project.org/r/html/paired.r.html
and is described in detail in the book 'Statistical Methods for Psychology'
The Zou method is adopted from http://seriousstats.wordpress.com/2012/02/05/comparing-correlations/
Credit goes to the authors of above mentioned packages!
Author: Philipp Singer (www.philippsinger.info)
"""

from __future__ import division

__author__ = 'psinger'

import numpy as np
import pandas
from scipy.stats import t, norm
from math import atanh, pow
from numpy import tanh

def rz_ci(r, n, conf_level = 0.95):
    zr_se = pow(1/(n - 3), .5)
    moe = norm.ppf(1 - (1 - conf_level)/float(2)) * zr_se
    zu = atanh(r) + moe
    zl = atanh(r) - moe
    return tanh((zl, zu))

def rho_rxy_rxz(rxy, rxz, ryz):
    num = (ryz-1/2.*rxy*rxz)*(1-pow(rxy,2)-pow(rxz,2)-pow(ryz,2))+pow(ryz,3)
    den = (1 - pow(rxy,2)) * (1 - pow(rxz,2))
    return num/float(den)

def dependent_corr(xy, xz, yz, n, twotailed=True, conf_level=0.95, method='steiger'):
    """
    Calculates the statistic significance between two dependent correlation coefficients
    @param xy: correlation coefficient between x and y
    @param xz: correlation coefficient between x and z
    @param yz: correlation coefficient between y and z
    @param n: number of elements in x, y and z
    @param twotailed: whether to calculate a one or two tailed test, only works for 'steiger' method
    @param conf_level: confidence level, only works for 'zou' method
    @param method: defines the method uses, 'steiger' or 'zou'
    @return: t and p-val
    """
    if method == 'steiger':
        d = xy - xz
        determin = 1 - xy * xy - xz * xz - yz * yz + 2 * xy * xz * yz
        av = (xy + xz)/2
        cube = (1 - yz) * (1 - yz) * (1 - yz)

        t2 = d * np.sqrt((n - 1) * (1 + yz)/(((2 * (n - 1)/(n - 3)) * determin + av * av * cube)))
        p = 1 - t.cdf(abs(t2), n - 3)

        if twotailed:
            p *= 2

        return t2, p
    elif method == 'zou':
        L1 = rz_ci(xy, n, conf_level=conf_level)[0]
        U1 = rz_ci(xy, n, conf_level=conf_level)[1]
        L2 = rz_ci(xz, n, conf_level=conf_level)[0]
        U2 = rz_ci(xz, n, conf_level=conf_level)[1]
        rho_r12_r13 = rho_rxy_rxz(xy, xz, yz)
        lower = xy - xz - pow((pow((xy - L1), 2) + pow((U2 - xz), 2) - 2 * rho_r12_r13 * (xy - L1) * (U2 - xz)), 0.5)
        upper = xy - xz + pow((pow((U1 - xy), 2) + pow((xz - L2), 2) - 2 * rho_r12_r13 * (U1 - xy) * (xz - L2)), 0.5)
        return lower, upper
    else:
        raise Exception('Wrong method!')

def independent_corr(xy, ab, n, n2 = None, twotailed=True, conf_level=0.95, method='fisher'):
    """
    Calculates the statistic significance between two independent correlation coefficients
    @param xy: correlation coefficient between x and y
    @param xz: correlation coefficient between a and b
    @param n: number of elements in xy
    @param n2: number of elements in ab (if distinct from n)
    @param twotailed: whether to calculate a one or two tailed test, only works for 'fisher' method
    @param conf_level: confidence level, only works for 'zou' method
    @param method: defines the method uses, 'fisher' or 'zou'
    @return: z and p-val
    """

    if method == 'fisher':
        xy_z = 0.5 * np.log((1 + xy)/(1 - xy))
        ab_z = 0.5 * np.log((1 + ab)/(1 - ab))
        if n2 is None:
            n2 = n

        se_diff_r = np.sqrt(1/(n - 3) + 1/(n2 - 3))
        diff = xy_z - ab_z
        z = abs(diff / se_diff_r)
        p = (1 - norm.cdf(z))
        if twotailed:
            p *= 2

        return z, p
    elif method == 'zou':
        L1 = rz_ci(xy, n, conf_level=conf_level)[0]
        U1 = rz_ci(xy, n, conf_level=conf_level)[1]
        L2 = rz_ci(ab, n2, conf_level=conf_level)[0]
        U2 = rz_ci(ab, n2, conf_level=conf_level)[1]
        lower = xy - ab - pow((pow((xy - L1), 2) + pow((U2 - ab), 2)), 0.5)
        upper = xy - ab + pow((pow((U1 - xy), 2) + pow((ab - L2), 2)), 0.5)
        return lower, upper
    else:
        raise Exception('Wrong method!')

# features = ["accurate", "adequate", "concise", "similarity",  "bleu", "b1" ,"b2"  ,"b3"  ,"b4"]
# p = pandas.read_csv("results_bleu_cat.csv")
# c = p[features].corr()


# print(c)

# target = "similarity"
# features.remove(target)

# print("steiger")
# for i,f1 in enumerate(features):
#     for f2 in features[i+1:]:
#         tval, p = dependent_corr(c[target][f1], c[target][f2], c[f1][f2],210, method='steiger')
#         if p>.05:
#             print("%s - %s: %f"%(f1, f2, p))

# print("zou")
# for i,f1 in enumerate(features):
#     for f2 in features[i+1:]:
#         l, u = dependent_corr(c[target][f1], c[target][f2], c[f1][f2],210, method='zou')
#         if u>0 and l<0:
#             print("%s - %s:%f %f"%(f1, f2, l, u))

import scipy.stats as ss
print(ss.rankdata([1,2,2,4]))

p = pandas.read_csv("results_bleu_cat.csv")
u1 = p.loc[p["user_id"]==1]
u2 = p.loc[p["user_id"]==3]
u3 = p.loc[p["user_id"]==4]
b = [(b1 + b2 + b3)/3 for b1,b2,b3 in zip(u1["bleu"], u2["bleu"], u3["bleu"])]


adequate = pandas.DataFrame({"u1": list(u1["adequate"]), "u1source": list(u1["source"]), "u2":list(u2["adequate"]), "u2source": list(u2["source"]), "u3":list(u3["adequate"]), "u3source": list(u3["source"]), "b": b})
accurate = pandas.DataFrame({"u1": list(u1["accurate"]), "u1source": list(u1["source"]), "u2":list(u2["accurate"]), "u2source": list(u2["source"]), "u3":list(u3["accurate"]), "u3source": list(u3["source"]), "b": b})
concise = pandas.DataFrame({"u1": list(u1["concise"]), "u1source": list(u1["source"]), "u2":list(u2["concise"]), "u2source": list(u2["source"]), "u3":list(u3["concise"]), "u3source": list(u3["source"]), "b": b})
similarity = pandas.DataFrame({"u1": list(u1["similarity"]), "u1source": list(u1["source"]), "u2":list(u2["similarity"]), "u2source": list(u2["source"]), "u3":list(u3["similarity"]), "u3source": list(u3["source"]), "b": b})


cadequate = adequate.corr()
caccurate = accurate.corr()
cconcise = concise.corr()
print(cadequate)
print(caccurate)
print(cconcise)
print()


features13 = ["u1", "u3", "b"]
adequate13 = adequate.loc[adequate["u1source"]==adequate["u3source"]]
accurate13 = accurate.loc[accurate["u1source"]==accurate["u3source"]]
concise13 = concise.loc[concise["u1source"]==concise["u3source"]]

cadequate13 = adequate13[features13].corr()
caccurate13 = accurate13[features13].corr()
cconcise13 = concise13[features13].corr()
print(cadequate13)
print(caccurate13)
print(cconcise13)

print() 

features23 = ["u2", "u3", "b"]
adequate23 = adequate.loc[adequate["u3source"]==adequate["u2source"]]
accurate23 = accurate.loc[accurate["u3source"]==accurate["u2source"]]
concise23 = concise.loc[concise["u3source"]==concise["u2source"]]

cadequate23 = adequate23[features23].corr()
caccurate23 = accurate23[features23].corr()
cconcise23 = concise23[features23].corr()
print(cadequate23)
print(caccurate23)
print(cconcise23)




target = "u3"
f1 = "b"

f2 = "u1"
for i,c in enumerate([cadequate13, caccurate13, cconcise13]):
    tval, p = dependent_corr(c[target][f1], c[target][f2], c[f1][f2],105, method='steiger')
    if p>.05:
        print("strieger %f: %s - %s: %f"%(i, f1, f2, p))

    l, u = dependent_corr(c[target][f1], c[target][f2], c[f1][f2],105, method='zou')
    if u>0 and l<0:
        print("zou %f: %s - %s:%f %f"%(i, f1, f2, l, u))





f2 = "u2"
for i,c in enumerate([cadequate23, caccurate23, cconcise23]):
    tval, p = dependent_corr(c[target][f1], c[target][f2], c[f1][f2],105, method='steiger')
    if p>.05:
        print("strieger %f: %s - %s: %f"%(i, f1, f2, p))

    l, u = dependent_corr(c[target][f1], c[target][f2], c[f1][f2],105, method='zou')
    if u>0 and l<0:
        print("zou %f: %s - %s:%f %f"%(i, f1, f2, l, u))



