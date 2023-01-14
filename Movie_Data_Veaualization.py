import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Import data
data = pd.read_csv("D:/DEAP Mini Project/IMDB mini proj/IMDB_Updated.csv")
df=pd.DataFrame(data)

#info
df.info()

#num of rows and cols
print('Rows:',df.shape[0])
print('Columns: ',df.shape[1])

#Display top & bottom 5 rows
print(df.head(5))
print(df.tail(5))
print(df.sample(5))

#Data analysis
print(df.dtypes)
#All columns are object expect rating which is float
#Column names:
print('Column Names:',df.columns.values)
df=df.astype({'title':'string','year':'string','certificate':'string','genre':'string'})

df.rename(columns= {'runtime':'duration'},inplace=True)
print(df.dtypes)
print('Column Names:',df.columns.values)
#delete column decription as it is of no use
del df['desc']
print('Column Names:',df.columns.values)

#FOr missing values(boolean output)
print(df.isnull().values.any())
df.isnull()
print('Null values columnwise')
print(df.isna().sum())
#visualize missing values
print(sns.heatmap(df.isnull()))
##Preprocessing
plt.show()
#Duplicate data
print(df.duplicated().sum())
df.drop_duplicates(inplace=True)
print(df.duplicated().sum())
#df=df.drop_duplicates()

print(df.describe())
""""
#As rows after 8960 does not contain any values for description, ratings and
# votes so we will remove that from our dataset
df=df[df['votes'].notna()]
print(df.isna().sum())

#converting votes to int
df['votes']=df['votes'].str.replace(",","").astype("int")
df['duration']=df['duration'].str.replace("min","")
df['duration'].astype('float')
"""""
#For Year some cells have null value  means movie not release yet so we can drop them.
df = df[df['year'].notna()]
print(df.isna().sum())

df=df[df['votes'].notna()]
print(df.isna().sum())

#Clean Year column
print('old',df['year'].value_counts())
df['year']=df['year'].str[-4:]
print('\nnew',df['year'].value_counts())
df=df[df.year != 'IV']
df=df[df.year != 'V']
df=df[df.year != 'XIV']
print('\nnew',df['year'].value_counts())

#cleaning certificate data converting into less number of values
print('old',df['certificate'].value_counts())
df['certificate']=df['certificate'].replace(['16+','U/A 16+'],['UA 16+','UA 16+'])
df['certificate']=df['certificate'].replace(['18','18+'],['A','A'])
df['certificate']=df['certificate'].replace(['Unrated'],['Not Rated'])
df['certificate']=df['certificate'].replace(['7','7+'],['UA 7+','UA 7+'])
df['certificate']=df['certificate'].replace(['13','13+','12+'],['UA 13+','UA 13+','UA 13+'])
df['certificate']=df['certificate'].replace(['16'],['UA 16+'])
df['certificate']=df['certificate'].replace(['15','15+'],['UA 16+','UA 16+'])
df['certificate']=df['certificate'].replace(['U/A'],['UA'])
df['certificate']=df['certificate'].replace(['3+'],['PG'])
df['certificate']=df['certificate'].replace(['All'],['U'])
print('\nnew\n',df['certificate'].value_counts())


## MISSING VALUES FILLING TECH
#DURATION: calulate average movie duration
df['duration']=df['duration'].replace(" min","", regex=True)
df['duration']=pd.to_numeric(df['duration'])
avgdur= df['duration'].mean()
print(avgdur)

df['duration'].fillna(avgdur,inplace = True)
print(df.isna().sum())


#GENRE
print(df['genre'].value_counts())
print(df['genre'].isna().sum())


s1 = df.query("certificate == 'UA 16+'")["genre"]
df1 = pd.DataFrame(s1)
print(df1.head())
print(list(df1.columns))
print(df1['genre'].value_counts())


# here we have some rows of genre which are null so we replace them comparing with certificate
print("before \n",df['genre'].isna().sum())
df.loc[df["certificate"] == "A", "genre"] = 'Horror, Crime, Drama'
#df = df[df['certificate'].notna()]
print(df.isna().sum())

