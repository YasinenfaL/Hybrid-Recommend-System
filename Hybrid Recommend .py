################################
# Hybrid Recommender System
################################


###############################
# User Based Recommendation
###############################


# Libraries
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

###################################
# Task 1: Data Preparation
###################################

# Step 1: Read movie, rating datasets.
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')

# Step 2: Add the movie names and genre of the Ids to the rating dataset from the movie dataset
df = movie.merge(rating, on="movieId", how="left")
df.head()

# Step 3: Keep the names of the movies with less than 1000 votes in the list
# and subtract from the dataset
movie1 = pd.DataFrame(df["title"].value_counts())
rare_movie = movie1[movie1["title"] <= 1000].index
common_movies = df[~df["title"].isin(rare_movie)]
common_movies.head()

# Step 4: In the index, user IDs, movie names and create a pivot table for the dataframe with ratings as values


user_movies_df = pd.pivot_table(common_movies, index=["userId"], columns=["title"], values="rating")
user_movies_df[5:5]


# Step 5: Functionalize all the operations done

def create_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    df = movie.merge(rating, on="movieId", how="left")
    movie1 = pd.DataFrame(df["title"].value_counts())
    rare_movie = movie1[movie1["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movie)]
    user_movies_df = pd.pivot_table(common_movies, index=["userId"], columns=["title"], values="rating")
    return user_movies_df


user_movies_df1 = create_movie_df()

####################################################
# Task 2: Determining the Movies Watched by the User to Suggest
####################################################

# Step 1: Choose a random user id.

user_id = 28195.0

# Step 2: Create a new dataframe named random user df consisting of observation units of the selected user

user_movies_df.index
random_user_df = user_movies_df[user_movies_df.index == user_id]

# Step 3: Assign the movies that the selected users voted to a list called movies watched

movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()

# alternative
# movie_watch1= [col for col in random_user_df.columns if random_user_df[col].notna().any()]


####################################################
# Task 3: Accessing Data and Ids of Other Users Watching the Same Movies
####################################################

# Step 1: Lines of movies watched by the selected user.
# select from user movie_df and create a new dataframe named movies_watched_df

movies_watched_df = user_movies_df[movies_watched]

# Step 2: Each user carries the information of how many movies the selected user has watched.
# Create a new dataframe named user_movie_count

user_movie_count = movies_watched_df.T.notna().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]

# Step 3: of the movies that the selected user has voted
# Create a list called users_same_movies from the user IDs of those who watch 60 percent or more.

p = len(movies_watched) * 60 / 100

users_same_movies = user_movie_count[user_movie_count["movie_count"] > p]["userId"]
len(users_same_movies)

############################################################################
# Task 4: Identifying Users Most Similar to the User to Suggest
###########################################################################

# Step 1: With the selected user in the user_same_movies list
# filter movies_watched_df dataframe to find similar users ids
# filter the dataframe

df1 = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies.index)],
                 random_user_df[movies_watched]])

df1.shape
df1.nunique()

# Step 2: Create a new corr_df dataframe where users' correlations with each other will be found

corr_df = df1.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.rename(["userıd1", "userıd2"], inplace=True)
corr_df.reset_index(inplace=True)

# Step 3: Highly correlated with the selected user (over 0.65)
# create a new dataframe# named top_users by filtering users

best_users = corr_df[(corr_df["userıd1"] == user_id) & (corr_df["corr"] >= 0.65)][["userıd2", "corr"]]

best_users = best_users.rename(columns={"userıd2": "userId"})

# Step 4: Merge the top users data frame'line with the rating dataset.


rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
best_users = best_users.merge(rating, how="inner", on="userId")
best_users = best_users[best_users["userId"] != user_id]

###############################################################
# Task 5: Calculating the Weighted Average Recommendation Score
###############################################################

# Step 1: Create a new variable named weighted_rating, which is the product of each user's corr and rating

best_users["weighted_average"] = best_users["corr"] * best_users["rating"]

# Step 2: Movie id and all users belonging to each movie
# Create a new dataframe named recommendation_df containing the average value of the weighted ratings.

recommendation_df = best_users.groupby("movieId").agg({"weighted_average": "mean"})

# Step 3: weighted rating in recommendation df
# Select movies greater than 3.5 and sort by weighted rating.

recommendation_df = recommendation_df[recommendation_df["weighted_average"] > 3.5]. \
    sort_values(by="weighted_average", ascending=False)
recommendation_df.reset_index(inplace=True)

# Step 4: fetch movie names from movie dataset and select top 5 movies to recommend

movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
new_df = recommendation_df.merge(movie[["movieId", "title"]])
new_df.head(5)

###############################################
# Item Based Recommendation
##############################################


# Task 1: Make an item-based suggestion based on the last and highest rated movie the user watched.

# Step 1: Read movie, rating datasets.
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

movie = pd.read_csv("datasets/movie_lens_dataset/movie.csv")
rating = pd.read_csv("datasets/the_movies_dataset/ratings.csv")
df = movie.merge(rating, how="left", on="movieId")

# Step 2: Get the id of the movie with the most recent score from the movies that the selected user gave 5 points.

rating[(rating["userId"] == user_id) &
       (rating["rating"] == 5)]. \
    sort_values(by="timestamp", ascending=False)

movie_name = df[df["movieId"] == 3706]["title"].iloc[0]

# Step 3: Created in User based recommendation section
# Filter user movie df dataframe by selected movie id

movie_name = user_movies_df1[movie_name]

# Step 4: Find the correlation of the selected movie with the other movies using the filtered dataframe and rank them.

df_new_movies = user_movies_df1.corrwith(movie_name).sort_values(ascending=False)
df_new_movies = pd.DataFrame(df_new_movies, columns=["corr"])
df_new_movies.reset_index(inplace=True)

# Step 5: Give the first 5 movies as suggestions except the selected movie itself.

df_new_movies.iloc[1:6]
