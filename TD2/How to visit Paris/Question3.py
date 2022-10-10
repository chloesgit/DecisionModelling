import scipy.stats as stats


TE_data=[9/2,5,15.5]
ML_data=[3,4,12]
AT_data=[1,3,9.50]
MO_data=[2,2,11]
JT_data=[3/2,3,0]
CA_data=[2,4,10]
CP_data=[5/2,1,10]
CN_data=[2,5,5]
BS_data=[2,4,8]
SC_data=[3/2,1,8.5]
PC_data=[3/4,3,0]
TM_data=[2,2,15]
AC_data=[3/2,5,0]

dic={"TE":TE_data,"ML":ML_data,"AT":AT_data,"MO":MO_data,"JT":JT_data,"CA":CA_data,"CP":CP_data,"CN":CN_data,"BS":BS_data,"SC":SC_data,"PC":PC_data,"TM":TM_data,"AC":AC_data}

price_list=[dic[x][2] for x in dic.keys()]
distance_list=[dic[x][0] for x in dic.keys()]

tau_kendall, p_value_kendall = stats.kendalltau(price_list, distance_list)
rho_spearman, pval_spearman = stats.spearmanr(price_list, distance_list)
print("Kendall rank correlation coefficient",tau_kendall)
print("Spearman ranking correlation coefficient",rho_spearman)

#Kendall rank correlation coefficient is 0.61 while Spearman's one is 0.74. It is close to 1 so the longer the visit is the more expensive it is, which seems consistent. According to litterature, Kendall's score is usually lower than Spearman's which is the case here.