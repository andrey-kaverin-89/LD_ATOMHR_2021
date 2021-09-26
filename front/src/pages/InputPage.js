import React, { useState } from 'react';
// import { Alert, Button, Spin } from 'antd';
// import { useQuery } from '@apollo/react-hooks';
import { withRouter } from 'react-router-dom';
// import ExploreQueryBuilder from '../components/QueryBuilder/ExploreQueryBuilder';
// import { GET_DASHBOARD_ITEM } from '../graphql/queries';
// import TitleModal from '../components/TitleModal.js';
// import { Icon } from '@ant-design/compatible';


// import React from 'react';
// import { Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar, ComposedChart, Area, AreaChart,
  // LineChart, ResponsiveContainer, PieChart, Pie, Label, Cell
// } from 'recharts';
// import cubejs from '@cubejs-client/core';
// import { QueryRenderer } from '@cubejs-client/react';



import { Upload, message, Spin, Input } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import axios from 'axios';
import api from '../api/api';

const { Dragger } = Upload;

const props = {
  name: 'file',
  multiple: false,
//   action: () => {
    // return api.auth().then(res => {console.log('res', res); return true},console.log)
//   },
//   data: (f) => {
//     console.log('upload', f)
//     return api.auth().then(token => {
//         api.upload(f, token).then(res => {
//             console.log(res)
//             message.success(`file uploaded successfully.`);
//         })
//     },console.log)
//   },
//   onChange(info) {
    // const { status } = info.file;
    // if (status !== 'uploading') {
    //   console.log(info.file, info.fileList);
    // }
    // if (status === 'done') {
    //   message.success(`${info.file.name} file uploaded successfully.`);
    // } else if (status === 'error') {
    // //   message.error(`${info.file.name} file upload failed.`);
    //   message.success(`file uploaded successfully.`);
    // }
//   },
//   onDrop(e) {
    // console.log('Dropped files', e.dataTransfer.files);
    // return api.auth().then(res => {
    //     message.success(`file uploaded successfully.`);
    // },console.log)
//   },
  showUploadList: false
};


const InputPage = withRouter(({ history, location }) => {

    const [cols, set_cols] = useState([])
    const [is_loading, set_is_loading] = useState(false)

    const onLoad = (f) => {
        console.log('upload', f)
        set_is_loading(true)
        return api.auth().then(token => {
            api.upload(f, token).then(res => {
                console.log(res)
                set_is_loading(false)
                set_cols(res)
                message.success(`file uploaded successfully.`);
            })
        },console.log)
    }
    
  return (
    <div style={{margin:50}}>

        <Dragger {...props} data={onLoad}>
            <p className="ant-upload-drag-icon">
                <InboxOutlined />
            </p>
            <p className="ant-upload-text">Click or drag file to this area to upload</p>
            <p className="ant-upload-hint">
            Support for a single or bulk upload. Strictly prohibit from uploading company data or other
            band files
            </p>
        </Dragger>

        <br/>
        <br/>

        { is_loading ? 
            <div style={{textAlign:'center'}}><Spin size="large" /></div> 
            : 
            <div>
                {cols.length ? cols.map((x,i)=>(
                    <div key={i}>
                        <Input value={x.name} style={{width:600}} /> {x.type}
                    </div>)) 
                    : ''
                }
            </div>
        }
        

    </div>
  );
});
export default InputPage;
