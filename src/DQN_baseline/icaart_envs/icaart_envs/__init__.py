from gym.envs.registration import register

register(id='TreasureMapWorldSmall-v0',
         entry_point = 'icaart_envs.envs:TreasureMapWorldSmall')
register(id='Cube-v0',
         entry_point = 'icaart_envs.envs:Cube')
register(id='TreasureMapWorld-v0',
         entry_point = 'icaart_envs.envs:TreasureMapWorld')
register(id='OfficeBot-v0',
         entry_point = 'icaart_envs.envs:OfficeBot')

# register(id='TreasureMapWorldSmall-v0',
#          entry_point = 'src.DQN_baseline.icaart_envs.icaart_envs.envs:TreasureMapWorldSmall')
# register(id='Cube-v0',
#          entry_point = 'src.DQN_baseline.icaart_envs.icaart_envs.envs:Cube')
# register(id='TreasureMapWorld-v0',
#          entry_point = 'src.DQN_baseline.icaart_envs.icaart_envs.envs:TreasureMapWorld')
# register(id='OfficeBot-v0',
#          entry_point = 'src.DQN_baseline.icaart_envs.icaart_envs.envs:OfficeBot')
