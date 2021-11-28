import Api from './api';

const route = 'answers';

const answerApi  = {
    predictAnswers(question) {
        return Api.get(`${route}/${escape(question)}`);
    }
};

export default answerApi;