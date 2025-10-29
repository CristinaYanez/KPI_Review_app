#run with: python -m streamlit run app.py

import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt 
from matplotlib.patches import Circle, Wedge
import plotly.graph_objects as go
import plotly.express as px  
#------------------------------------------------------------------------------------ 
# run the scripts to compute kpi's and generate today's reports

#------------------------------------------------------------------------------------ 
# load today's report
path='C:/Users/User/Desktop/Cristina/Projects/BI/OUTPUTS/'
filename=str(datetime.today()).split()[0].replace('-','_')+'retentionReport.csv'
filename1=str(datetime.today()).split()[0].replace('-','_')+'growthReport.csv'
filename2=str(datetime.today()).split()[0].replace('-','_')+'revenueReport.csv'
df=pd.read_csv( filename) 
df1=pd.read_csv( filename1) 
df2=pd.read_csv( filename2) 
st.set_page_config(layout="wide")
st.title("2025 Performance")
retention_data=pd.read_csv( 'kpi_retention.csv') 
growth_data=pd.read_csv( 'kpi_growth.csv') 
revenue_data=pd.read_csv( 'kpi_revenue.csv') 
# general charts
fig1 = px.bar(
    x=['Consider Contracts', '2025 Remaining Contracts'],
    y=[df['consider contracts'].sum(), df['2025 contracts'].sum()-df['consider contracts'].sum()],
    title='2025 YTD Number of Contracts',
    color=['Consider Contracts', '2025 Remaining Contracts'],
    color_discrete_map={
        'Consider Contracts': '#28a745',
        '2025 Remaining Contracts': '#473D3C'
    } ,
    text=[df['consider contracts'].sum(), df['2025 contracts'].sum()-df['consider contracts'].sum()],
) 
fig1.update_layout(
    showlegend=False,
    xaxis_title=None,         
    yaxis_title=None  
)
fig2 = px.pie(
    names=['Retained','Cancelled'],
    values=[df['retained contracts'].sum(),df['cancelled contracts'].sum()],
    title='YTD Contracts & Status',
    color_discrete_sequence=["#3e58dd", "#dc3545"]
) 
fig2.update_layout(
    legend=dict(
        orientation="h",        
        yanchor="bottom",       
        y=-0.2,               
        xanchor="center",      
        x=0.5                   
    )
)
fig35 = px.pie(
    names=['Retained ACV','Cancelled ACV'],
    values=[df['KPI ACV YTD'].sum(),df['Portfolio ACV'].sum()-df['KPI ACV YTD'].sum()],
    title='YTD Renewal ACV',
    color_discrete_sequence=["#28a745", "#dc3545"]
) 
fig35.update_layout(
    legend=dict(
        orientation="h",        
        yanchor="bottom",       
        y=-0.2,               
        xanchor="center",      
        x=0.5                   
    )
)
fig1.update_layout(height=400,width=600)
fig2.update_layout(height=400)
fig35.update_layout(height=400)
col0,col1, col2,col3,col4  = st.columns([0.4,1,1,1,0.4])
with col1:
    st.plotly_chart(fig1, use_container_width=False)
with col2:
    st.plotly_chart(fig2, use_container_width=True) 
with col3:
    st.plotly_chart(fig35, use_container_width=True) 
