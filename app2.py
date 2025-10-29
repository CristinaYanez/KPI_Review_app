#run with: python -m streamlit run app2.py
import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt 
from matplotlib.patches import Circle, Wedge
import plotly.graph_objects as go
import plotly.express as px

# Cargar el reporte de hoy
path='C:/Users/User/Desktop/Cristina/Projects/BI/OUTPUTS/'
filename=str(datetime.today()).split()[0].replace('-','_')+'Report.csv'
df=pd.read_csv(filename) 
st.set_page_config(layout="wide")
st.title("2025 Performance")
data=pd.read_csv(path+'growth_retention.csv') 
#-------------------------------------------------------------------------------------
# contracts diagram
total_2025 = df['2025 contracts'].sum()
total_retained = df['retained contracts'].sum()
total_cancelled = df['cancelled contracts'].sum()
total_considered = total_retained + total_cancelled 
considered_pct = total_considered / total_2025 if total_2025 > 0 else 0
retained_pct = total_retained / total_considered if total_considered > 0 else 0
cancelled_pct = total_cancelled / total_considered if total_considered > 0 else 0 
# FIGURE
fig_circle, ax = plt.subplots(figsize=(3, 3))  
fig_circle.patch.set_facecolor('none')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10) 
ax.axis('off') 
outer_circle = Circle((5, 5), 5, color="white", ec='white')
ax.add_patch(outer_circle)  
inner_radius = 5 * considered_pct
inner_center_y = 5 - (4.8 - inner_radius)   
retained_angle = 360 * retained_pct
cancelled_angle = 360 * cancelled_pct 
retained_wedge = Wedge(center=(4.6, inner_center_y), r=inner_radius, theta1=0, theta2=retained_angle,
                       facecolor='#0000FF', edgecolor='white')
cancelled_wedge = Wedge(center=(4.6, inner_center_y), r=inner_radius, theta1=retained_angle, theta2=360,
                        facecolor="#F51111", edgecolor='white')
ax.add_patch(retained_wedge)
ax.add_patch(cancelled_wedge) 
ax.text(5, 7.6, f'Total Contracts TY\n {total_2025}\nTotal Contracts YTD\n {total_considered}', ha='center', fontsize=7.5,color='black')
# ax.text(9.35, 5.5, f'Used\n {total_considered}', ha='right', fontsize=8,color='black')
ax.text(2, 4.5, f'Retention Rate\n xx% ({total_retained})  ', ha='left', fontsize=8,color='white')
ax.text(7.6, 2.4,f'Cancelled\n{total_cancelled}', ha='right', fontsize=8,color='white')  
#--------------------------------------------------------------------------------------
# Growth  

growth_cols = ['Portfolio ACV', 'KPI ACV YTD', 'Renewed ACV YTD']
growth_labels = ['2025 ACV', 'ACV YTD', 'RENEWED ACV']
growth_values = list(df[growth_cols].sum()/1000000)
#FIGURE
fig_bar = px.bar(
    x=growth_labels,  
    y=growth_values,
    title='Growth',
    labels={'x': '', 'y': 'Millions of dollars'},
    color_discrete_sequence=['blue']
) 
fig_bar.update_layout(  
    title_font_size=25
)   
#-----------------------------------------------------------------------------------------
figgo = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=round(df['retention ($)'].sum(),1),
    delta={'reference': round(df['KPI ACV YTD'].sum(),1), 'increasing': {'color': "green"}},
    gauge={
        'axis': {'range': [None, round(df['Portfolio ACV'].sum(),1)]},
        'bar': {'color':'lightgreen'},# "#00Ff08"
        'steps': [
            {'range': [0,  round(df['KPI ACV YTD'].sum(),1)], 'color': "blue"},
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 1,
            'value': round(df['Portfolio ACV'].sum(),1)
        },
    },
    
    title={
            'text': "<b>ACV Portfolio Renewal Overview</b>",
            'font': {'size': 25},
            'align': 'left'
        } ))


