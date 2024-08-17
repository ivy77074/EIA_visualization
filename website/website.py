import streamlit as st
import pandas as pd
import plotly.express as pex
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from myeia.api import API
from datetime import date
from datetime import timedelta
import glob, os


# set page is wide
st.set_page_config(layout='wide')

# folderimg = os.getcwd() + '\\CO_NG_images'
# folderimg2 = os.getcwd() + '\\dpr images'
folderimg = './CO_NG_images'
folderimg2 = './dpr images'

# get data
@st.cache_data
def refreshData():
    imagePaths = []
    for file in glob.glob('./CO_NG_images/*.jpg'):
        imagePaths.append(file)
    
    #### get interactive graph data for crude and gas
    # register an EIA API token then past it here
    EIA_TOKEN = 'RntNbLbGg7j09oSsnvyUaY7fIEV0UlyNNiAaVPzh'
    eia = API(EIA_TOKEN)

    data = []
    for item in ['TOPRL48', 'TOPRAC', 'TOPRBK', 'TOPREF', 'TOPRMP', 'TOPRNI', 'TOPRPM', 'TOPRWF', 'TOPRR48']:
        dftemp = pd.DataFrame(eia.get_series_via_route(route='steo/', 
                                                    series=item,
                                                    facet='seriesId',
                                                    frequency='monthly'))
        data.append(dftemp)
    dfto = pd.concat(data, axis=1)
    
    ##### change eia data in df
    # set date in index to a column
    df1 = dfto.reset_index()

    # change columns' names
    df1.columns = ['date', 'L48_shale', 'austin_chalk', 'bakken', 'eagle_ford', 'mississippian', 'niobrara', 'permian', 'woodford', 'other']

    # change types' other columns to float
    df1['L48_shale'] = df1['L48_shale'].astype(float)
    df1['austin_chalk'] = df1['austin_chalk'].astype(float)
    df1['bakken'] = df1['bakken'].astype(float)
    df1['eagle_ford'] = df1['eagle_ford'].astype(float)
    df1['mississippian'] = df1['mississippian'].astype(float)
    df1['niobrara'] = df1['niobrara'].astype(float)
    df1['permian'] = df1['permian'].astype(float)
    df1['woodford'] = df1['woodford'].astype(float)
    df1['other'] = df1['other'].astype(float)

    # add anadarko and eagle ford basin for df
    dfCO = df1.copy()

    dfCO['anadarko'] = dfCO['mississippian'] + dfCO['woodford']
    dfCO['eagleFord'] = dfCO['eagle_ford'] + dfCO['austin_chalk']

    # change sting to datetime
    dfCO['date'] = pd.to_datetime(dfCO['date'])

    # add data for anadarko and eagleFord
    dfCO['anadarko'] = dfCO['mississippian'] + dfCO['woodford']
    dfCO['eagleFord'] = dfCO['eagle_ford'] + dfCO['austin_chalk']

    # round data to 2 decimal places
    dfCO['L48_shale'] = dfCO['L48_shale'].apply(lambda x: round(x, 2))
    dfCO['austin_chalk'] = dfCO['austin_chalk'].apply(lambda x: round(x, 2))
    dfCO['bakken'] = dfCO['bakken'].apply(lambda x: round(x, 2))
    dfCO['eagle_ford'] = dfCO['eagle_ford'].apply(lambda x: round(x, 2))
    dfCO['mississippian'] = dfCO['mississippian'].apply(lambda x: round(x, 2))
    dfCO['niobrara'] = dfCO['niobrara'].apply(lambda x: round(x, 2))
    dfCO['permian'] = dfCO['permian'].apply(lambda x: round(x, 2))
    dfCO['woodford'] = dfCO['woodford'].apply(lambda x: round(x, 2))
    dfCO['other'] = dfCO['other'].apply(lambda x: round(x, 2))

    dfCO['anadarko'] = dfCO['anadarko'].apply(lambda x: round(x, 2))
    dfCO['eagleFord'] = dfCO['eagleFord'].apply(lambda x: round(x, 2))


    ### get data for natural gas
    data = []
    for item in ['SNGPRL48', 'SNGPRBK', 'SNGPRBN', 'SNGPREF', 'SNGPRFY', 'SNGPRHA', 'SNGPRMC', 'SNGPRMP', 'SNGPRNI', 'SNGPRPM', 'SNGPRUA', 'SNGPRWF', 'SNGPRR48']:
        dfto = pd.DataFrame(eia.get_series_via_route(route='steo/', 
                                                    series=item,
                                                    facet='seriesId',
                                                    frequency='monthly'))
        data.append(dftemp)
    dfto = pd.concat(data, axis=1)
    # set date in index to a column
    df2 = dfto.reset_index()

    # change columns' names
    df2.columns = ['date', 'L48_shale', 'bakken', 'barnett', 'eagle_ford', 'fayetteville', 'haynesville', 'marcellus', 'mississippian', 'niobrara', 'permian', 'utica', 'woodford', 'other']


    # change types' other columns to float
    df2['L48_shale'] = df2['L48_shale'].astype(float)
    df2['bakken'] = df2['bakken'].astype(float)
    df2['barnett'] = df2['barnett'].astype(float)
    df2['eagle_ford'] = df2['eagle_ford'].astype(float)
    df2['fayetteville'] = df2['fayetteville'].astype(float)
    df2['haynesville'] = df2['haynesville'].astype(float)
    df2['marcellus'] = df2['marcellus'].astype(float)
    df2['mississippian'] = df2['mississippian'].astype(float)
    df2['niobrara'] = df2['niobrara'].astype(float)
    df2['permian'] = df2['permian'].astype(float)
    df2['utica'] = df2['utica'].astype(float)
    df2['woodford'] = df2['woodford'].astype(float)
    df2['other'] = df2['other'].astype(float)


    ##### add anadarko, permian, appalachia data into df
    dfNG = df2.copy()

    dfNG['anadarko'] = dfNG['mississippian'] + dfNG['woodford'] + dfNG['fayetteville']
    dfNG['permianimg'] = dfNG['permian'] + dfNG['barnett']
    dfNG['appalachia'] = dfNG['marcellus'] + dfNG['utica']

    # change sting to datetime
    dfNG['date'] = pd.to_datetime(dfNG['date'])

    # add data for anadarko, permianimg, and appalachia
    dfNG['anadarko'] = dfNG['mississippian'] + dfNG['woodford'] + dfNG['fayetteville']
    dfNG['permianimg'] = dfNG['permian'] + dfNG['barnett']
    dfNG['appalachia'] = dfNG['marcellus'] + dfNG['utica']

    # round data to 2 decimal places
    dfNG['L48_shale'] = dfNG['L48_shale'].apply(lambda x: round(x, 2))
    dfNG['bakken'] = dfNG['bakken'].apply(lambda x: round(x, 2))
    dfNG['barnett'] = dfNG['barnett'].apply(lambda x: round(x, 2))
    dfNG['eagle_ford'] = dfNG['eagle_ford'].apply(lambda x: round(x, 2))
    dfNG['fayetteville'] = dfNG['fayetteville'].apply(lambda x: round(x, 2))
    dfNG['haynesville'] = dfNG['haynesville'].apply(lambda x: round(x, 2))
    dfNG['marcellus'] = dfNG['marcellus'].apply(lambda x: round(x, 2))
    dfNG['mississippian'] = dfNG['mississippian'].apply(lambda x: round(x, 2))
    dfNG['niobrara'] = dfNG['niobrara'].apply(lambda x: round(x, 2))
    dfNG['permian'] = dfNG['permian'].apply(lambda x: round(x, 2))
    dfNG['utica'] = dfNG['utica'].apply(lambda x: round(x, 2))
    dfNG['woodford'] = dfNG['woodford'].apply(lambda x: round(x, 2))
    dfNG['other'] = dfNG['other'].apply(lambda x: round(x, 2))

    dfNG['anadarko'] = dfNG['anadarko'].apply(lambda x: round(x, 2))
    dfNG['permianimg'] = dfNG['permianimg'].apply(lambda x: round(x, 2))
    dfNG['appalachia'] = dfNG['appalachia'].apply(lambda x: round(x, 2))

    ### get weekly production for the line in graph
    crude = pd.DataFrame(eia.get_series_via_route(route="petroleum/sum/sndw", series='W_EPC0_FPF_R48_MBBLD', frequency="weekly",))

    crude.reset_index(inplace=True)
    crude.columns = ['date', 'L48']
    crude['L48'] = crude['L48'].astype(float)
    crude['L48'] = crude['L48'] / 1000
    crude = crude.sort_values('date')



    #### get dpr data
    # get dpr images' paths
    imagePaths2 = []
    for file in glob.glob('./dpr images/*.jpg'):
        imagePaths2.append(file)
    
    # true rounding
    def rounding(num, n=0):
        num = float(num)
        if '.' in str(num):
            if len(str(num).split('.')[1]) > n and str(num).split('.')[1][n] == '5':
                num += 1 * 10 ** -(n+1)
        if n:
            return str(round(num, n))
        else:
            return str(round(num))

    series = [['RIGSAP', 'RIGSBK', 'RIGSEF', 'RIGSHA', 'RIGSPM', 'RIGSR48'],
          ['NWDAP', 'NWDBK', 'NWDEF', 'NWDHA', 'NWDPM', 'NWDR48'],
          ['NWCAP', 'NWCBK', 'NWCEF', 'NWCHA', 'NWCPM', 'NWCR48'],
          ['DUCSAP', 'DUCSBK', 'DUCSEF', 'DUCSHA', 'DUCSPM', 'DUCSR48']]

    activity = ['rig count', 'drilled', 'completed', 'DUC']


    finaldf = []
    for i in range(len(series)):
        # get data then store in df
        data = []
        for item in series[i]:
            df = pd.DataFrame(eia.get_series_via_route(route='steo/', 
                                                            series=item,
                                                            facet='seriesId',
                                                            frequency='monthly'))
            data.append(df)
        dftemp = pd.concat(data, axis=1)
            
        # reset index and add date col
        dftemp = dftemp.reset_index()

        # rename cols
        dftemp.columns = ['date','appalachia', 'bakken', 'eagle_ford', 'haynesville', 'permian', 'others']
        # add activity col
        dftemp['activity'] = activity[i]
        # change col order
        dftemp = dftemp.loc[:, ['date', 'activity','appalachia', 'bakken', 'eagle_ford', 'haynesville', 'permian', 'others']]
        
        if activity[i] == 'rig count':
            dftemp['appalachia'] = dftemp['appalachia'].apply(rounding)
            dftemp['bakken'] = dftemp['bakken'].apply(rounding)
            dftemp['eagle_ford'] = dftemp['eagle_ford'].apply(rounding)
            dftemp['haynesville'] = dftemp['haynesville'].apply(rounding)
            dftemp['permian'] = dftemp['permian'].apply(rounding)
            dftemp['others'] = dftemp['others'].apply(rounding)

        dftemp = dftemp.query("date >= '2013-12-01'")
        # add dftemp to finaldf
        finaldf.append(dftemp)

    ### change values in df to float from str
    for df in finaldf:
        df['appalachia'] = df['appalachia'].astype(float)
        df['bakken'] = df['bakken'].astype(float)
        df['eagle_ford'] = df['eagle_ford'].astype(float)
        df['haynesville'] = df['haynesville'].astype(float)
        df['permian'] = df['permian'].astype(float)
        df['others'] = df['others'].astype(float)

        df['Total'] = (df['appalachia'] + 
                            df['bakken'] + 
                            df['eagle_ford'] + 
                            df['haynesville'] + 
                            df['permian'] + 
                            df['others'])

    # group different activity
    dfri = finaldf[0]
    dfdr = finaldf[1]
    dfco = finaldf[2]
    dfdu = finaldf[3]

    # reorganize data for subplot
    dfdr1 = dfdr.drop(['activity', 'bakken', 'eagle_ford', 'haynesville', 'permian', 'others', 'Total'], axis = 1)
    dfdr1.columns = ['date', 'Drilled']
    dfco1 = dfco.drop(['date', 'activity', 'bakken', 'eagle_ford', 'haynesville', 'permian', 'others', 'Total'], axis = 1)
    dfco1.columns = ['Completed']
    dfap = pd.concat([dfdr1, dfco1], axis = 1, join = 'inner')

    dfdr2 = dfdr.drop(['activity', 'appalachia', 'eagle_ford', 'haynesville', 'permian', 'others', 'Total'], axis = 1)
    dfdr2.columns = ['date', 'Drilled']
    dfco2 = dfco.drop(['date', 'activity', 'appalachia', 'eagle_ford', 'haynesville', 'permian', 'others', 'Total'], axis = 1)
    dfco2.columns = ['Completed']
    dfba = pd.concat([dfdr2, dfco2], axis = 1, join = 'inner')

    dfdr3 = dfdr.drop(['activity', 'appalachia', 'bakken', 'haynesville', 'permian', 'others', 'Total'], axis = 1)
    dfdr3.columns = ['date', 'Drilled']
    dfco3 = dfco.drop(['date', 'activity', 'appalachia', 'bakken', 'haynesville', 'permian', 'others', 'Total'], axis = 1)
    dfco3.columns = ['Completed']
    dfea = pd.concat([dfdr3, dfco3], axis = 1, join = 'inner')

    dfdr4 = dfdr.drop(['activity', 'appalachia', 'bakken', 'eagle_ford', 'permian', 'others', 'Total'], axis = 1)
    dfdr4.columns = ['date', 'Drilled']
    dfco4 = dfco.drop(['date', 'activity', 'appalachia', 'bakken', 'eagle_ford', 'permian', 'others', 'Total'], axis = 1)
    dfco4.columns = ['Completed']
    dfha = pd.concat([dfdr4, dfco4], axis = 1, join = 'inner')

    dfdr5 = dfdr.drop(['activity', 'appalachia', 'bakken', 'eagle_ford', 'haynesville', 'others', 'Total'], axis = 1)
    dfdr5.columns = ['date', 'Drilled']
    dfco5 = dfco.drop(['date', 'activity', 'appalachia', 'bakken', 'eagle_ford', 'haynesville', 'others', 'Total'], axis = 1)
    dfco5.columns = ['Completed']
    dfpe = pd.concat([dfdr5, dfco5], axis = 1, join = 'inner')

    dfdr6 = dfdr.drop(['activity', 'appalachia', 'bakken', 'eagle_ford', 'haynesville', 'permian', 'Total'], axis = 1)
    dfdr6.columns = ['date', 'Drilled']
    dfco6 = dfco.drop(['date', 'activity', 'appalachia', 'bakken', 'eagle_ford', 'haynesville', 'permian', 'Total'], axis = 1)
    dfco6.columns = ['Completed']
    dfot = pd.concat([dfdr6, dfco6], axis = 1, join = 'inner')

    return dfCO, dfNG, imagePaths, crude, df, imagePaths2, dfri, dfdr, dfco, dfdu, dfap, dfba, dfea, dfha, dfpe, dfot


