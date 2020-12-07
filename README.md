# Learning Mealy Reward Machines

Code for the framework which learns reward models with temporal dependencies. The associated publication is Rens et al. (2021) Online Learning of Non-Markovian Reward Models

The following are basic instructions for running the algorithm that learns Mealy Reward Machines (MRMs) and for running the baseline deep NN. We call the former Angluin Reward Machine (ARM) and the latter Deep Q-learning Network (DQN).

To run ARM, simply run the Experiments.py file, which is locates in src/ARM_Learning_MRMs.

Remember to select the desired domain (treasure-map, cube, etc.) by (un)commenting the appropriate lines at the top of ARM.py, getExperience.py and MRM_learning_tools.py

To run DQN, simply run the Q_learning_kerasrl.py file, which is located in src/DQN_baseline.

Remember to select the desired domain (treasure-map, cube, etc.) by (un)commenting the appropriate lines in Q_learning_kerasrl.py to set the ENV_NAME variable.


# Dependencies:

The main dependency to mention now is the 'stormpy' package.
Informatin about its installation can be found at https://moves-rwth.github.io/stormpy/installation.html#requirements.
stormpy requires Storm. Info about its installation can be found at https://www.stormchecker.org/documentation/obtain-storm/build.html. From our experience, it is best to build storm from source. If you attempt to install it using Homebrew, you are likely to run into problems with installing stormpy.

An important not here is that you must make sure that both Storm and stormpy are based on the same version.

There is more advice at the links provided above.
