"""
directors...
index,name,director
0,Snow White and the Seven Dwarfs,David Hand
1,Pinocchio,Ben Sharpsteen
2,Fantasia,full credits
3,Dumbo,Ben Sharpsteen
4,Bambi,David Hand

movies....
index,movie_title,release_date,genre,MPAA_rating,total_gross,inflation_adjusted_gross
0,Snow White and the Seven Dwarfs,"Dec 21, 1937",Musical,G,"$184,925,485","$5,228,953,251"
1,Pinocchio,"Feb 9, 1940",Adventure,G,"$84,300,000","$2,188,229,052"
2,Fantasia,"Nov 13, 1940",Musical,G,"$83,320,000","$2,187,090,808"
3,Song of the South,"Nov 12, 1946",Adventure,G,"$65,000,000","$1,078,510,579"
"""
import pandas as pd

directors_file = 'Desktop/Python/directors/disney_directors.csv'
movies_file = 'Desktop/Python/directors/disney_movies_total_gross.csv'

# Load the directors and movies CSV file
df_directors = pd.read_csv(directors_file)
df_movies = pd.read_csv(movies_file)

# Display the first few rows
# print(df_directors.head())
# print(df_movies.head())

# Summary statistics for numerical columns
# print(df_directors.describe())
# print(df_movies.describe())


# Check for missing or poorly conditioned data
df_directors.isnull().sum()  # Checking missing values in disney_directors.csv
df_movies.isnull().sum()     # Checking missing values in disney_movies_total_gross.csv


# Handle missing data
# Dropping rows where the 'title' or 'director' is missing in df_directors
directors_df_clean = df_directors.dropna(subset=['name', 'director'])

# Dropping rows where 'movie_title' is missing in df_movies
movies_df_clean = df_movies.dropna(subset=['movie_title'])


# Cleaning the inflation_adjusted_gross column: remove '$' and ',' and convert to numeric
movies_df_clean['inflation_adjusted_gross'] = movies_df_clean['inflation_adjusted_gross'].replace({r'\$': '', ',': ''}, regex=True)

# Convert to numeric, coercing any errors to NaN
movies_df_clean['inflation_adjusted_gross'] = pd.to_numeric(movies_df_clean['inflation_adjusted_gross'], errors='coerce')



# Merging the two dataframes on 'name' and 'movie_title' (case-insensitive merge)
# This assumes that the 'name' in df_directors matches 'movie_title' in df_movies
merged_df = pd.merge(
    directors_df_clean, 
    movies_df_clean, 
    left_on=directors_df_clean['name'].str.lower(), 
    right_on=movies_df_clean['movie_title'].str.lower(),
    how='inner'
)

# print(merged_df.head())

"""

Task 1: Produce a table of directors and the number of titles they directed. 
Preferably order the table from highest number of titles directed to lowest number of titles directed.

"""

print('\n')
print('Task1: directors and the number of titles they directed')
print('\n')

# Group by 'director' and count the number of titles directed
director_movie_count = merged_df.groupby('director').size().reset_index(name='number_of_titles')

# Sort by number of titles in descending order
director_movie_count_sorted = director_movie_count.sort_values(by='number_of_titles', ascending=False)

# Display the final result
print(director_movie_count_sorted)


"""
Task 2: Produce a table of directors showing the total inflation adjusted gross (across all of the movies they directed) 
for each director. Ideally order the table from highest total inflation adjusted gross to lowest and show only the top 5 directors.

"""

print('\n')
print('Task2: directors showing the total inflation adjusted gross')
print('\n')

# Group by 'director' and count the number of titles directed
director_gross_total = merged_df.groupby('director')['inflation_adjusted_gross'].sum().reset_index()

# Sort by number of titles in descending order
director_gross_total = director_gross_total.sort_values(by='inflation_adjusted_gross', ascending=False)

# Format the inflation_adjusted_gross with a dollar sign and commas
director_gross_total['inflation_adjusted_gross'] = director_gross_total['inflation_adjusted_gross'].apply(lambda x: "${:,.2f}".format(x))


# Display the final result
print(director_gross_total)


"""
Task 3: Showing only directors who directed 5 or more titles, 
produce a table of mean inflation adjusted gross by director. 
Ideally, order the table from the highest inflation adjusted gross to lowest.

"""

print('\n')
print('Task3: directors (with 5 title or more) showing the mean inflation adjusted gross ')
print('\n')

# Group by director and calculate the mean inflation_adjusted_gross
directors_mean_gross_df = merged_df.groupby('director')['inflation_adjusted_gross'].mean().reset_index()

# Count the number of titles directed by each director
title_counts = merged_df['director'].value_counts()

# Filter for directors with 5 or more titles
directors_with_5_titles = title_counts[title_counts >= 5].index

# Keep only those directors in the mean DataFrame
directors_mean_gross_df = directors_mean_gross_df[directors_mean_gross_df['director'].isin(directors_with_5_titles)]

# Sort by mean inflation_adjusted_gross in descending order
directors_mean_gross_df = directors_mean_gross_df.sort_values(by='inflation_adjusted_gross', ascending=False)

# Format the inflation_adjusted_gross with a dollar sign and commas
directors_mean_gross_df['inflation_adjusted_gross'] = directors_mean_gross_df['inflation_adjusted_gross'].apply(lambda x: "${:,.2f}".format(x))

# Display the resulting DataFrame
print(directors_mean_gross_df)