tabs=['Retention','Growth','Revenue']
tabs = st.tabs(tabs)  
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
######### CONTRACTS DISTRIBUTION for retention #########
filtered_df = df[df['Agent Name'] != 'REASSIGNED']
filtered_df['AM']=filtered_df['Agent Name']  
melted_df = filtered_df.melt(
    id_vars=['AM', 'KPI ACV YTD'],
    value_vars=['retained contracts', 'cancelled contracts'],
    var_name='Contract Type',
    value_name='Count'
) 
melted_df['ACV YTD'] = (
    melted_df['Count'] / melted_df.groupby('AM')['Count'].transform('sum')
) * melted_df['KPI ACV YTD'] 
fig = px.bar(
    melted_df,
    y='AM',
    x='ACV YTD',
    color='Contract Type',
    orientation='h',
    color_discrete_map={
        'retained contracts': '#3e58dd',
        'cancelled contracts': '#dc3545'
    },
    title='YTD Renewal by AM ',
    text='Count'
)
fig.update_traces(textposition='inside')
fig.update_layout(yaxis={'categoryorder': 'total ascending'},xaxis=dict(showgrid=True, gridcolor='lightgrey'))
#------------------------------------------------------------------------------------ 
# RETENTION  
etapas = ["2025 Total Portfolio ACV", "Remaining Renewal ACV","Renewal ACV YTD" ,"Cancellations ACV ", "ACV YTD"]
valores = [df['Portfolio ACV'].sum(),df['KPI ACV YTD'].sum()-df['Portfolio ACV'].sum(),df1['KPI ACV YTD'].sum(), df['retention ($)'].sum()-df['KPI ACV YTD'].sum(),df['retention ($)'].sum()]
# waterfall figure
fig5 = go.Figure(go.Waterfall( 
    orientation="v",
    measure=["relative", "relative", 'total',"relative",  'total' ],
    x=etapas,
    text=[f"${v:,.0f}" for v in valores],
    y=valores, 
    connector={"line": {"color": "rgb(63, 63, 63)"}},
    increasing={"marker": {"color": "#28a745"}},    
    decreasing={"marker": {"color": "#dc3545"}},   
    totals={"marker": {"color": "#3e58dd"}}        
))
fig5.update_layout(
    title="Retention",
    waterfallgap=0.3,
    template="plotly_white",
    title_font=dict(size=28)
)

fig5.add_annotation(
    text="Retention "+str(round((df['retention ($)'].sum())/(df['KPI ACV YTD'].sum())*100,2))+'% ',
    xref="paper", yref="paper",
    x=0.83, y=0.3,   
    showarrow=False,
    font=dict(size=20,color='black'),
    align="center"
) 


#------------------------------------------------------------------------------------ 
# display charts
with tabs[0]: #0:retention 
    col11, col31, = st.columns([1, 1])
    with col11:
        st.plotly_chart(fig5, use_container_width=True) 
    with col31:
        st.plotly_chart(fig, use_container_width=True) 
    ret_tabs = st.tabs(list(filtered_df['Agent Name'].unique()))  
    for i, agent in enumerate(filtered_df['Agent Name']):
        with ret_tabs[i]: 
            agent_df=df[df['Agent Name']==agent]         
                        
            # retention
            etapas = ["2025 Total Portfolio ACV", "Remaining Renewal ACV", 'Renewal ACV YTD',"Cancellations", "ACV YTD"]
            valores = [agent_df['Portfolio ACV'].sum(),agent_df['KPI ACV YTD'].sum()-agent_df['Portfolio ACV'].sum(),agent_df['KPI ACV YTD'].sum(), agent_df['retention ($)'].sum()-agent_df['KPI ACV YTD'].sum(),agent_df['retention ($)'].sum()]
            fig6 = go.Figure(go.Waterfall(
                orientation="v",
                measure=["relative", "relative",'total',"relative",  'total' ],
                x=etapas,
                text=[f"${v:,.0f}" for v in valores],
                y=valores,
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#28a745"}},   
                decreasing={"marker": {"color": "#dc3545"}},   
                totals={"marker": {"color": "#007bff"}}       
            ))
            fig6.update_layout(
                title="Retention",
                waterfallgap=0.3,
                template="plotly_white",
            )  
            fig6.add_annotation(
                text="Retention "+str(agent_df['retention ($)%'].values[0])+'%',  
                xref="paper", yref="paper",
                x=0.82, y=0.20,  
                showarrow=False,
                font=dict(size=20,color='black'),
                align="left"
            ) 
            fig6.add_annotation(
                text="Contracts Retention Rate: "+ str(agent_df['retention (#)%'].values[0])+'%',  
                xref="paper", yref="paper",
                x=0.99, y=0.99,  
                showarrow=False,
                font=dict(size=20,color='gray'),
                align="left"
            )
            # spif retention 
            # agent_df
            if agent_df['initial SPIF ACV'].sum()==1:
                agent_df['initial SPIF ACV']=0
            etapas = ["2025 Portfolio (Since August)",  "SPIF Retention", "SPIF Retained ACV YTD"]
            valores = [agent_df['initial SPIF ACV'].sum(),  agent_df['retentionSPIF ($)'].sum()-agent_df['initial SPIF ACV'].sum(), agent_df['retentionSPIF ($)'].sum()]
            fig7 = go.Figure(go.Waterfall(
                orientation="v",
                measure=["relative", "relative",'total',  ],
                x=etapas,
                text=[f"${v:,.0f}" for v in valores],
                y=valores,
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#21a740"}},   
                decreasing={"marker": {"color": "#dc3545"}},   
                totals={"marker": {"color": "#007bff"}}       
            ))
            fig7.update_layout(
                title="Retention SPIF",
                waterfallgap=0.3,
                template="plotly_white",
            )  
            fig7.add_annotation(
                text="SPIF Retention "+ str(agent_df['retentionSPIF ($)%'].values[0])+'%',  
                xref="paper", yref="paper",
                x=0.51, y=0.2,   
                showarrow=False,
                font=dict(size=20,color='black'),
                align="left"
            ) 
            col1, col2  = st.columns(2)
            with col1:
                st.plotly_chart(fig6, use_container_width=True)
            with col2:
                st.plotly_chart(fig7, use_container_width=True,key=agent+'spif')
            # show dataset
            with st.expander(agent+" Dataset"):
                displ=retention_data[retention_data['AE_NAME']==agent].reset_index()
                displ.drop(columns=['index'],inplace=True)
                st.dataframe(displ,width=2000)  
