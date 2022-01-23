import React, {useState} from "react";
import {Box, Button, TextField} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

export default function SearchBar({label, handleSearch}) {
    const [value, setValue] = useState('');
    const [loading, setLoading] = useState(false);

    const handleKeyPress = async (event) => {
        if (event.key === 'Enter') {
            if (handleSearch !== undefined) {
                setLoading(true);
                await handleSearch(value);
                setLoading(false);
            }

        }
    }

    const handleSearchButtonClick = async () => {
        if (handleSearch !== undefined) {
            setLoading(true);
            await handleSearch(value);
            setLoading(false);
        }
    }

    return (
        <Box sx={{mt: 4, display: "flex", alignItems: "center", justifyContent: "center"}}>
            <TextField type="text"
                       value={value}
                       sx={{width: '60%'}}
                       onChange={event => setValue(event.target.value)}
                       onKeyPress={handleKeyPress}
                       label={label}/>
            <Button variant='outlined'
                    disabled={loading}
                    sx={{ml: 2}}
                    startIcon={!loading && <SearchIcon/>}
                    onClick={handleSearchButtonClick}>
                {loading ? "Loading..." : "Search"}
            </Button>
        </Box>
    )

};