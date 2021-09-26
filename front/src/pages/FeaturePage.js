import React, { useState } from 'react';
// import { Alert, Button, Spin } from 'antd';
// import { useQuery } from '@apollo/react-hooks';
import { withRouter } from 'react-router-dom';
// import ExploreQueryBuilder from '../components/QueryBuilder/ExploreQueryBuilder';
// import { GET_DASHBOARD_ITEM } from '../graphql/queries';
// import TitleModal from '../components/TitleModal.js';
// import { Icon } from '@ant-design/compatible';


// import React from 'react';
import { Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar, ComposedChart, Area, AreaChart,
  // LineChart, ResponsiveContainer, PieChart, Pie, Label, Cell
} from 'recharts';
// import cubejs from '@cubejs-client/core';
// import { QueryRenderer } from '@cubejs-client/react';


let feature_importance = [{'feature_name': 'position', 'weight': 0.27355405773323604},
    {'feature_name': 'gender', 'weight': 0.0676824445858595},
    {'feature_name': 'marital_status', 'weight': 0.005355932112053576},
    {'feature_name': 'absence', 'weight': 0.007222197902745777},
    {'feature_name': 'absence_days', 'weight': 0.016202784877002732},
    {'feature_name': 'salary', 'weight': 0.019899357649865324},
    {'feature_name': 'city', 'weight': 0.00015455710752427086},
    {'feature_name': 'children_num', 'weight': 0.009695259458417661},
    {'feature_name': 'age', 'weight': 0.025410265533449987},
    {'feature_name': 'has_mentor', 'weight': 0.003287506827870181},
    {'feature_name': 'experience', 'weight': 0.04702103370147369},
    {'feature_name': 'layoff_month', 'weight': 0.5220385621517538},
    {'feature_name': 'is_large_family', 'weight': 0.00020791262632113546},
    {'feature_name': 'is_retiree', 'weight': 0.0022681277324264433}];
feature_importance.forEach((el)=> {
    el.feature_name = el.feature_name.replace(new RegExp('_', 'g'), ' ')
})
feature_importance.sort((a,b) => (a.weight < b.weight) ? 1 : ((b.weight < a.weight) ? -1 : 0))

let hired_dismissed_months = [
    {'month': 1, 'hired': 10, 'dismissed': 4}, // hired - были приняты на работу в этом месяце, dismissed - были уволены
    {'month': 2, 'hired': 4, 'dismissed': 2},
    {'month': 3, 'hired': 6, 'dismissed': 7},
    {'month': 4, 'hired': 10, 'dismissed': 5},
    {'month': 5, 'hired': 3, 'dismissed': 4},
    {'month': 6, 'hired': 6, 'dismissed': 3},
    {'month': 7, 'hired': 10, 'dismissed': 8},
    {'month': 8, 'hired': 6, 'dismissed': 11},
    {'month': 9, 'hired': 37, 'dismissed': 13},
    {'month': 10, 'hired': 13, 'dismissed': 6},
    {'month': 11, 'hired': 8, 'dismissed': 5},
    {'month': 12, 'hired': 3, 'dismissed': 11},
]
const months = {
    1: 'январь',
    2: 'февраль',
    3: 'март',
    4: 'апрель',
    5: 'май',
    6: 'июнь',
    7: 'июль',
    8: 'август',
    9: 'сентябрь',
    10: 'октябрь',
    11: 'ноябрь',
    12: 'декабрь'
}
hired_dismissed_months.forEach((el)=> {
    el.month_name = months[el.month];
    el.difference = el.hired - el.dismissed;
});

const data_big = [
    {month: 1, woman: 8, man: 11, avg_woman_age: 55, avg_man_age: 64, avg_woman_experience: 27, avg_man_experience: 24},
    {month: 2, woman: 9, man: 14, avg_woman_age: 54, avg_man_age: 63, avg_woman_experience: 27, avg_man_experience: 29},
    {month: 3, woman: 12, man: 14, avg_woman_age: 57, avg_man_age: 63, avg_woman_experience: 29, avg_man_experience: 29},
    {month: 4, woman: 11, man: 13, avg_woman_age: 56, avg_man_age: 60, avg_woman_experience: 27, avg_man_experience: 27},
    {month: 5, woman: 11, man: 13, avg_woman_age: 56, avg_man_age: 60, avg_woman_experience: 27, avg_man_experience: 27},
    {month: 6, woman: 14, man: 13, avg_woman_age: 58, avg_man_age: 60, avg_woman_experience: 30, avg_man_experience: 27},
    {month: 7, woman: 14, man: 8, avg_woman_age: 58, avg_man_age: 57, avg_woman_experience: 30, avg_man_experience: 30},
    {month: 8, woman: 14, man: 11, avg_woman_age: 58, avg_man_age: 59, avg_woman_experience: 30, avg_man_experience: 28},
    {month: 9, woman: 12, man: 13, avg_woman_age: 54, avg_man_age: 57, avg_woman_experience: 28, avg_man_experience: 27},
    {month: 10, woman: 12, man: 13, avg_woman_age: 54, avg_man_age: 57, avg_woman_experience: 28, avg_man_experience: 27},
    {month: 11, woman: 9, man: 14, avg_woman_age: 50, avg_man_age: 56, avg_woman_experience: 27, avg_man_experience: 29},
    {month: 12, woman: 9, man: 14, avg_woman_age: 50, avg_man_age: 56, avg_woman_experience: 27, avg_man_experience: 29}
]
data_big.forEach((el)=> {
    el.month_name = months[el.month];
});

