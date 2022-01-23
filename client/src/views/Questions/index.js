import React, {useEffect, useState} from "react";
import {Stack} from "@mui/material";
import SearchBar from "../../components/SearchBar";
import QuestionResult from "../../components/QuestionResult";
import questionApi from "../../services/question";


export default function Questions() {
    const topK = 7;
    const [loading, setLoading] = useState(false);
    const [questions, setQuestions] = useState([]);

    useEffect(() => {
        document.title = `Questions :: ${process.env.REACT_APP_TITLE}`
    }, []);

    const handleSearch = async (query) => {
        setLoading(true);
        const response = await questionApi.getSimilarQuestions(query, topK);
        setQuestions(response.data);
        setLoading(false);
    }

    return (
        <div className="Questions">
            <SearchBar label="Search similar questions..." handleSearch={handleSearch}/>
            <Stack sx={{mt: 6}}>
                {
                    (loading)
                        ? [...Array(topK).keys()].map(key =>
                            <QuestionResult sx={{mb:2}}
                                            loading={true}
                                            key={key}/>
                        )
                        : questions.map(item =>
                            <QuestionResult
                                key={item.id}
                                sx={{mb:2}}
                                question={item.text}
                                createdAt="September 3, 2015"
                                score={item.score}/>
                        )
                }

            </Stack>
            {(questions.length === 0 && !loading) &&
                <div>
                    <center>Please input the question and click search.</center>
                </div>
            }

        </div>
    )
}
