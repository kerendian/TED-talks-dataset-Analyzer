import pandas as pd
import ast

table = pd.read_csv("ted_main.txt") 

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
    






