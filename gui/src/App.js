import React, { Component } from 'react'
import SearchInput from './components/searchInput/SearchInput'
import Container from '@material-ui/core/Container';
import MoviesContainer from './components/moviesContainer/MoviesContainer'
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles'

import './app.scss'

const darkTheme = createMuiTheme({
  palette: {
    type: 'dark',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      light: '#cc33ff',
      main: '#e699ff',
      contrastText: '#ffcc00',
    }
  },
});

export default class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      movies: []
    }
  }

  getMoviesForQuery = data => {
    this.setState({ movies: data.movies })
  }

  render() {
    const { movies } = this.state

    return (
      <ThemeProvider theme={darkTheme}>
        <Container className="app">
          <h3>TTDS Movie Project 2020</h3>
          <div className="search-container">
            <SearchInput getMoviesForQuery={this.getMoviesForQuery} />
          </div>
          {movies.length > 0 && <MoviesContainer movies={movies} /> }
        </Container>
      </ThemeProvider>
    )
  }
}
