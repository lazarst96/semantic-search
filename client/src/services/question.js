import Api from './api';

const route = 'questions';

const questionApi = {
    getSimilarQuestions(question, n = 5) {
        return Api.get(`${route}/${escape(question)}/similar`, {params: {top_k: n}});
    }
};

export default questionApi;