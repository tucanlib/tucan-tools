from glob import glob
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [12, 6]

def get_last_grades(grades_path = 'grades'):
    files = sorted(glob(grades_path + '/*.txt'))
    if not len(files):
        return ''

    with open(files[-1]) as f:
        return [[y.strip() for y in x.split('\t\t') ]for x in f.readlines()]

df = pd.DataFrame(get_last_grades(), columns = ['grade', 'date', 'title']).set_index('title')
df['grade'] = pd.to_numeric(df.grade)
df['date'] = pd.to_datetime(df.date)

df.plot(x='date', y='grade', style=".")
