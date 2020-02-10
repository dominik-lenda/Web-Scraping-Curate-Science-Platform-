import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

df = pd.read_csv('stats.csv')

df = df.sort_values(by=['year'], ascending = True)

# prepare access graph
df1 = df[['access_bool', 'year']]

df1 = df1.groupby('year', as_index=False).agg('mean')

# remove last row (2020)
df1 = df1.drop(df1.tail(1).index)

prop = sns.lineplot(x="year", y="access_bool", data=df1)
prop.set(xlabel='year', ylabel='proportion of articles with access')

plt.savefig('access_prop.pdf')
plt.show()


# prepare graph with badges
df2 = df[['year', 'open_materials', 'open_data', 'preregistration']]

df2 = df2.groupby('year', as_index=False).agg('mean')

# remove last row (2020)
df2 = df2.drop(df2.tail(1).index)

df2 = pd.melt(df2, id_vars = ['year'], var_name='badges', value_name='stats')

badge = sns.lineplot(x="year", y="stats", hue = "badges", data=df2)

badge.set(xlabel='year', ylabel='sum of articles with a badge')

plt.savefig('badges_prop.pdf')
plt.show()
