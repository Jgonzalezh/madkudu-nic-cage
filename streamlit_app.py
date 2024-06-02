import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.balloons()
st.markdown("# Nicolas Cage Data App")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.write("Glad you are here ✨. In this app, we will review some of the findings in the data about Nicolas Cage movies"
         )
st.markdown("## Basic Data about Nic Cage movies")
st.write("Cage movies are a little bit worse rated than other movies, as you can see in Rating a Metascore. Nevertheless, they get more reviews than other average films and they pretty regular in duration.")
df=pd.read_csv('imdb-movies-dataset.csv')
df.drop_duplicates(inplace=True)
df.drop(columns=['Poster'], inplace=True)
#st.write(df.head(5))
#st.write(df.dtypes)
df['Metascore'] = pd.to_numeric(df['Metascore'], errors='coerce')
df['Review Count'] = pd.to_numeric(df['Review Count'], errors='coerce')
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')
df['Year'] = df['Year'].astype(str)
# Replace NaN values with a default year (e.g., 1900)
default_year = '1900'
df['Year'] = df['Year'].replace('nan', '1900')
df['Year'].fillna(default_year, inplace=True)
# Extract year from the string and convert it to integer
df['Year'] = df['Year'].str.split('.').str[0].astype(int)
# Now convert 'Year' column to datetime with year only
df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year
# Print data types to confirm the change
#st.write(df.dtypes)

def has_nicolas_cage(cast_value):
    if isinstance(cast_value, str) and 'Nicolas Cage' in cast_value:
        return 1
    else:
        return 0

# Apply the custom function to create the 'Cage Movie' column
df['Cage Movie'] = df['Cast'].apply(has_nicolas_cage)

numeric_columns = ['Rating', 'Metascore', 'Review Count', 'Duration (min)']
for column in numeric_columns:
    # Calculate statistics by 'Cage Movie'
    stats_by_cage_movie = df.groupby('Cage Movie')[column].agg(['min', 'max', 'mean', 'median'])
    st.write(column, stats_by_cage_movie)

# Calculate the correlation matrix
correlation_matrix = df[numeric_columns].corr()

st.write("We can see a high correlation between the Metascore and the Rating")

# Print correlation matrix
st.write("Correlation Matrix:")
st.write(correlation_matrix)

st.markdown("## Insights about Nic Cage filmography")
st.write("Nicol Cage has done more Romance and Drama movies.")

avg_ratings = {}
movie_counts = {}
df.dropna(subset=['Genre'], inplace=True)
# Create a list of unique categories
all_categories = ','.join(df['Genre'])
categories_list = all_categories.split(',')
unique_categories = list(set(categories_list))

for category in unique_categories:
    category_df = df[(df['Genre'].str.replace(' ', '').str.contains(category)) & (df['Cage Movie'] == 1)]
    count = len(category_df)
    if count >= 3:  # Check if count is at least 3
        avg_rating = category_df['Rating'].mean()
        avg_ratings[category] = avg_rating
        movie_counts[category] = count

# Sort categories based on average ratings in descending order
sorted_categories = sorted(avg_ratings, key=avg_ratings.get, reverse=True)

# Plot the average rating for each category where 'Cage Movie' is equal to 1 and count >= 3
plt.figure(figsize=(12, 6))
plt.bar(sorted_categories, [avg_ratings[category] for category in sorted_categories], color='skyblue')

plt.title('Average Rating by Genre for Cage Movies (Count >= 3)')
plt.xlabel('Genre')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt.show())
st.write("Let's check the performance")


# Create lists to store movie counts and average ratings
movie_counts = {}
avg_ratings = {}
# Create a list of unique categories
all_categories = ','.join(df['Genre'])
categories_list = all_categories.split(',')
unique_categories = list(set(categories_list))
# Drop rows with NaN values in 'Genre' column
df.dropna(subset=['Genre'], inplace=True)

# Iterate over unique categories to calculate movie counts and average ratings
for category in unique_categories:
    category_df = df[(df['Genre'].str.replace(' ', '').str.contains(category)) & (df['Cage Movie'] == 1)]
    count = len(category_df)
    if count >= 3:  # Check if count is at least 3
        avg_rating = category_df['Rating'].mean()
        avg_ratings[category] = avg_rating
        movie_counts[category] = count

# Sort categories based on movie counts in descending order
sorted_categories = sorted(movie_counts, key=movie_counts.get, reverse=True)

