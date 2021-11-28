import React from "react";
import {Avatar, Card, CardHeader, Stack, Typography} from "@mui/material";
import {blue} from "@mui/material/colors";
import SearchBar from "../../components/SearchBar";

export default class Questions extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    handleSearch = (query) => {
        console.log(query);
    }

    render() {
        return (
            <div className="Questions">
                <SearchBar label="Search similar questions..." handleSearch={this.handleSearch.bind(this)}/>
                <Stack sx={{mt: 6}}>
                    <Card variant='outlined'>
                        <CardHeader title="How to write letter of complain?"
                                    subheader="September 14, 2016"
                                    avatar={
                                        <Avatar sx={{bgcolor: blue[400], width:'50px', height: '50px'}} aria-label="recipe">
                                            <Typography>0.65</Typography>
                                        </Avatar>
                                    }/>
                        {/*<CardContent>*/}

                        {/*</CardContent>*/}
                    </Card>
                </Stack>

            </div>
        )
    }
}