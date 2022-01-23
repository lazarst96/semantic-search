import {Avatar, Card, CardHeader, Typography} from "@mui/material";
import {blue} from "@mui/material/colors";
import React from "react";
import SkeletonLoader from "./skeletonLoader";


export default function QuestionResult({loading = false, question, createdAt, score, sx}) {
    return (
        <Card variant='outlined' sx={sx}>
            {loading
                ? <SkeletonLoader/>
                : <CardHeader title={question}
                              subheader={createdAt}
                              avatar={
                                  <Avatar sx={{bgcolor: blue[400], width: '50px', height: '50px'}}>
                                      <Typography>{score.toFixed(2)}</Typography>
                                  </Avatar>
                              }/>
            }
        </Card>
    )
}