# Create lists for bar chart
genres = []
counts = []
for category in sorted_categories:
    genres.append(category)
    counts.append(movie_counts[category])

# Plot the number of movies per genre
plt.figure(figsize=(12, 6))
plt.bar(genres, counts, color='skyblue')
plt.title('Number of Movies per Genre for Cage Movies (Count >= 3)')
plt.xlabel('Genre')
plt.ylabel('Number of Movies')
plt.xticks(rotation=45)

# Add a trend line for average ratings
plt.plot(sorted_categories, [avg_ratings[category] for category in sorted_categories], marker='o', color='red', label='Average Rating')
plt.legend()

plt.tight_layout()
st.pyplot(plt.show())
st.write("Nicol Cage has done more Romance and Drama movies.")
st.markdown("## Nic Cage co-workers")

st.write("He is not very repetitive, most of his co-cast never found themselves again. Here are some examples")
#st.write("Charing Cast: average rating and film together")

# Convert 'Cast' column to strings
df['Cast'] = df['Cast'].astype(str)

# Drop rows with NaN values in 'Cast' column
df.dropna(subset=['Cast'], inplace=True)

# Exclude 'Nicolas Cage' from the list of co-stars
all_co_stars = ','.join(df['Cast'].str.replace('Nicolas Cage', '').str.replace(', ', ','))
co_stars_list = all_co_stars.split(',')
unique_co_stars = list(set(co_stars_list))

# Initialize dictionary to store average ratings for each co-star
avg_ratings = {}
counts = {}


for co_star in unique_co_stars:
    co_star_df = df[(df['Cast'].str.contains(co_star)) & (df['Cage Movie'] == 1)]
    count = len(co_star_df)
    avg_rating = co_star_df['Rating'].mean()
    count = co_star_df['Rating'].count()
    if avg_rating is not None:  # Check if average rating is not None
        avg_ratings[co_star] = avg_rating
        counts[co_star]= count

# Sort co-stars based on average ratings in descending order
#sorted_co_stars = sorted(avg_ratings, key=avg_ratings.get, reverse=True)
sorted_co_stars = sorted(avg_ratings, key=lambda x: avg_ratings[x] if not pd.isnull(avg_ratings[x]) else float('-inf'), reverse=True)

# Filter out co-stars with NaN average ratings and counts less than 2
filtered_avg_ratings = {co_star: avg_ratings[co_star] for co_star in avg_ratings if not pd.isnull(avg_ratings[co_star]) and counts[co_star] > 1 and len(co_star) > 1}
filtered_counts = {co_star: counts[co_star] for co_star in counts if co_star in filtered_avg_ratings}

# Sort co-stars based on average ratings in descending order
sorted_co_stars = sorted(filtered_avg_ratings, key=filtered_avg_ratings.get, reverse=True)

# Plot the average ratings for each co-star
plt.figure(figsize=(12, 6))
plt.bar(sorted_co_stars, [filtered_avg_ratings[co_star] for co_star in sorted_co_stars], color='skyblue')

plt.title('Average Rating by Co-star for Cage Movies (Count > 1)')
plt.xlabel('Co-star')
plt.ylabel('Average Rating')
plt.xticks(rotation=90)
plt.tight_layout()
st.pyplot(plt.show())
st.write("I would definitively pair him with John Goodman, Ryan Reynolds Catherine Goodman")
st.markdown("## In how many movies has N.C. acted? ")


actor_movie_count = {}

# Iterate over each row in the DataFrame
for cast_list in df['Cast']:
    # Split the cast list into individual actors
    actors = cast_list.split(', ')
    # Iterate over each actor
    for actor in actors:
        # Increment the count for the current actor
        actor_movie_count[actor] = actor_movie_count.get(actor, 0) + 1

# Sort the dictionary based on the count of movies in descending order
sorted_actor_movie_count = dict(sorted(actor_movie_count.items(), key=lambda x: x[1], reverse=True))

# Print the count of movies for each actor in descending order
counting=0
for actor, count in sorted_actor_movie_count.items():
    st.write(f"{actor}: {count} movies")
    counting+=1
    if counting>3:
        break
st.write("Way more than those other giants from the industry")
st.markdown("## Fun Facts")
st.write("In 2014 he made 8 movies! And he has worked the most with John Turteltaub as a director with a pretty good result.")
st.markdown("# Summary")
st.write("Nicolas Cage has made a tremendous amount of films, a little below the average in rating. He usually doesn't repeat his co-actors and directors. If you need to choose a film from Nic Cage I would recommend Drama as a subject.")

