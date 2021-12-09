import pandas as pd
import os

csv_path = r'G:\07_FrieseZeegat_Classificatie\04_Workspace\FrieseZeegat_run_2\Run_stats.csv'


df = pd.read_csv(csv_path, sep=';')
tot_elapsed_time = pd.to_timedelta(df['Elapsed time']).sum()
print(f'one at a time, 2 at a time')
print(f'{tot_elapsed_time}, {tot_elapsed_time/2}')