print("before \n",df['genre'].isna().sum())
df.loc[df["certificate"] == "UA", "genre"] = 'Action, Drama, Romance'
#df = df[df['certificate'].notna()]
print(df.isna().sum())

print("before \n",df['genre'].isna().sum())
df.loc[df["certificate"] == "U", "genre"] = 'Comedy, Drama, Mystery'
#df = df[df['certificate'].notna()]
print(df.isna().sum())

print("before \n",df['genre'].isna().sum())
df.loc[df["certificate"].isna(), "genre"] = 'Comedy, Drama'
#df = df[df['certificate'].notna()]
print(df.isna().sum())
"""""
"""""
# after filling genre value we still have some null value in genre as certificate dont have any value so we drop them
print("After\n",df['genre'].isna().sum())
df = df[df['genre'].notna()]
print("After\n",df['genre'].isna().sum())

gkk = df.groupby(['certificate','genre'])
print(gkk.first())

print(df.isna().sum())

df.loc[df["certificate"].isna() , "certificate"] = 'NotRated'
print(df['certificate'].isna().sum())
print(df.isna().sum())

#VISUALIZATION

df1=df[df['year']=='2022']
df1[['rating','title']].groupby('rating').count().plot(kind='bar', title='rating')
plt.xlabel('rating')
plt.ylabel('No of movies')
#plt.scatter(df['rating'],df['votes'])
plt.show()


#visualise relationship between content rating and duration
df1=df[df['year']=='2022']
df1.boxplot(column='duration',by='rating')
plt.show()

#Correlation between rating and votes:


print(df['rating'].corr(df['votes']))
#Output: 0.07527249061605838 here we have relation lies between -1 to 1 as value comes positive here we have positive correlation

#Correlation between votes rating duration
plt.figure(figsize=(12,10))
plt.title('Correlation of Movie Features',fontsize = 18, color='#333d29')
sns.heatmap(df.corr(),annot=True, cmap=['#004346','#036666','#06837f','#02cecb','#b4ffff','#f8e16c','#fed181'])

plt.figure()
sns.countplot(x='certificate', order = df['certificate'].value_counts().index[0:-1],palette =['#f5c518', '#121212','#8b8b8b'],data = df)
plt.show()

plt.figure()
sns.countplot(x='rating',palette =['#f5c518', '#121212','#8b8b8b'], data = df)
plt.show()

plt.figure()
sns.countplot(x='certificate',hue='rating',order = df['certificate'].value_counts().index[0:-1],palette ='mako', data = df)
plt.show()

plt.figure()
sns.countplot(x='year',data=df,palette =['#f5c518', '#121212','#8b8b8b'], order=df['year'].value_counts().index[0:15])
plt.show()

genres_list = []
for i in df['genre']:
    genres_list.extend(i.split(','))

fig, axes = plt.subplots(nrows=1, ncols=2)

df_plot = pd.DataFrame(Counter(genres_list).most_common(5), columns=['genre', 'total'])
ax = sns.barplot(data=df_plot, x='genre', y='total', ax=axes[0], palette=['#06837f', '#02cecb', '#b4ffff', '#f8e16c', '#fed811'])
ax.set_title('Top 5 Genres in Movies', fontsize=18, weight=600, color='#333d29')
sns.despine()

df_plot_full = pd.DataFrame([Counter(genres_list)]).transpose().sort_values(by=0, ascending=False)
df_plot.loc[len(df_plot)] = {'genre': 'Others', 'total':df_plot_full[6:].sum()[0]}
plt.title('Percentage Ratio of Movie Genres', fontsize=18, weight=600, color='#333d29')
wedges, texts, autotexts = axes[1].pie(x=df_plot['total'], labels=df_plot['genre'], autopct='%.2f%%',
                                       textprops=dict(fontsize=14), explode=[0,0,0,0,0,0.1], colors=['#06837f', '#02cecb', '#b4ffff', '#f8e16c', '#fed811', '#fdc100'])

for autotext in autotexts:
    autotext.set_color('#1c2541')
    autotext.set_weight('bold')

axes[1].axis('off')
