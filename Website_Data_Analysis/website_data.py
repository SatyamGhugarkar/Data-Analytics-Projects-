#################################################################################################################################
#   import python libraries
# 
#  Auther :      Satyam Ghugarkar
#  Date :         23/10/2025  Required Python Packages
#################################################################################################################################
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 

################################################################################################################################# 
#  Description:   What patterns or trends can you observe in website sessions and users over time?
#  Auther :       Satyam Ghugarkar
#  Date :         23/10/2025   File Path 
#################################################################################################################################

df = pd.read_csv("data-export.csv")
print(df.head())

##################################################################################################################################
#     Headers
###################################################################################################################################

df.columns = df.iloc[0]
df= df.drop(index = 0).reset_index(drop = True)
df.columns = ["Channel group","Datehour","Users","Sessions","Engaged Sessions","Average engagement","Engaged sessions per user","Events","Engagement rate","Event count"]

##################################################################################################################################
#  function name: data_cleaning 
#  Description:   cleaning data and data visulization for the above set 
#  Auther :       Satyam Ghugarkar
#  Date :         23/10/2025  
##################################################################################################################################
def data_cleaning():
    
    df["Datehour"] = pd.to_datetime(df["Datehour"], format = "%Y%m%d%H",errors="coerce")

    numeric_cols = df.columns.drop(["Channel group","Datehour"])
    df[numeric_cols]= df[numeric_cols].apply(pd.to_numeric, errors= "coerce")
    df["Hour"]= df["Datehour"].dt.hour

    print(df.head())
    print(df.info())
    print(df.describe())

#####################################################################################################################################
#  function name :  sessions_and_user
#    Description :  Traffic by Hour Channel 
#       Question :  1.At what hours of the day does each channel drive the most traffic?
#         Auther :  Satyam Ghugarkar
#           Date :  23/10/2025
#####################################################################################################################################
def sessions_and_user():

    sns.set(style="whitegrid")
    plt.figure(figsize=(10,5))
    df.groupby("Datehour")[["Sessions", "Users"]].sum().plot(ax=plt.gca())
    plt.title("Sessions and users over time")
    plt.xlabel("Datehour")
    plt.ylabel(" Count")
    plt.show()


##################################################################################################################################################
###function name :  total_users()
#    Description :  TOTAL USERS BY CHANNEL
#       Question :  2.Which marketing channel brought the highest number of users to the website, and how can we use this insight to improve traffic from other sources?
#         Auther :  Satyam Ghugarkar
#           Date :  23/10/2025    
###################################################################################################################################################
def total_users():

    plt.figure(figsize=(10,5))
    sns.barplot(data= df , x = "Channel group", y = "Users", estimator= np.sum, palette="viridis")
    plt.title("total users by channel ")
    plt.xticks(rotation=69)
    plt.show()

   


#####################################################################################################################################################
### function name :  sessions_and_use 
#    Description :  Traffic by Hour Channel 
#       Question :  3. At what hours of the day does each channel drive the most traffic?
#         Auther :  Satyam Ghugarkar
#           Date :   23/10/2025   3. AVERAGE ENGAGEMENT TIME BY CHANNEL 
# Which channel has the highest average engagement time, and what does that tell us about user behavior and content effectiveness?
#########################################################################################################################################################
def avg_engagement_time():
        
    plt.figure(figsize=(10,5))
    sns.barplot(data=df , x = "Channel group" , y = "Average engagement", estimator= np.mean , palette="magma")
    plt.title(" Avg Engagement time  by channel")
    plt.xticks(rotation=45)
    plt.show

  

####################################################################################################################################################
#  function name : engagement_rate() 
#    Description :  Traffic by Hour Channel 
#       Question :  4. How does engagement rate vary across different traffic channels?
#         Auther : Satyam Ghugarkar
#           Date :  23/10/2025 
#	
################################################################################################################################################

def engagement_rate():

    plt.figure(figsize=(10,5))
    sns.boxplot(data = df , x = "Channel group", y= "Engagement rate",palette= "coolwarm")
    plt.title("Enagagement rate distribution by channel")
    plt.xticks(rotation = 45 )
    plt.show()



####################################################################################################################################################################
#  function name :  eng_vs_noneng()
#    Description :  ENGAGED VS NON ENGAGED 
#       Question :  5. Which channels are driving more engaged sessions compared to non-engaged ones, and what strategies can improve engagement in underperforming channels?
#         Auther :  Satyam Ghugarkar
#           Date :    23/10/2025 
#######################################################################################################################################################


def eng_vs_noneng():
        
    Sessions_df = df.groupby("Channel group")[["Sessions", "Engaged Sessions"]].sum().reset_index()

    # Create Non-Engaged column
    Sessions_df["Non-Engaged"] = Sessions_df["Sessions"] - Sessions_df["Engaged Sessions"]

    # Melt dataframe
    Sessions_df_melted = Sessions_df.melt(
        id_vars="Channel group",   # fixed: removed trailing space
        value_vars=["Engaged Sessions", "Non-Engaged"],  # fixed: corrected spelling
        var_name="Session type",
        value_name="Count"
    )

    print(Sessions_df_melted.head())


    plt.figure(figsize=(10,5))
    sns.barplot(
        data=Sessions_df_melted,
        x="Channel group",          # fixed: removed extra space
        y="Count",                  # fixed: use the correct column name from melt
        hue="Session type"          # fixed: use the column created by melt
    )
    plt.title("Engaged vs Non-Engaged Sessions")
    plt.xticks(rotation=45)
    plt.show()


#########################################################################################################################################################
#  function name :  traffic_hour() 
#    Description :  Traffic by Hour Channel 
#       Question :  6. At what hours of the day does each channel drive the most traffic?
#         Auther :  Satyam Ghugarkar
#           Date :   23/10/2025 
#########################################################################################################################################################

def traffic_hour():

    heatmap_data= df.groupby(["Hour", "Channel group"])["Sessions"].sum().unstack().fillna(0)

    plt.figure(figsize=(10,5))
    sns.heatmap(heatmap_data, cmap="YlGnBu", linewidth=.5, annot=True , fmt = ".0f")
    plt.title("traffic by hour and channel")
    plt.xlabel("channel group")
    plt.ylabel("hour of day")
    plt.show()



#########################################################################################################################################################
# function name :   eng_vs_session()
#   Description :   Enageged rate vs sessions over time 
#      Question :   7. Is there any correlation between high traffic(sessions) and high engagement rate over the time?
#        Auther :   Satyam Ghugarkar
#          Date :   23/10/2025 
#########################################################################################################################################################

def eng_vs_session():

    df_plot = df.groupby("Datehour")[[ "Engagement rate","Sessions"]].mean().reset_index()

    plt.figure(figsize=(10,5))
    plt.plot(df_plot['Datehour'], df_plot["Engagement rate"], label= "Engagement rate", color="green")
    plt.plot(df_plot['Datehour'], df_plot["Sessions"], label ="Sessions" , color = "blue")
    plt.title("engagement rate vss sessions over time")
    plt.xlabel("Datehour")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
   
   data_cleaning()
    
   sessions_and_user()
   total_users()
   avg_engagement_time()
   engagement_rate()
   eng_vs_noneng()
   traffic_hour()
   eng_vs_session()



if __name__ == "__main__":
    main()


