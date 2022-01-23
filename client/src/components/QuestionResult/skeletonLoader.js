import React from "react";
import {CardHeader, Skeleton} from "@mui/material";


export default function SkeletonLoader() {
    return (
        <CardHeader
            avatar={
                <Skeleton animation="wave" variant="circular" width={50} height={50} />
            }
            title={
                <Skeleton animation="wave" height={10} width="40%" style={{ marginBottom: 6 }}/>
            }
            subheader={
                <Skeleton animation="wave" height={10} width="15%" />
            }
        />
    )
}