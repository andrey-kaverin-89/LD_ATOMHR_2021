

import axios from "axios"

const url_api = 'https://russianprogrammer.pythonanywhere.com/atom/api/v1/'

export default {

    auth(login = 'demouser', pass = 'demopass') {
        return axios.post(url_api + 'auth', {
            username: login,
            password: pass
        }).then( res => {
            return res?.data?.result?.access_token
        })
    },

    upload(file, token) {
        let formData = new FormData()
        formData.append('file', file)
        return axios.post(url_api + 'uploadfile', formData).then( res => {
            return res?.data?.result?.columns
        })
    },
    
    feature_importances(keys = ["gender","absence"]) {
        return axios.get(url_api + 'get_feature_importances', {
            params: keys
        }).then( res => {
            return res?.data?.result?.columns
        })
    }
}