#------------------------------------------------------------------------------------ 
#-------------------------------------------------------------------------------------
######### CONTRACTS DISTRIBUTION for growth #########   
filtered_df = df1[df1['Agent Name'] != 'REASSIGNED']
filtered_df['AM']=filtered_df['Agent Name'] 
melted_df = filtered_df.melt(
    id_vars=['AM', 'KPI ACV YTD'],
    value_vars=['retained contracts', 'cancelled contracts'],
    var_name='Contract Type',
    value_name='Count'
) 
melted_df['ACV YTD'] = (    melted_df['Count'] / melted_df.groupby('AM')['Count'].transform('sum')) * melted_df['KPI ACV YTD'] 
fig = px.bar(
    melted_df,
    y='AM',
    x='ACV YTD',
    color='Contract Type',
    orientation='h',
    color_discrete_map={
        'retained contracts': "#3c57e0",
        'cancelled contracts': "#d83243"
    },
    title='YTD Renewal ACV by AM & Status ',
    text='Count'
)
fig.update_traces(textposition='inside')
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
#------------------------------------------------------------------------------------ 
# GROWTH  
etapas = ["2025 Total Portfolio ACV", "Remaining Renewal ACV" ,'ACV YTD',"Growth", "Renewed ACV YTD"]
valores = [df1['Portfolio ACV'].sum(),df1['KPI ACV YTD'].sum()-df1['Portfolio ACV'].sum(),df1['KPI ACV YTD'].sum(), df1['growth ($)'].sum(),df1['Renewed ACV YTD'].sum()]
# waterfall figure
fig5_1 = go.Figure(go.Waterfall( 
    orientation="v",
    measure=["relative", "relative", 'total',"relative", 'total' ],
    x=etapas,
    text=[f"${v:,.0f}" for v in valores],
    y=valores, 
    connector={"line": {"color": "rgb(63, 63, 63)"}},
    increasing={"marker": {"color": "#28a745"}},    
    decreasing={"marker": {"color": "#dc3545"}},   
    totals={"marker": {"color": "#047bfb"}}       
)) 
fig5_1.update_layout(
    title="Overall Growth",
    waterfallgap=0.3,
    template="plotly_white",
    title_font=dict(size=28)
)
fig5_1.add_annotation(
    text="Growth "+str(round((df1['growth ($)'].sum())/(df1['KPI ACV YTD'].sum())*100,2))+'% ',
    xref="paper", yref="paper",
    x=0.81, y=0.24,   
    showarrow=False,
    font=dict(size=20,color='black'),
    align="center"
) 
#------------------------------------------------------------------------------------ 
with tabs[1]: #1:growth
    ret_tabs = st.tabs(list(filtered_df['Agent Name'].unique()))  
    for i, agent in enumerate(filtered_df['Agent Name']):  
        with ret_tabs[i]: 
            
            col1, col3  = st.columns(2)    
            with col1:
                st.plotly_chart(fig5_1, use_container_width=True,key=agent) 
            with col3:
                agent_df1=df1[df1['Agent Name']==agent] 
                # st.text(agent_df1['retention ($)%'])
                # growth
                etapas = ["2025 Total Portfolio ACV", "Remaining Renewal ACV",'ACV YTD', "Growth", "Renewed ACV YTD"]
                valores = [agent_df1['Portfolio ACV'].sum(),agent_df1['KPI ACV YTD'].sum()-agent_df1['Portfolio ACV'].sum(),agent_df1['KPI ACV YTD'].sum(), agent_df1['growth ($)'].sum(),agent_df1['Renewed ACV YTD'].sum()]
                fig6_1 = go.Figure(go.Waterfall( 
                    orientation="v",
                    measure=["relative", "relative", 'total',"relative", 'total' ],
                    x=etapas,
                    text=[f"${v:,.0f}" for v in valores],
                    y=valores, 
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                    increasing={"marker": {"color": "#1ab33e"}},   
                    decreasing={"marker": {"color": "#dc3545"}},  
                    totals={"marker": {"color": "#057bfa"}}         
                ))
                fig6_1.update_layout(
                    title=' '.join(pd.Series(agent.split()).str.capitalize())+" Growth",
                    waterfallgap=0.3,
                    template="plotly_white",
                    title_font=dict(size=28)
                )             
                                
                fig6_1.add_annotation(
                    text="Growth "+str(round((agent_df1['growth ($)'].sum())/(agent_df1['KPI ACV YTD'].sum())*100,2))+'% ',
                    xref="paper", yref="paper",
                    x=0.81, y=0.23,   
                    showarrow=False,
                    font=dict(size=20,color='black'),
                    align="center"
                ) 
                st.plotly_chart(fig6_1, use_container_width=True)

            # show dataset
            with st.expander(agent+" Dataset"):
                displ=growth_data[growth_data['AE_NAME']==agent].reset_index()
                displ.drop(columns=['index'],inplace=True)
                st.dataframe(displ,width=2000)  
