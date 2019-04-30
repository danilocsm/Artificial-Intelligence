import os
import pandas as pd 

def min_max_normalization(dataframe, column):

    def apply_min_max(value):

        new_value = (value - min_value) / (max_value - min_value)
        return new_value
    
    min_value = dataframe[column].min()
    max_value = dataframe[column].max()
    dataframe[column] = dataframe[column].apply(apply_min_max)

    return dataframe

def map_categorical_to_discrete_values(dataframe, column):
     
    def aux_map_function(value):

        return values_dic[value]
    
    unique_values = dataframe[column].unique()
    values_dic = dict(zip(unique_values,range(len(unique_values))))
    dataframe[column] = dataframe[column].apply(aux_map_function)

    return dataframe
   
def remove_missing_values(dataframe):

    workclass_mode = dataframe['workclass'].mode()[0]
    occupation_mode = dataframe['occupation'].mode()[0]
    dataframe['workclass'].replace(' ?', workclass_mode, inplace=True)
    dataframe['occupation'].replace(' ?', occupation_mode, inplace=True)

    return dataframe

def get_means(bins):

    means = []
    for i in range(len(bins)-1):
        mean = (bins[i]+bins[i+1]) // 2
        means.append(mean)
    
    return means

def discrete_ages(dataframe):
    
    def discretize_age_into_interval_mean(age):
        
        for mean, interval in interval_mean_dic.items():
            if age in interval:
                return mean

    max_age = dataframe['age'].max()
    min_age = dataframe['age'].min()
    bin_size = int((max_age - min_age) / 10)
    age_bins = list(range(min_age, max_age+1, bin_size))
    bins_mean = get_means(age_bins)
    ages = dataframe['age'].values
    intervals = pd.cut(ages, age_bins, include_lowest=True, right=False)
    interval_mean_dic = dict(zip(bins_mean,intervals.categories))
    dataframe['age'] = dataframe['age'].apply(discretize_age_into_interval_mean)

    return dataframe

def preprocess_data(dataframe):
    
    categorical_features = ['sex','workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'incoming']
    
    # removing missing values in workclass and occupation columns
    dataframe = remove_missing_values(dataframe)

    # discretizing the age attribute into the means of the bins created
    dataframe = discrete_ages(dataframe)

    # encoding all categorical features of the dataset
    for feature in categorical_features:
        dataframe = map_categorical_to_discrete_values(dataframe, feature)

    # dropping the column that won't be used in the training step
    dataframe.drop(['native-country'], axis=1, inplace=True)

    # normalizing all data with the min_max algorithm (range[0,1])
    columns = dataframe.columns
    for column in columns:
        dataframe = min_max_normalization(dataframe, column)

    return dataframe 

if __name__ == "__main__":
    
    dataset_dir = '/home/danilocrgm/Documents/datasets/adults-dataset/adult.csv'
    raw_dataframe = pd.read_csv(dataset_dir)

    # pre processing the data
    print("Original dataset")
    print(raw_dataframe.head(),"\n")
    new_dataframe = preprocess_data(raw_dataframe)
    print("Pre-processed dataset")
    print(new_dataframe.head())
    save_path = os.getcwd() + '/' + 'pre_processed_data.csv'
    if not os.path.isfile(save_path):
        new_dataframe.to_csv(save_path)