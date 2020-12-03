import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")

# fm = pd.read_csv('/results/FM_cumultv_Cube Problem_ExpVal0.15.csv')
ql = pd.read_csv('/results/d_q_learning_baseline_TreasureMapWorldNew-v0_single_start')

fig, ax = plt.subplots()

# sns.lineplot(data=fm, x="Episodes/10", y="Return", color='b', ax = ax)
sns.lineplot(data=ql, x="Episodes/1", y="Return", color='r', ax = ax)
plt.legend(['ARM', 'DQN'], loc='upper left')
plt.show()

# plt.legend(loc='lower right', frameon=False, ['Q-learn', 'Angluin-RM'])