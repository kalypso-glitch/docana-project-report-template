import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

#loading the user's data
df = pd.read_csv(r"data/user_stats.csv")
dfsorted=df.sort_values(by='count_posts', ascending=False)

df = dfsorted.iloc[2:] #removing the top 2 users as they are likely bots

#plotting for all users
x = df['count_posts'] 
y = df['avg_wo_outliers']  

plt.scatter(x, y, color='blue', marker='x')
plt.xlabel('Number of posts')
plt.ylabel('Average Post Complexity')
plt.show()

#linear regression_figure 2
slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.xlabel('Number of posts')
plt.ylabel('Post Complexity')
plt.show()

#sorting top 10 users by posts
top10=df.nlargest(10, 'count_posts')
#print(top10)


#saving in a new csv file
#top10.to_csv('c:\\Users\\kassi\\OneDrive\\Έγγραφα\\master\\(3) sose 26\\Document analysis\\final project\\top10users.csv', index=False)
 
#plotting top 10 users_figure 3

x = top10['count_posts']
y = top10['avg_wo_outliers']

plt.plot(x,y)
plt.xlabel('Number of posts')
plt.ylabel('Average Post Complexity')

plt.show()
