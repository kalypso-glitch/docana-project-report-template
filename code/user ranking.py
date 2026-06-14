import pandas as pd
import matplotlib.pyplot as plt

#loading the user's data
df = pd.read_csv('user_stats.csv')
dfsorted=df.sort_values(by='count_posts', ascending=False)

df = dfsorted.iloc[2:] #removing the top 2 users as they are likely bots

x = df['count_posts'] 
y = df['avg_wo_outliers']  

plt.scatter(x, y, color='blue', marker='x')
#plt.plot(x,y)
plt.xlabel('Number of posts')
plt.ylabel('Average Post Complexity')

plt.show()

#sorting top 10 users by posts
top10=df.nlargest(10, 'count_posts')
#print(top10)


#saving in a new csv file
#top10.to_csv('c:\\Users\\kassi\\OneDrive\\Έγγραφα\\master\\(3) sose 26\\Document analysis\\final project\\top10users.csv', index=False)
 
#making a simple graph 
#import matplotlib.pyplot as plt

#x = top10['count_posts'][1:] #skipping the first one
#y = top10['avg_wo_outliers'][1:]  #also skip the first one

#plt.scatter(x, y, color='blue', marker='x')

#plt.xlabel('Number of posts')
#plt.ylabel('Average Post Complexity')

#plt.show()