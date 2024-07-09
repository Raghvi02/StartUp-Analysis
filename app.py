import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout ='wide', page_title='StartUp')
df= pd.read_csv('startup_clean.xls')
df['date']= pd.to_datetime(df['date'],errors='coerce')
df['year']=df['date'].dt.year
data= df.groupby(['year','startup'])['amount'].sum().reset_index()
data= data.sort_values(['year','amount'],ascending=[True, False])
data=data.groupby('year').head()
data.set_index(data['startup'],inplace = True)
data.drop(columns=['year','startup'],inplace = True)
st.sidebar.title('Startup Funding Analysis')

def load_overall_analysis():
    # st.title('OverAll Analysis')
    total=round( df['amount'].sum())
    max_fund= df.groupby('amount')['amount'].sum().max()
    count_fund=  len(df.groupby('startup'))
    avg_fund=  round(df.groupby('startup')['amount'].sum().mean())
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',str(total)+' Cr')
    with col2:
        st.metric('Max',str(max_fund)+' Cr')
    with col3:
        st.metric('Funded StartUps',str(count_fund)+' Cr')
    with col4:
        st.metric('Average',str(avg_fund)+' Cr')
    st.subheader('YOY')
    select= st.selectbox('Select Type',['Total','Count'])
    if select== 'Total':
        temp_df=df.groupby('year')['startup'].count()
    else:
        temp_df=df.groupby('year')['amount'].sum()
    plt.plot(temp_df)
    st.pyplot(plt)
    col1,col2= st.columns(2)
    with col1:
        vert_series=df.groupby('vertical')['amount'].sum().sort_values(ascending = False).head()
        st.subheader('Most Invested Verticles')
        fig5, ax5= plt.subplots()
        ax5.pie(vert_series,autopct="%0.1f%%",labels=vert_series.index)
        st.pyplot(fig5)
    with col2:
        vert2_series=df.groupby('vertical')['startup'].count().sort_values(ascending = False).head()
        st.subheader('Count Verticles')
        fig6, ax6= plt.subplots()
        ax6.pie(vert2_series,autopct="%0.1f%%",labels=vert_series.index)
        st.pyplot(fig6)
        
    st.title('Funding Types and their count')
    col1, col2= st.columns(2)
    df2=df.groupby('round')['startup'].count().sort_values(ascending = False)
    with col1:
        st.dataframe(df2, height =800, width=2000) 
    with col2:
        fig6,ax6= plt.subplots()
        ax6.bar(df2.head().index, df2.head().values )
        ax6.set_xticklabels(df2.head().index, rotation=45)
        st.pyplot(fig6)
    st.title('City wise funding')
    col1, col2= st.columns(2)
    df3=df.groupby('city')['startup'].count().sort_values(ascending = False)
    with col1:
        st.dataframe(df3, height =800, width=2000) 
    with col2:
        fig7,ax7= plt.subplots()
        ax7.bar(df3.head().index, df3.head().values )
        ax7.set_xticklabels(df3.head().index, rotation=45)
        st.pyplot(fig7)   
    col1, col2= st.columns(2)
    with col1:
        st.title('Find Top Funded StartUps of each year')
        yr=st.selectbox('Select Year', df['year'].unique())
        if yr == 2015:
            st.dataframe(data.iloc[0:5,1:])
        elif yr == 2016:
            st.dataframe(data.iloc[5:10])
        elif yr == 2017:
            st.dataframe(data.iloc[10:15])
        elif yr == 2018:
            st.dataframe(data.iloc[15:20])
        elif yr == 2019:
            st.dataframe(data.iloc[20:25])
        else:
            st.dataframe(data.iloc[25:])
    
    
           
        
        
        
        
        
        
def load_investor_details(investor):
    df2=df[df['Investors Name'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(df2)
    col1,col2= st.columns(2)
    with col1:
        big_series=df[df['Investors Name'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values( ascending = False).head()
        st.subheader('Most Biggest Investments')
        fig, ax= plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        sectors=df[df['Investors Name'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')
        fig1, ax1= plt.subplots()
        ax1.pie(sectors,autopct="%0.1f%%",labels=sectors.index)
        st.pyplot(fig1)
    col1,col2= st.columns(2)
    with col1:
        stage= df[df['Investors Name'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stages Invested In')
        fig2, ax2= plt.subplots()
        ax2.pie(stage, autopct="%0.1f%%",labels=stage.index)
        st.pyplot(fig2)
    with col2:
        city= df[df['Investors Name'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Cities Invested In')
        fig3, ax3= plt.subplots()
        ax3.pie(city, autopct="%0.1f%%",labels=city.index)
        st.pyplot(fig3)
    
    df['year']=df['date'].dt.year
    date= df[df['Investors Name'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investment')
    fig4, ax4= plt.subplots()
    ax4.plot(date)
    st.pyplot(fig4)
   
    
option = st.sidebar.selectbox('Select One',['OverAll Analysis', 'StartUp','Investor'])
if option =='OverAll Analysis':
    st.title('OverAll Analysis')
    load_overall_analysis()
    
    
elif option== 'StartUp':
    st.sidebar.selectbox('Select StartUp',df['startup'].unique().tolist())
    st.title('StartUp Analysis')
    btn1=st.sidebar.button('Find StartUp Details')
    
else:
    investor=st.sidebar.selectbox('Select Investor',sorted(set(df['Investors Name'].str.split(',').sum())))
    st.title('Investor Analysis')
    btn2=st.sidebar.button('Find StartUp Details')
    if btn2:
        load_investor_details(investor)
    