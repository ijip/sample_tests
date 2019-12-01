import pandas as pd
from scipy import stats
import scipy.stats as st

#считываем файл с данными, добавляя header и разделяя параметры сепаратором ','
file = pd.read_csv("/usr/local/data/transactions.txt", sep=',', header= None, names=['note', 'clientId', 'transactionVal', 'segment'])
# выведем количество клиентов для каждого из сегментов без повтора клиентов
print(file.drop_duplicates(subset='clientId')['segment'].value_counts())
# подсчёт среднего объема транзакций в каждом из сегментов
mean = file.groupby('segment')['transactionVal'].mean()
# передадим значения переменным mean_af, mean_r для сегментов af и r соответственно
mean_af, mean_r = mean[0], mean[1]
# выборка данных объёмов транзакций сегмента AF
x_af = file[file['segment'] == 'AF']['transactionVal'].reset_index(drop=True)
# выборка данных объёмов транзакций сегмента R
x_r = file[file['segment'] == 'R']['transactionVal'].reset_index(drop=True)
# доверительный интервал для среднего объема отдельной транзакции сегмента AF
tint_af = stats.t.interval(alpha=0.9, df= len(x_af)-1, loc=mean_af, scale=st.sem(x_af))
# доверительный интервал для среднего объема отдельной транзакции сегмента R
tint_r = stats.t.interval(alpha=0.9, df= len(x_r)-1, loc=mean_r, scale=st.sem(x_r))
print(tint_af) # вывод доверительных интервалов для af
print(tint_r) # вывод доверительных интервалов для r
print(stats.ttest_ind(tint_af, tint_r)) # проверим гипотезу о равенстве средних объемов отдельных транзакций между сегментами
# Если при выводе этой функции значение прараметра pvalue будет сильно выше 0,1 (уровень значимости 10%), то
# гипотезу о равенстве средних объемов

