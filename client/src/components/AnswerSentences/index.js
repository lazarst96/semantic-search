import React from "react";
import {Card, CardContent, Skeleton} from "@mui/material";
import "./style.scss";
import PropTypes from "prop-types";

class AnswerSentences extends React.Component {

    renderSentence(sentence, key) {
        const className = "Sentence" + ((sentence.selected) ? " Sentence-selected" : "");
        return (
            <span className={className}
                  key={key}>
                {sentence.text}
            </span>
        )
    }

    renderSkeletonLoader() {
        const lengths = ['60%', '35%', '40%', '40%', '30%', '60%', '70%'];

        const sent1Id = Math.floor(Math.random() * 7);
        const sent2Id = Math.floor(Math.random() * 7);
        return (
            <CardContent>
                {lengths.map((l, key) => (
                    <Skeleton variant="text"
                              animation='wave'
                              key={key}
                              width={l}
                              sx={{
                                  display: "inline-block",
                                  mr: 2,
                                  ...((sent1Id === key || sent2Id === key)?
                                      {bgcolor: "aquamarine"}:
                                      {})
                              }}/>
                ))}
            </CardContent>
        )
    }

    render() {
        return (
            <Card className="AnswerSentences"
                  variant="outlined"
                  sx={{fontSize: '1.2rem', ...this.props.sx}}>
                {!this.props.loading ? (
                        <CardContent sx={{px: '30px', wordBreak: "break-word"}}>
                            {this.props.sentences.map((s, index) => (
                                this.renderSentence(s, index)
                            ))}
                        </CardContent>
                    ) :
                    this.renderSkeletonLoader()}
            < /Card>
        )
    }
}

AnswerSentences.propTypes = {
    sentences: PropTypes.array,
    sx: PropTypes.object,
    loading: PropTypes.bool
};

AnswerSentences.defaultProps = {
    sentences: [],
    sx: {},
    loading: false
};

export default AnswerSentences;