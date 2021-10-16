import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
#table = pd.read_csv("ted_main.txt")

"""
A class used to represent a TED talks dataset Analyzer.
full information about TED talks dataset here: https://www.kaggle.com/rounakbanik/ted-talks.
"""
class TedAnalyzer:
    """
    Constructor for TedAnalyzer class.
    param file_path: file that contains the data
    """
    def __init__(self,file_path):
        self.data = pd.read_csv(file_path) 
    
    """
    Method that returns a copy of the data attribute.
    """   
    def get_data(self):
        return pd.DataFrame.copy(self.data)
    
    """
    Method that returns a tuple holding the shape of the data attribute.
    """   
    def get_data_shape(self):
        return self.data.shape
    
    """
    Method that returns a Dataframe object that contains a
    copy of the top n rows from the data attribute, that has the highest values in the
    column_name column.
    param column_name: lst name of one culumn in the table
    param n: int number of the top n rows
    """   
    def get_top_n_by_col(self,column_name,n):
        if n > len(self.get_data()):
            return self.get_data().nlargest(n,column_name)
        return self.get_data().nlargest(n,column_name)
    
    """
    Method that returns a list of the unique values in the column column_name.
    param column_name: lst name of one culumn in the table
    """   
    def get_unique_values_as_list(self,column_name):
        return self.data[column_name].unique().tolist()
    
    """
    Method that returns a dictionary of the unique value in column column_name as keys
    and the number of rows they appear in as values.
    param column_name: lst name of one culumn in the table
    """   
    def get_unique_values_as_dict(self,column_name):
        unique_count = self.data[column_name].value_counts() #returns the unique values and number of rows they appear
        return unique_count.to_dict() 
      
    """
    Method that return a Series object with counts of the null values in each column.
    """      
    def get_na_counts(self):
        return self.data.isnull().sum()
        
    """
    Method that returns a copy of the data attribute with all the rows that contain at least one null value.
    """   
    def get_all_na(self):
        return self.get_data()[self.get_data().isnull().any(axis=1)]
    """
    Method that removes all rows that contain at least a single column with null value
    from the data attribute and resets the index of the result DataFrame. 
    """   
    def drop_na(self):
        
        self.data = self.data.dropna().reset_index()
        
    """
    Method that returns a list of all the unique strings from the “tags” column.
    """   
    def get_unique_tags(self):
        tags_list = self.data['tags'].tolist() 
        unique_tags_list = []
        for string in tags_list:
             for val in ast.literal_eval(string):
                 if val not in unique_tags_list: 
                     unique_tags_list.append(val) 
        return unique_tags_list
    
    """
    Method that  adds a new column called
    new_column_name to the data attribute that shows the “duration” value in minutes
    instead of seconds.
    param new_column_name: lst name of new culumn in the table
    """   
    def add_duration_in_minutes(self,new_column_name):
        self.data[new_column_name] = (self.data['duration']/60).astype('int64')
        
    """
    Method that returns a subset of the data attribute with
    all the rows that their column_name values exceed the threshold.
    param column_name: lst name of one culumn in the table
    param treshold: int number
    """     
    def filter_by_row(self,column_name,treshold):
        df = self.data
        return df[df[column_name] > treshold].dropna()


    """
    Method to convert the Unix timestamps into a human readable format.
    """
    def convert_unix_to_datetime(self):
        self.data['film_date'] = self.data['film_date'].apply(lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%d-%m-%Y'))
        self.data['published_date'] = self.data['published_date'].apply(
            lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%d-%m-%Y'))
    """
    Method that parse the rating_x data of each TED Talk and adds a new column for rating_x data 
    param rating_x: specific rating from the ratings can be given by TED talks viewers
    """
    def parse_rating(self, rating_x):
        rate = []
        data = self.data
        # Loop over all talks in dataframe
        for ll in range(len(data)):
            # First we split on the rating of interest and subsequent splits work to isolate the rating counts
            splitting = data['ratings'][ll].split(rating_x)
            splitting2 = splitting[1].split(':')
            splitting3 = splitting2[1].split(" ")
            splitting4 = splitting3[1].split("}")
            # Isolate number of ratings
            rate.append(splitting4[0])
            series = pd.Series(rate)
            # Create column in dataframe for rating
            data[rating_x] = series

    # list of all ratings
    ratings = ['Funny', 'Beautiful', 'Ingenious', 'Courageous', 'Longwinded', 'Confusing',
               'Informative', 'Fascinating', 'Unconvincing', 'Persuasive', 'Jaw-dropping', 'OK',
               'Obnoxious', 'Inspiring']
    """
    Method that adds cols for all possible ratings
    param ratings: list of all possible ratings
    """
    def add_rating_cols(self, ratings):
        for rating in ratings:
            self.parse_rating(rating)
        return self.data[ratings]

    # Categorize the ratings into the three broad categories
    positive = ['Funny', 'Beautiful', 'Ingenious', 'Courageous', 'Inspiring', 'Jaw-dropping', 'Fascinating']
    negative = ['Longwinded', 'Unconvincing', 'Obnoxious', 'Confusing']
    moderate = ['Informative', 'OK', 'Persuasive']
    """
    Method that adds new cols to the data for each category of t he ratings: positive, negative, moderate. 
    And sum the ratings appropriately
    param ratings: list of all possible ratings
    """
    def count_ratings_by_category(self, ratings):
        #Convert ratings from string to integers so we can use mathematical operations
        self.data[ratings] = self.data[ratings].astype(int)
        #Create new columns that sum the ratings appropriately
        self.data['Positive'] = self.data['Informative'] + self.data['Persuasive'] + self.data['Funny'] + self.data['Beautiful'] + self.data['Ingenious'] + self.data['Courageous'] + self.data['Inspiring'] + self.data['Jaw-dropping'] + self.data['Fascinating']
        self.data['Moderate'] = self.data['OK']
        self.data['Negative'] = self.data['Longwinded'] + self.data['Unconvincing'] + self.data['Obnoxious'] + self.data['Confusing']

    """
     Method that describe statistics for each category: count, mean, std, min, 25%, 50%, 75%, max
     """
    def describe_category_statistics(self):
        return self.data[['Positive', 'Moderate', 'Negative']].describe()


    def mean_views_related_talks(self):
        self.data['related_views'] = 0
        for ii in range(len(self.data)):
            # Remove string
            less = ast.literal_eval(self.data['related_talks'][ii])
            related_views = []
            for ll in range(len(less)):
                # Add view counts for each related talk into list
                related_views.append(less[ll]['viewed_count'])
                self.data[['related_views']][ii] = np.mean(related_views)
    """
    Method to check what the 15 most viewed TED talks of all time.
    """
    def fifteen_most_popular_ted_talks(self):
        pop_talks = self.data[['title', 'main_speaker', 'views', 'film_date']].sort_values('views', ascending=False)[:15]
        return pop_talks

    """
    Method that makes a bar chart to visualise these 15 talks in terms of the number of views they garnered.
    """
    def plot_number_of_most_popular_talks(self ,pop_talks):
        pop_talks['abbr'] = pop_talks['main_speaker'].apply(lambda x: x[:3])
        sns.set_style("whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='abbr', y='views', data=pop_talks)
        plt.show()


    """
    Method to visualize the number of TED talks through the years and check if our hunch that they have grown significantly is indeed true.
    """
    def visualize_number_of_ted_talks_through_the_years(self):
        self.convert_unix_to_datetime()
        self.data['year'] = self.data['film_date'].apply(lambda x: x.split('-')[2]) #apply lambda function on each film date that splits the year out
        year_df = pd.DataFrame(self.data['year'].value_counts().reset_index())
        year_df.columns = ['year', 'talks']
        plt.figure(figsize=(18, 5))
        sns.pointplot(x='year', y='talks', data=year_df)
        plt.show()


ratings = ['Funny', 'Beautiful', 'Ingenious', 'Courageous', 'Longwinded', 'Confusing',
           'Informative', 'Fascinating', 'Unconvincing', 'Persuasive', 'Jaw-dropping', 'OK',
           'Obnoxious', 'Inspiring']
test = TedAnalyzer("ted_main.csv")
# test.add_rating_cols(ratings)
# test.count_ratings_by_category(ratings)
# test.mean_views_related_talks()
# print(test.data['related_views'])


pop_talks1 = test.fifteen_most_popular_ted_talks()
# print(pop_talks1)
test.visualize_number_of_ted_talks_through_the_years()