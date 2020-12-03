import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set(style="darkgrid")
NUOF_TRIALS = 10

cumultv_file_name = ''
results_file_name = ''

# Originally, this file was designed so that different algorithms could be used.
# However, we ended up using only the main algo here, and leaving the baseline algo separate.
# Hence, the following assignment and subsequent code structure.
Algo = 'L_MRM_FM'

if Algo == 'L_MRM_FM':
    import src.ARM_Learning_MRMs.ARM as algo

if Algo == 'L_MRM_FM':
    p = Path('results/FM_params_' + algo.params[1] + '_ExpVal' + str(algo.params[6]) + '.txt')
    with p.open('w') as params_file:
        index = 0
        for param in algo.params:
            line = str(index) + ': ' + str(param)
            line += '\n'
            params_file.write(line)
            index += 1

    cumultv_file_name = '/results/FM_cumultv_' + algo.params[1] + '_ExpVal' + str(algo.params[6]) + '.csv'
    results_file_name = '/results/FM_results_' + algo.params[1] + '_ExpVal' + str(algo.params[6]) + '.txt'

    print('\n--------------------------------------')
    print('             Learning MRM               ')
    print('--------------------------------------\n')


Q_rewards = 0
for t in range(NUOF_TRIALS):
    algo.RewardPerResolutionVector = []
    algo.main(t+1)

    Q_rewards += algo.results[0]

    if t == 0:
        p = Path(cumultv_file_name)
        with p.open('w') as cumultv_file:
            line = 'Episodes/{},Return'.format(algo.RESOLUTION)
            line += '\n'
            cumultv_file.write(line)
            episode = 0
            for r in algo.RewardPerResolutionVector:
                episode += 1
                line = str(episode) + ',' + str(r)
                line += '\n'
                cumultv_file.write(line)

        p = Path(results_file_name)
        with p.open('w') as results_file:
            line = 'Iterations:'+str(NUOF_TRIALS)+'\n'
            results_file.write(line)
            index = 0
            for result in algo.results:
                line = str(index) + ': ' + str(result)
                line += '\n'
                results_file.write(line)
                index += 1
    else:
        p = Path(cumultv_file_name)
        with p.open('a') as cumultv_file:
            episode = 0
            for r in algo.RewardPerResolutionVector:
                episode += 1
                line = str(episode) + ',' + str(r)
                line += '\n'
                cumultv_file.write(line)

        p = Path(results_file_name)
        with p.open('a') as results_file:
            index = 0
            for result in algo.results:
                line = str(index) + ': ' + str(result)
                line += '\n'
                results_file.write(line)
                index += 1


tel = pd.read_csv(cumultv_file_name)
sns.relplot(data=tel, x="Episodes/{}".format(algo.RESOLUTION), y="Return", kind="line")
plt.show()