dfCO, dfNG, imagePaths, crude, df, imagePaths2, dfri, dfdr, dfco, dfdu, dfap, dfba, dfea, dfha, dfpe, dfot = refreshData()

imageNames = tuple(i[-11:-4] for i in imagePaths)
imageNames2 = tuple(i[-11:-4] for i in imagePaths2)



##### create web
# delete extra space on the top of page
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)
# set selectbox
st.markdown(
            """
            <style>
                .stSelectbox > div { width: 20%; margin-left: 80%;}
            </style>
            """, unsafe_allow_html=True)
# set tab font
st.markdown("""
            <style>
                .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {font-size:200%; font-family:\"Calibri\"; 
                                                                                                font-weight:bold;}
            </style>
            """, unsafe_allow_html=True)
# set image size when zoom out
st.markdown(
    """
    <style>
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)
# set image center
st.markdown(
    """
    <style>
        [data-testid="stImage"] { 
            text-align:center;
            display:block; 
            margin-left:auto; 
            margin-right:auto;
            width=100%;}
    </style>
    """, unsafe_allow_html=True
)

# create big tab for the page
mainTab1, mainTab2 = st.tabs(['EIA Production', 'Upstream Activity'])


with mainTab1:
    # create col to organize the layout
    col1, col2, col3 = st.columns([0.06, 0.88, 0.06], gap='medium', vertical_alignment="center")

    # inital session state
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    # add select box
    option = st.selectbox('select image', imageNames, index=st.session_state.counter, label_visibility='hidden', key='production')

    # col1 element
    with col1:
        # add left angle button
        def left():
            st.session_state.counter = imageNames.index(option)
            st.session_state.counter -= 1
            if st.session_state.counter < 0:
                st.session_state.counter = len(imagePaths)-1

        pic = imagePaths[st.session_state.counter]
        st.button('◀', on_click=left)

    with col3:
        # add right angle button
        def right():
            st.session_state.counter = imageNames.index(option)
            st.session_state.counter += 1
            if st.session_state.counter > len(imagePaths)-1:
                st.session_state.counter = 0

        pic = imagePaths[st.session_state.counter]
        st.button('▶', on_click=right)

    with col2:
        # add image
        if option:
            st.image(folderimg + '\\' + option + '.jpg')

    tab1, tab2 = st.tabs(["Crude Oil", "Natural Gas"])
    with tab1:
        # plot CO data figure
        COdata = dfCO[['date',  'bakken', 'niobrara', 'permian','anadarko','eagleFord', 'other']]
        COdata.columns = ['date', 'Bakken', 'Niobrara', 'Permian','Anadarko','Eagle Ford', 'Other']
        COdata = COdata.iloc[::-1]

        # stack graph
        fig = pex.area(COdata, x='date', y=['Anadarko', 'Other', 'Niobrara', 'Eagle Ford', 'Bakken', 'Permian'])

        # line graph 
        color_map = {'L48': 'black'}
        crude_color = crude['L48'].map(color_map)

        fig.add_trace(go.Scatter(x=crude['date'], y=crude['L48'], name='US prod', line=dict(color='black')))

        # US prod
        # forecast
        fig.update_layout(legend=dict(
            y=1,
            xanchor="right",
            x=-0.05,
            traceorder="reversed",
        ), hovermode='x unified')

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeslider_thickness = 0.1,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        fig.update_traces(mode="lines", hovertemplate=None)
        st.plotly_chart(fig, user_container_width=True)

    with tab2:
        # plot NG figure
        NGdata = dfNG[['date', 'bakken', 'niobrara', 'permianimg','anadarko', 'appalachia', 'haynesville', 'eagle_ford', 'other']]
        NGdata.columns = ['date', 'Bakken', 'Niobrara', 'Permian','Anadarko', 'Appalachia', 'Haynesville', 'Eagle Ford', 'Other']
        NGdata = NGdata.iloc[::-1]

        fig1 = pex.area(NGdata, x='date', y=['Other', 'Bakken', 'Niobrara', 'Eagle Ford', 'Anadarko', 'Haynesville', 'Permian', 'Appalachia'])

        fig1.update_layout(legend=dict(
            y=1,
            xanchor="right",
            x=-0.05,
            traceorder="reversed",
        ), hovermode='x unified')

        fig1.update_xaxes(
            rangeslider_visible=True,
            rangeslider_thickness = 0.1,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        fig1.update_traces(mode="lines", hovertemplate=None)
        st.plotly_chart(fig1, user_container_width=True)

with mainTab2:
    # create col to organize the layout
    col4, col5, col6 = st.columns([0.06, 0.88, 0.06], gap='medium', vertical_alignment="center")

    # inital session state
    if 'counter1' not in st.session_state:
        st.session_state.counter1 = 0

    # add select box
    option1 = st.selectbox('select image', imageNames2, index=st.session_state.counter1, label_visibility='hidden', key='activity')
 
    with col4:
         # add left angle button
        def left():
            st.session_state.counter1 = imageNames2.index(option1)
            st.session_state.counter1 -= 1
            if st.session_state.counter1 < 0:
                st.session_state.counter1 = len(imagePaths2)-1

        pic1 = imagePaths2[st.session_state.counter1]
        st.button('◀', on_click=left, key='tab2button1')

    with col6:
        # add right angle button
        def right():
            st.session_state.counter1 = imageNames2.index(option1)
            st.session_state.counter1 += 1
            if st.session_state.counter1 > len(imagePaths2)-1:
                st.session_state.counter1 = 0

        pic1 = imagePaths2[st.session_state.counter1]
        st.button('▶', on_click=right, key='tab2button2')

    with col5:
        # add image
        if option:
            st.image(folderimg2 + '\\' + option1 + '.jpg')
    
    tab3, tab4 = st.tabs(["Activity", "DUC"])

    with tab3:
        # draw the graph
        fig2 = make_subplots(rows=3, cols=2, 
                            shared_xaxes=True, 
                            vertical_spacing=0.08, 
                            shared_yaxes=True,
                            horizontal_spacing=0.03,
                            subplot_titles=('Appalachia', "Bakken", "Eagle Ford", "Haynesvile", "Permian", "Others"

                                        ))

        fig2.append_trace(go.Scatter(x=dfap.date, y=dfap['Drilled'], name='Drilled Well Per Month, Appalachia',                                   fill='tozeroy', 
                                        fillcolor='rgba(250,0,0,0.4)',
                                        mode='none'                      
                                ), row=1, col=1)


        fig2.append_trace(go.Scatter(x=dfap.date, y=dfap['Completed'], name='Completed Well Per Month, Appalachia',                                   fill='tozeroy', 
                                        fillcolor='rgba(100,200,200,0.4)',
                                        mode='none'                      
                                ), row=1, col=1)

        fig2.append_trace(go.Scatter(x=dfba.date, y=dfba['Drilled'], name='Drilled well per month, Bakken',                                   fill='tozeroy', 
                                        fillcolor='rgba(250,0,0,0.4)',
                                        mode='none'                      
                                ), row=1, col=2)

        fig2.append_trace(go.Scatter(x=dfba.date, y=dfba['Completed'], name='Completed Well Per Month, Bakken',                                   fill='tozeroy', 
                                        fillcolor='rgba(100,200,200,0.4)',
                                        mode='none'                      
                                ), row=1, col=2)

        fig2.append_trace(go.Scatter(x=dfea.date, y=dfea['Drilled'], name='Drilled Well Per Month, Eagle Ford',                                   fill='tozeroy', 
                                        fillcolor='rgba(250,0,0,0.4)',
                                        mode='none'                      
                                ), row=2, col=1)


        fig2.append_trace(go.Scatter(x=dfea.date, y=dfea['Completed'], name='Completed Well Per Month, Eagle Ford',                                   fill='tozeroy', 
                                        fillcolor='rgba(100,200,200,0.4)',
                                        mode='none'                      
                                ), row=2, col=1)

        fig2.append_trace(go.Scatter(x=dfha.date, y=dfha['Drilled'], name='Drilled Well Per Month, Haynesvile',                                   fill='tozeroy', 
                                        fillcolor='rgba(250,0,0,0.4)',
                                        mode='none'                      
                                ), row=2, col=2)


        fig2.append_trace(go.Scatter(x=dfha.date, y=dfha['Completed'], name='Completed Well Per Month, Haynesvile',                                   fill='tozeroy', 
                                        fillcolor='rgba(100,200,200,0.4)',
                                        mode='none'                      
                                ), row=2, col=2)

        fig2.append_trace(go.Scatter(x=dfpe.date, y=dfpe['Drilled'], name='Drilled Well Per Month, Permian',                                   fill='tozeroy', 
                                        fillcolor='rgba(250,0,0,0.4)',
                                        mode='none'                      
                                ), row=3, col=1)


        fig2.append_trace(go.Scatter(x=dfpe.date, y=dfpe['Completed'], name='Completed Well Per Month, Permian',                                   fill='tozeroy', 
                                        fillcolor='rgba(100,200,200,0.4)',
                                        mode='none'                      
                                ), row=3, col=1)

        fig2.append_trace(go.Scatter(x=dfot.date, y=dfot['Drilled'], name='Drilled Well Per Month, Others',                                   fill='tozeroy', 
                                        fillcolor='rgba(250,0,0,0.4)',
                                        mode='none'                      
                                ), row=3, col=2)

        fig2.append_trace(go.Scatter(x=dfot.date, y=dfot['Completed'], name='Completed Well Per Month, Others',                                   fill='tozeroy', 
                                        fillcolor='rgba(100,200,200,0.4)',
                                        mode='none'                   
                                ), row=3, col=2)

        fig2.update_layout(legend=dict(
            y=1,
            xanchor="right",
            x=-0.05,
            traceorder="reversed",
        ), hovermode='x unified')
        st.plotly_chart(fig2, user_container_width=True)

       

    with tab4:
        # plot dpr data figure
        dprdata = dfdu[['date',  'bakken', 'permian', 'eagle_ford', 'haynesville', 'appalachia', 'others', 'Total']]
        dprdata.columns = ['date', 'Bakken', 'Permian', 'Eagle Ford', 'Haynesville', 'Appalachia', 'Other', 'Total']
        dprdata = dprdata.iloc[::-1]

        # stack graph
        fig = pex.area(dprdata, x='date', y=['Bakken', 'Permian', 'Eagle Ford', 'Haynesville', 'Appalachia', 'Other', 'Total'])

        fig.update_layout(legend=dict(
            y=1,
            xanchor="right",
            x=-0.05,
            traceorder="reversed",
        ), hovermode='x unified')

        fig.update_xaxes(
        rangeslider_visible=True,
        rangeslider_thickness = 0.1,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
                ])
            )
        )

        fig.update_traces(mode="lines", hovertemplate=None)
        st.plotly_chart(fig, user_container_width=True)

        