figgo.add_annotation(
    x=1, y=0,  # Adjust position
    text=f"2025 ACV",
    showarrow=False,
    font=dict(color="red", size=20)
)
figgo.add_annotation(
    x=0.5, y=0,  # Adjust position
    text=f"Retention",
    showarrow=False,
    font=dict(color="white", size=16)
)
#############################################################################################

col1, col2,col3= st.columns([1, 1, 1])
with col1:    
    st.pyplot(fig_circle,width='content')
with col3:
    st.plotly_chart(fig_bar, width='content') 
with col2:
    st.plotly_chart(figgo, width='content')


# #--------------------------------------------------------------------------------------

growth_cols = ['Portfolio ACV', 'KPI ACV YTD', 'Renewed ACV YTD']
growth_labels = ['2025 ACV', 'ACV YTD', 'RENEWED ACV']

agents = [agent for agent in df['Agent Name'].unique() if agent != 'REASSIGNED'] 
tabs = st.tabs(agents) 
for i, agent in enumerate(agents):
    with tabs[i]:
        agent_df = df[df['Agent Name'] == agent]
        fig1 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=agent_df['retention ($)'].iloc[0],
            delta={'reference': agent_df['KPI ACV YTD'].iloc[0], 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, agent_df['Portfolio ACV'].iloc[0]]},
                'bar': {'color': "white"},
                'steps': [
                    {'range': [0, agent_df['KPI ACV YTD'].iloc[0]], 'color': "blue" },
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': agent_df['Portfolio ACV'].iloc[0]
                }
            },title={
                'text': "<b>Retention</b>",
                'font': {'size': 25},
                'align': 'left'
            } ))            
        fig1.add_annotation(
            x=1, y=0,  # Adjust position
            text=f"2025 ACV",
            showarrow=False,
            font=dict(color="red", size=20)
        )
        fig1.add_annotation(
            x=0.5, y=0,  # Adjust position
            text=f"Retention",
            showarrow=False,
            font=dict(color="white", size=16)
        )
        col1, col2,col3 = st.columns(3)
        with col1:
            st.plotly_chart(fig1)
        with col2: 
            growth_values = agent_df[growth_cols].sum() 
            fig2 = px.bar(
                x=growth_labels,
                y=growth_values,
                title='Growth',
                labels={'x': '', 'y': ''},
                color_discrete_sequence=['blue']
            ) 
            fig2.update_layout(  
                title_font_size=25
            )                 
            st.plotly_chart(fig2, width='content')   
        if st.button(agent+'   |   Contracts Distribution'):               
            st.dataframe(agent_df[['Agent Name', '2025 contracts', 'consider contracts', 'retained contracts', 'cancelled contracts', 'retention (#)%',]])
        
        if st.button(agent+'   |   Retention'):  
            col1, col2 = st.columns(2)
            with col1:
                agent_df1 = agent_df[['Agent Name', 'Portfolio ACV', 'KPI ACV YTD', 'Renewed ACV YTD']].copy().transpose()
                agent_df1.columns = agent_df1.iloc[0]
                agent_df1 = agent_df1[1:]
                st.dataframe(agent_df1,width=400)
            with col2:
                agent_df2 =agent_df[['retention ($)', 'retention ($)%', 'retentionSPIF ($)', 'retentionSPIF ($)%']].copy().transpose()
                # agent_df2.columns = agent_df2.iloc[0]
                # agent_df2 = agent_df2[1:]
                st.dataframe(agent_df2,width=400)
        if st.button(agent+'   |   growth'):  
            col1, col2 = st.columns(2)
            with col1:
                agent_df1 = agent_df[['Agent Name', 'Portfolio ACV', 'KPI ACV YTD', 'Renewed ACV YTD']].copy().transpose()
                agent_df1.columns = agent_df1.iloc[0]
                agent_df1 = agent_df1[1:]
                st.dataframe(agent_df1,width=400)
                
            # st.dataframe(agent_df[['Agent Name', 'Portfolio ACV', 'KPI ACV YTD', 'Renewed ACV YTD']].transpose(),width=400)
            with col2:
                st.dataframe(agent_df[['growth ($)', 'growth (%)',]].transpose(),width=200)  
        with st.expander("Dataset"):
            st.dataframe(data[data['AE_NAME']==agent],width=2000)  
                    