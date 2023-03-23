# Hybrid Recommender System

![recommend system](https://user-images.githubusercontent.com/111612847/227382360-d313512d-8608-4dd1-8b71-3a27dc9d1f65.jpg)

## Business Problem
Make 10 movie suggestions using the item-based and user-based recommendation methods for the user whose ID is given.

## Dataset Story
The dataset was provided by MovieLens, a movie recommendation service. Along with the films in it,
contains ratings. It contains 2,000,0263 ratings across 27,278 movies. This data set is 17 October 2016.
was created on. Includes 138,493 users and data from 09 January 1995 to 31 March 2015. Users
randomly chosen. It is known that all selected users voted for at least 20 movies.

# Variables

Movie
* movieId :	Unique ID assigned to each movie.
* title : 	Name of the movie.
* genres :	Category or genre of the movie.

Rating 
* userid :	Unique ID assigned to each user.
* movieId :	Unique ID assigned to each movie.
* rating	: Rating assigned by the user to the movie (out of 5).
* timestamp :	Date and time when

## Tasks
- User-Based
* Task 1: Data Preparation
* Task 2: Determining the Movies Watched by the User to Suggest
* Task 3: Accessing Data and Ids of Other Users Watching the Same Movies
* Task 4: Identifying Users Who Are Most Similar to the User to Suggest
* Task 5: Calculating the Weighted Average Recommendation Score and Keeping the Top 5 Movies
- Item-based
* Task 1: Make an item-based suggestion based on the last and highest rated movie the user watched.

