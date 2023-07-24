import pandas as pd 

def preprocess(df_summer,region_df):

    df_summer = df_summer[df_summer['Season']=='Summer']
    df_summer= df_summer.merge(region_df,on = "NOC",how="left")
    df_summer.drop_duplicates(inplace=True)
    df_summer = pd.concat([df_summer,pd.get_dummies(df_summer['Medal'])],axis=1)

    return df_summer

def pre_process(country_host_df):
    temp_df = country_host_df.drop_duplicates(subset= ['Year','Host_country','Host_city'])
    temp_df = temp_df.drop(['Country_Name', 'Country_Code',
       'Gold', 'Silver', 'Bronze'],axis=1)
    
    return temp_df