const gradientOffset = () => {
    const dataMax = Math.max(...hired_dismissed_months.map((i) => i.difference));
    const dataMin = Math.min(...hired_dismissed_months.map((i) => i.difference));

    if (dataMax <= 0) {
        return 0;
    }
    if (dataMin >= 0) {
        return 1;
    }

    return dataMax / (dataMax - dataMin);
};

const off = gradientOffset();

const FeaturePage = withRouter(({ history, location }) => {
  return (
    <div>
   

        {/*график feature_importance*/}
        <div style={{marginLeft: "300px", marginTop: "50px"}}>feature importance</div>
        <BarChart layout="vertical" width={900} height={600} data={feature_importance}
                  margin={{
                      top: 20,
                      right: 5,
                      bottom: 20,
                      left: 50
                  }}
        >
            <CartesianGrid stroke="#f5f5f5" />
            <XAxis type="number"   />
            <YAxis type="category" dataKey="feature_name" width={120} />
            <Tooltip />
            <Legend />
            <Bar dataKey="weight" fill="#025EA1"/>
        </BarChart>

        {/*график принятия/увольнения по месяцам*/}
        <div style={{marginLeft: "300px", marginTop: "50px"}}>Принятие/увольнение по месяцам</div>
        <AreaChart width={900} height={300} data={hired_dismissed_months}
                  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
                <linearGradient id="hired" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#B2C541" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#B2C541" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="dismissed" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#EE6C23" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#EE6C23" stopOpacity={0}/>
                </linearGradient>
            </defs>
            <XAxis dataKey="month_name" width={80} />
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Area type="monotone" dataKey="hired" stroke="#B2C541" fillOpacity={1} fill="url(#hired)" />
            <Area type="monotone" dataKey="dismissed" stroke="#EE6C23" fillOpacity={1} fill="url(#dismissed)" />
        </AreaChart>

        {/*график разницы принятых и уволенных по месяцам*/}
        <div style={{marginLeft: "300px", marginTop: "50px"}}>График разницы принятых и уволенных по месяцам</div>
        <AreaChart
            width={900} height={300}
            data={hired_dismissed_months}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month_name" />
            <YAxis />
            <Tooltip />
            <defs>
                <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                    <stop offset={off} stopColor="#B2C541" stopOpacity={1} />
                    <stop offset={off} stopColor="#EE6C23" stopOpacity={1} />
                </linearGradient>
            </defs>
            <Area type="monotone" dataKey="difference" stroke="none" fill="url(#splitColor)" />
        </AreaChart>

        {/*Кол-во женщин/мужчин, средний возраст, среднее кол-во опыта*/}
        <div style={{marginLeft: "300px", marginTop: "50px"}}>Кол-во женщин/мужчин, средний возраст, среднее кол-во опыта</div>
            <ComposedChart
                width={920}
                height={450}
                data={data_big}
                margin={{
                    top: 10,
                    right: 10,
                    bottom: 20,
                    left: 20,
                }}
            >
                <CartesianGrid stroke="#f5f5f5" />
                <XAxis dataKey="month_name" scale="band" />
                <YAxis  />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="avg_woman_experience" fill="rgba(178, 33, 116, 0.4)" stroke="#B22174" />
                <Area type="monotone" dataKey="avg_man_experience" fill="rgba(37, 151, 137, 0.4)" stroke="#259789" />
                <Bar dataKey="woman" barSize={20} fill="#B22174" />
                <Bar dataKey="man" barSize={20} fill="#259789" />
                <Line type="monotone" dataKey="avg_woman_age" stroke="#F0A600" />
                <Line type="monotone" dataKey="avg_man_age" stroke="#EE6C23" />
            </ComposedChart>

        {/*<QueryRenderer*/}
        {/*    // query={{*/}
        {/*    //   measures: ['Stories.count'],*/}
        {/*    //   dimensions: ['Stories.time.month'],*/}
        {/*    // }}*/}
        {/*    render={({ resultSet = [{name: 'a', value: 12}] }) => {*/}
        {/*      if (!resultSet) {*/}
        {/*        return 'Loading...';*/}
        {/*      }*/}

        {/*      return (*/}
        {/*          // <LineChart data={resultSet.rawData()}>*/}
        {/*          //   <XAxis dataKey="Stories.time" />*/}
        {/*          //   <YAxis />*/}
        {/*          //   <Line type="monotone" dataKey="Stories.count" stroke="#8884d8" />*/}
        {/*          // </LineChart>*/}
        {/*        <LineChart width={730} height={250} data={data}*/}
        {/*                   margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>*/}
        {/*            <CartesianGrid strokeDasharray="3 3" />*/}
        {/*            <XAxis dataKey="name" />*/}
        {/*            <YAxis />*/}
        {/*            <Tooltip />*/}
        {/*            <Legend />*/}
        {/*            <Line type="monotone" dataKey="pv" stroke="#8884d8" />*/}
        {/*            <Line type="monotone" dataKey="uv" stroke="#82ca9d" />*/}
        {/*        </LineChart>*/}
        {/*      );*/}
        {/*    }}*/}
        {/*/>*/}



    </div>
  );
});
export default FeaturePage;
