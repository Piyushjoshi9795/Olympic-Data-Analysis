import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import preprocesser ,helper,analysis_text


# reading the csv files
df  = pd.read_csv("Olympic2.csv")
region_df = pd.read_csv("noc_regions.csv")
host_df = pd.read_csv("Summer_olympic_Medals.csv")

# Cleaning of dataset
df_summer  = preprocesser.preprocess(df,region_df)
country_host_df = preprocesser.pre_process(host_df)


# Side bar section 
st.sidebar.title(":red[Olympics Analysis] ")
st.sidebar.image('https://logos-world.net/wp-content/uploads/2021/09/Olympics-Logo.png')

user_input2 = st.sidebar.radio(
    'Start an Option ',
    ('Home','Start Analysis'),
    )

if user_input2 == 'Home':
    st.title(":blue[_Web Application for Exploratory Data Analysis on Olympics_] ")
    st.markdown("![Alt Text](https://mentalitch.com/wp-content/uploads/2016/08/Interesting-Facts-About-The-Olympics.jpg)")
    analysis = analysis_text.analysis()
    st.title(":blue[_About Project_]")
    st.write(analysis)

#Operation to Start analysis section 
if user_input2 == 'Start Analysis':
# Side bar section 
    user_menu = st.sidebar.radio(
        'Select an Option ',
        ('Hosting Country','Medal Tally','Overall Analysis','Country-wise Analysis',
         'Athlete wise Analysis'),
        key=None
    )
#  To get the name of the list which hosted the different Olympic in Different Year
    if user_menu == 'Hosting Country':
        st.title(':stadium: :blue[List of Olympic Game Host Cities]')
        st.table(country_host_df.style.background_gradient(cmap="Greens"))
        
    # operation for Medal Tally 
    if user_menu == 'Medal Tally' :
        st.sidebar.header("Medal Tally")
        years,country = helper.country_year_list(df_summer)
        selected_year = st.sidebar.selectbox("Select Year",years)
        selected_country = st.sidebar.selectbox("Select Country",country)

        medal_tally = helper.fetch_medal_tally(df_summer,selected_year,selected_country)

        if selected_year == 'Overall' and selected_country == 'Overall':
            st.title(':trophy: :blue[Overall Tally] ')

        if selected_year != 'Overall' and selected_country == 'Overall':
            st.title(':trophy: :blue[Medal tally in ] ' + str(selected_year) + ' :blue[ Olympics]')

        if selected_year == 'Overall' and selected_country != 'Overall':
            st.title(':trophy: '+ selected_country + ' :blue[Overall Performance in Olympics]')

        if selected_year != 'Overall' and selected_country != 'Overall':
            st.title(':trophy: :blue[Performance of ] ' + selected_country + ' :blue[ in ] ' 
                     + str(selected_year) + ' :blue[ Olympics]')

        st.table(medal_tally.style.background_gradient(cmap="Greens"))


    # for Overall Analysis
    if user_menu == 'Overall Analysis':
            edition = df_summer["Year"].unique().shape[0]-1
            cities = df_summer["City"].unique().shape[0]
            sports = df_summer["Sport"].unique().shape[0]
            events = df_summer["Event"].unique().shape[0]
            athletes = df_summer["Name"].unique().shape[0]
            nations = df_summer["region"].unique().shape[0]

            st.title(":blue[Top Statistics]")
            col1,col2,col3 = st.columns(3)
            with col1:
                st.header(":red[_Editions_]")
                st.title(edition)
            with col2:
                st.header(":red[_Hosts_]")
                st.title(cities)
            with col3:
                st.header(":red[_Sports_]")
                st.title(sports)
            
            col1,col2,col3 = st.columns(3)
            with col1:
                st.header(":red[_Events_]")
                st.title(events)
            with col2:
                st.header(":red[_Nations_]")
                st.title(nations)
            with col3:
                st.header(":red[_Athletes_]")
                st.title(athletes)



# Country wise Analysis 
    if user_menu == 'Country-wise Analysis':

        st.sidebar.title(":blue[Country - Wise Analysis]")

        country_list = df_summer['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.sidebar.selectbox("Select a Country ",country_list)

# line plot to show the medal tally over the year
        country_df = helper.yearwise_medal_tally(df_summer,selected_country)
        fig = px.line(country_df, x ='Year',y = 'Medal')
        st.title(selected_country + " :blue[Medal Tally Over the Year]")
        st.plotly_chart(fig)

# heatmap to ploat Excels in different sports
        st.title(selected_country + ' :blue[Excels in the following sports]')
        pt = helper.country_event_heatmap(df_summer,selected_country)
        fig,ax = plt.subplots(figsize = (20,20))
        ax = sns.heatmap(pt,annot = True)
        st.pyplot(fig)

# Analysis according to Athlete wise 
    if user_menu == 'Athlete wise Analysis':
        athlete_df = df_summer.drop_duplicates(subset=['Name','region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

# ploting probability distribution function w.r.t age and medal
        fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist',
                                            'silver Medalist','Bronze Medalist'],show_rug= False,show_hist=False)
        fig.update_layout(autosize = False,width = 800, height = 600)
        st.title(":blue[Distribution of Age]")
        st.plotly_chart(fig)
# Distribution of Medal over age 
        x = []
        name = []
        famous_sport = ['Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming',
                        'Badminton','Sailing','Gymnastics','Art Competitions','Handball',
                        'Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing',
                        'Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis',
                        'Golf','Softball','Archery','Volleyball','Synchronized Swimming',
                        'Table Tennis','Rhythmic Gymnastics','Rugby Sevens',
                        'Beach Volleyball','Triathlon', 'Polo','Ice Hockey'
                        ]
        
        st.sidebar.title(":blue[Distribution of Medal over Age]")
        user_menu1 = st.sidebar.radio(
            'Select an Option ',
            ('Gold','Silver','Bronze')
        )

        for sport in famous_sport:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == user_menu1]['Age'].dropna())
            name.append(sport)
        
        fig = ff.create_distplot(x, name,show_hist=False,show_rug=False)
        fig.update_layout(autosize = False,width = 800, height = 600)
        st.title(":blue[Distribution of Age wrt Sports ] " + (user_menu1) + ':sports_medal:')
        st.plotly_chart(fig)

# Scatterplot for winning medal over hight vs weight
        sport_list = df_summer['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        st.title(':blue[Height vs Weight]')
        selected_sport = st.selectbox("Select a Sport ",sport_list)
        temp_df = helper.weight_v_hright(df_summer,selected_sport)
        fig,ax = plt.subplots()
        ax = sns.scatterplot(temp_df, x="Weight", y="Height",hue='Medal',style='Sex',s=80)
        
        st.pyplot(fig)

# Number of Male and Female Athletes Partisipation over the years
        st.title(':blue[Men Vs Women Participation Over the Years]')
        final = helper.men_vs_women(df_summer)
        fig = px.line(final,x='Year',y=['Male','Female'])
        st.plotly_chart(fig)


