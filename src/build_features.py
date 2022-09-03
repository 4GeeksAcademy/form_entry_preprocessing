import pandas as pd
import numpy as np

#PREPROCESSING FUNCTIONS

def change_to_datetime(df,column):
    df[column] = df[column].apply(pd.to_datetime).copy()
    return df

def change_format(df,column):
    df[column] = df[column].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

def combine_columns(df, column1, column2, new_column):
    df[new_column] = df[column1].fillna('') + str(' ') + df[column2].fillna('')   
    return df

def drop_null_columns(df):
    df.dropna(axis=1, how='all', inplace=True)  
    return df

def drop_test_rows(df):
    df = df[df["email"].str.contains("@4geeks") == False]
    return df

def remove_duplicates(df):
    print('shape before combining duplicates: ', df.shape)
    df = df.replace("Nan", np.nan).copy()
    df = df.sort_values("created_at").copy()
    df = df.groupby("email").first().reset_index()
    print('shape after combining duplicates: ', df.shape)
    return df
    
def clean_course(df,column):
    df[column] = df[column].replace(['full-stack-ft', 'full_stack', 'full-stack,software-engineering',
                                    'coding-introduction','outcomes'], 'full-stack')
    df[column] = df[column].replace(['machine-learning', 'machine-learning-enginnering'], 
                                    'machine-learning-engineering')
    print(df[column].value_counts())
    return df
 
def clean_location(df,column):
    df[column] = df[column].replace(['maracaibo'], 'maracaibo-venezuela')
    df[column] = df[column].replace(['los-cortijos-caracas'], 'caracas-venezuela') 
    print(df[column].value_counts())
    return df
  
    
def clean_language(df,column):
    df[column] = df[column].replace('us', 'en')
    print(df[column].value_counts())
    return df
    
    
def clean_utm_source(df,column):
    df[column] = df[column].replace('LInkedin', 'linkedin')
    df[column] = df[column].replace('CourseReport', 'coursereport')
    df[column] = df[column].replace(['landingjobs?utm_medium=machine-learning-engineering', 
                                    'landingjobs?utm_medium=full-stack', 'landingjobs?utm_medium=RRSS'],
                                    'landingjobs')
    df[column] = df[column].replace('google_ads', 'google')
    df[column] = df[column].replace(['Business Manager IG', 'Instagram_Feed', 'ig', 'Instagram_Stories'], 'instagram')
    df[column] = df[column].replace(['Facebook','Facebook ads','Facebook_Marketplace','Facebook_Mobile_Feed',
                                    'facebook_instagram','fb','an','facebook_awareness','Facebook_Stories',
                                    'Facebook_Desktop_Feed'], 'facebook')
    df[column] = df[column].replace('4geeks', 'ticjob')
    print(df[column].value_counts())
    return df


def clean_utm_medium(df,column):
    df[column] = df[column].replace(['schoolpage','coursereportschoolpage', 'schoolpage?utm_source=careerkarma',
                                    'Blog','affiliate_email','rrss','inscripcion','event'], 'referral')
    df[column] = df[column].replace(['ppc','FB paid','Facebook_Mobile_Feed','Instagram_Stories','Instagram_Feed'],
                                    'cpc')
    df[column] = np.where((df['utm_source'] == 'linkedin') & (df[column] == 'social') , 
                              'cpc', df[column])

    df[column] = np.where((df['utm_source'] == 'linkedin') & (df[column] == 'Inmail') , 
                              'cpc', df[column])
    print(df[column].value_counts())
    return df      
    

def assign_lead_type(df,column1,column2):
    df.loc[df[column1] == 'request_more_info', column2] = 'SOFT'
    df.loc[df[column1] == 'website-lead', column2] = 'STRONG'
    df.loc[df[column1] == 'newsletter', column2] = 'DISCOVERY'
    df.loc[df[column1] == 'contact-us', column2] = 'SOFT'
    df.loc[df[column1] == 'utec-uruguay', column2] = 'STRONG'
    df.loc[df[column1] == 'jobboard-lead', column2] = 'STRONG'
    df.loc[df[column1] == 'hiring-partner', column2] = 'OTHER'
    df.loc[df[column1] == 'download_outcome', column2] = 'DISCOVERY'
    df.loc[df[column1] == 'website-lead,blacks-in-technology', column2] = 'STRONG'
    df.loc[df[column1] == 'request_downloadable', column2] = 'DISCOVERY'
    print(df[column2].value_counts())
    return df

def assign_with_conditions(df):
    df['utm_medium'] = np.where((df['utm_source'] == 'Facebook ads') | 
                              (df['utm_source'] == 'Facebook_Marketplace') | 
                              (df['utm_source'] == 'Facebook_Mobile_Feed') |
                              (df['utm_source'] == 'facebook_awareness') |
                              (df['utm_source'] == 'Facebook_Stories') |
                              (df['utm_source'] == 'Facebook_Desktop_Feed') |
                              (df['utm_source'] == 'Business Manager IG') |
                              (df['utm_source'] == 'Instagram_Feed') |
                              (df['utm_source'] == 'Instagram_Stories'), 
                              'cpc', df['utm_medium'])

    df['utm_source'] = np.where((df['utm_medium'] == 'Instagram_Stories') |
                              (df['utm_medium'] == 'Instagram_Feed'),
                              'instagram', df['utm_source'])

    df['utm_source'] = np.where((df['utm_medium'] == 'Facebook_Mobile_Feed'),
                              'facebook', df['utm_source'])
       
    print('Assignation with conditions ok')
    return df
  
#Visualization features
    
def countplot_features(df, feature):
    fig = plt.figure(figsize=(10,6))
    ax = sns.countplot(x=df[feature], order=df[feature].value_counts(ascending=False).index);

    abs_values = df[feature].value_counts(ascending=False).values
    ax.bar_label(container=ax.containers[0], labels=abs_values)
    plt.xticks(rotation=30, ha='right')
    #plt.show()
    
def countplot_targetvsfeature(df,feature,target):
    fig = plt.figure(figsize=(10,6))
    ax = sns.countplot(x=df[feature], hue=target, order=df[feature].value_counts(ascending=False).index);

    abs_values = df[feature].value_counts(ascending=False).values
    ax.bar_label(container=ax.containers[0], labels=abs_values)
    plt.xticks(rotation=30, ha='right')
    #plt.show()