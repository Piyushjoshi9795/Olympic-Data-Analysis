import numpy as np

def fetch_medal_tally(df_summer,year,country):
    
    medal_df = df_summer.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    flag = 0

    if year == "Overall" and country  == "Overall":
        temp_df = medal_df
        
    if year == "Overall" and country  != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
        
    if year != "Overall" and country  == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
        
    if year != "Overall" and country  != "Overall":
        temp_df =  medal_df[(medal_df["Year"] == int(year)) & (medal_df["region"] == country)]
    
    if flag == 1:
          x= temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x= temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Total'] = x['Total'].astype(int)
    
    return x


def medal_tally(df_summer):

    medal_tally = df_summer.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]

    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Total'].astype(int)

    return medal_tally


def country_year_list(df_summer):

    year = df_summer["Year"].unique().tolist()
    year.sort()
    year.insert(0,'Overall')

    country = np.unique(df_summer["region"].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return year,country

def data_over_time(df_summer,col):

    nation_over_time = df_summer.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values("index")
    nation_over_time.rename(columns={'index':'Edition','Year':col},inplace=True)

    return nation_over_time


# to get the successful Athele
def most_successful(df_summer,sport):
    temp_df = df_summer.dropna(subset = ['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df_summer,left_on='index',right_on='Name',
                                        how = 'left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'}, inplace = True)
    return x

# year wise medal tally 
def yearwise_medal_tally(df_summer,country):
    temp_df = df_summer.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    
    return final_df

# function for heatmap
def country_event_heatmap(df_summer,country):

    temp_df = df_summer.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    
    pt = new_df.pivot_table(index = 'Sport',columns = 'Year',values='Medal',aggfunc = 'count').fillna(0)

    return pt


# getting data regarding weight vs hight 
def weight_v_hright(df_summer,sport):
    athlete_df = df_summer.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna("NO Medal",inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else :
        return athlete_df
    
# Number of Male and Female Athletes Partisipation over the years
def men_vs_women(df_summer):

    athlete_df = df_summer.drop_duplicates(subset=['Name','region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women =  athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    Final = men.merge(women, on= 'Year',how='left')
    Final.rename(columns= {'Name_x':'Male','Name_y':'Female'},inplace = True)

    Final.fillna(0,inplace=True)
    return Final
