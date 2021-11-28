import React from "react";
import SearchBar from "../../components/SearchBar";
import {Stack} from "@mui/material";
import AnswerSentences from "../../components/AnswerSentences";
import answerApi from "../../services/answer";


export default class Answers extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            paragraphs: []
        };
        this.sentences = [
            {text: 'This the first sentence. ', selected: false},
            {text: 'This the second sentence. ', selected: true},
            {text: 'This the third sentence. ', selected: false},
            {text: 'This the third sentence. ', selected: false},
            {text: 'This the third sentence. ', selected: false},
        ];
    }

    handleSearch = async (query) => {
        this.setState({loading: true});
        const response = await answerApi.predictAnswers(query);
        this.setState({
            loading: false,
            paragraphs: response.data
        });
    }

    render() {
        return (
            <div className="Answers">
                <SearchBar label="Ask a question..." handleSearch={this.handleSearch.bind(this)}/>
                <Stack sx={{mt: 6, width: '70%', mx: "auto"}}>
                    {
                        (this.state.loading) ?
                            [1, 2, 3, 4, 5].map(doc => (
                                <AnswerSentences loading={true}
                                                 key={doc}
                                                 sx={{mt: 2}}/>
                            )) :
                            this.state.paragraphs.map(doc => (
                                <AnswerSentences loading={false}
                                                 sentences={doc.sentences}
                                                 key={doc.id}
                                                 sx={{mt: 2}}/>
                            ))}

                </Stack>
            </div>
        )
    }
}