#------------------------------------------------------------------------------------ 
with tabs[2]: #2: revenue
    #bar charts
    
    fig1_2 = px.bar(
        x=['Expected Revenue', 'Actual Revenue'],
        y=[df2['expected_revenue'].sum(), df2['revenue'].sum()],
        title='Overall Revenue',
        color=['Consider Contracts', '2025 Remaining Contracts'],
        color_discrete_map={
            'Consider Contracts': "#282aa7",
            '2025 Remaining Contracts': "#35944E"
        } ,
        text=[df2['expected_revenue'].sum(), df2['revenue'].sum()],
    ) 
    fig1_2.update_layout(
        showlegend=False,
        xaxis_title=None,         
        yaxis_title=None  
    )
    fig1_2.update_layout(width=400)
    filtered_df2 = df2[df2['AE_NAME'] != 'REASSIGNED']
    ret_tabs = st.tabs(list(filtered_df2['AE_NAME'].unique()))  
    for i, agent in enumerate(filtered_df2['AE_NAME']):  
        with ret_tabs[i]:             
            agent_df2=df2[df2['AE_NAME']==agent] 
            col1,col2=st.columns(2)
            with col1:
                st.plotly_chart(fig1_2, use_container_width=False,key=agent+'revenue')

            with col2: 
                fig2_2 = px.bar(
                    x=['Expected Revenue', 'Actual Revenue'],
                    y=[agent_df2['expected_revenue'].sum(), agent_df2['revenue'].sum()],
                    title=' '.join(pd.Series(agent.split()).str.capitalize())+" Revenue",
                    color=['Consider Contracts', '2025 Remaining Contracts'],
                    color_discrete_map={
                        'Consider Contracts': "#282aa7",
                        '2025 Remaining Contracts': "#35944E"
                    } ,
                    text=[agent_df2['expected_revenue'].sum(), agent_df2['revenue'].sum()],
                ) 
                fig2_2.update_layout(
                    showlegend=False,
                    xaxis_title=None,         
                    yaxis_title=None  
                )
                fig2_2.update_layout(width=400)
                st.plotly_chart(fig2_2, use_container_width=False)

    
 

