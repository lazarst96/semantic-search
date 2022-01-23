import './App.css';
import {Routes, Route, Link} from "react-router-dom";

import Home from "./views/Home";
import Questions from "./views/Questions";
import NotFound from "./views/NotFound";
import {AppBar, Box, Button, Container, Toolbar, Typography} from "@mui/material";
import Answers from "./views/Answers";

function App() {
    return (
        <div className="App">
            <AppBar position='static' color="transparent">
                <Container maxWidth="xl">
                    <Toolbar disableGutters color='white'>
                        <Typography
                            variant="h5"
                            noWrap
                            component="div"
                            sx={{mr: 2, display: {xs: 'none', md: 'flex'}, flexGrow: 1, textDecoration:'none'}}>
                            <Link to={"/"} className="App-link">
                                {process.env.REACT_APP_TITLE || "Semantic Q&A Search"}
                            </Link>
                        </Typography>
                        <Box sx={{ml: 4, display: {xs: 'none', md: 'flex'}}}>
                            <Button
                                component={Link}
                                to='/similar-questions'
                                variant="text"
                                key="SimilarQuestions"
                                sx={{
                                    my: 2,
                                    color: 'black',
                                    display: 'block',
                                    textTransform: 'capitalize',
                                    fontWeight: 'thin'
                                }}>
                                <Typography
                                    variant="subtitle1"
                                    noWrap
                                    component="span">
                                    Similar Questions
                                </Typography>
                            </Button>

                            <Button
                                component={Link}
                                to='/question-answering'
                                variant="text"
                                key="Answers"
                                sx={{
                                    my: 2,
                                    ml: 4,
                                    color: 'black',
                                    display: 'block',
                                    textTransform: 'capitalize',
                                    fontWeight: 'thin',
                                    textDecoration: 'none'
                                }}>
                                <Typography
                                    variant="subtitle1"
                                    noWrap
                                    component="span">Question Answering</Typography>
                            </Button>
                        </Box>
                    </Toolbar>
                </Container>
            </AppBar>
            <Container maxWidth="xl">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/similar-questions" element={<Questions/>}/>
                    <Route path="/question-answering" element={<Answers/>}/>
                    <Route path="*" element={<NotFound/>}/>
                </Routes>
            </Container>
        </div>
    );
}

export default App;
