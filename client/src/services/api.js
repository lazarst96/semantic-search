import axios from 'axios';
import snakecaseKeys from "snakecase-keys";
import camelcaseKeys from "camelcase-keys";


const _axios = axios.create({
    baseURL: process.env.REACT_APP_API_ROOT,
    withCredentials: false,
    headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
});

_axios.defaults.transformResponse = [(data, headers) => {
    if (data && headers['content-type'].includes('application/json')) {
        return camelcaseKeys(JSON.parse(data), {deep: true})
    }
}];

_axios.defaults.transformRequest = [(data, headers) => {
    if (data && headers['Content-Type'].includes('application/json')) {
        return JSON.stringify(snakecaseKeys(data, {deep: true}))
    }
}];

export default _axios;