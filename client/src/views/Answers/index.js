import React, {useEffect, useState} from "react";
import SearchBar from "../../components/SearchBar";
import {Stack} from "@mui/material";
import AnswerSentences from "../../components/AnswerSentences";
import answerApi from "../../services/answer";

export default function Answers() {
    const topK = 5;
    const [loading, setLoading] = useState(false);
    const [paragraphs, setParagraphs] = useState([]);

    useEffect(() => {
        document.title = `Answers :: ${process.env.REACT_APP_TITLE}`
    }, []);

    const handleSearch = async (query) => {
        setLoading(true);
        const response = await answerApi.predictAnswers(query);
        setLoading(false);
        setParagraphs(response.data);
    }
    return (
        <div className="Answers">
            <SearchBar label="Ask a question..." handleSearch={handleSearch}/>
            <Stack sx={{mt: 6, width: '70%', mx: "auto"}}>
                {
                    (loading) ?
                        [...Array(topK).keys()].map(doc => (
                            <AnswerSentences loading={true}
                                             key={doc}
                                             sx={{mt: 2}}/>
                        )) :
                        paragraphs.map(doc => (
                            <AnswerSentences loading={false}
                                             sentences={doc.sentences}
                                             key={doc.id}
                                             sx={{mt: 2}}/>
                        ))}

            </Stack>
            {(paragraphs.length === 0 && !loading) &&
                <div>
                    <center>Please input the question and click search.</center>
                </div>
            }
        </div>
    )
}