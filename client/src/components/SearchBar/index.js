import React from "react";
import {Box, Button, TextField} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import PropTypes from 'prop-types';


class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: ''
        }
    }

    handleChange = (prop) => (event) => {
        this.setState({
            [prop]: event.target.value
        });
    }

    handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            if (this.props.handleSearch !== undefined)
                this.props.handleSearch(this.state.value);
        }
    }

    handleSearchButtonClick = () => {
        if (this.props.handleSearch !== undefined)
            this.props.handleSearch(this.state.value);
    }


    render() {
        return (
            <Box sx={{mt: 4, display: "flex", alignItems: "center", justifyContent: "center"}}>
                <TextField type="text"
                           value={this.state.value}
                           sx={{width: '60%'}}
                           onChange={this.handleChange('value').bind(this)}
                           onKeyPress={this.handleKeyPress.bind(this)}
                           label={this.props.label}/>
                <Button variant='outlined'
                        sx={{ml: 2}}
                        startIcon={<SearchIcon/>}
                        onClick={this.handleSearchButtonClick.bind(this)}>
                    Search
                </Button>
            </Box>
        )
    }
}

SearchBar.propTypes = {
    label: PropTypes.string,
    handleSearch: PropTypes.func
}

export default SearchBar;