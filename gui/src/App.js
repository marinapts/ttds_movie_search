import React, { Component, Fragment } from 'react'
import Container from '@material-ui/core/Container'
import Skeleton from '@material-ui/lab/Skeleton'
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles'

import SearchInput from './components/searchInput/SearchInput'
import MoviesContainer from './components/moviesContainer/MoviesContainer'

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
      movies: [],
      showCards: false
    }
  }

  getMoviesForQuery = data => {
    console.log(data)
    this.setState({
      showCards: true,
      movies: data.movies,
      genres: data.category_list
    })
  }

  render() {
    const { showCards, movies, genres } = this.state

    return (
      <ThemeProvider theme={darkTheme}>
        <Container className="app">
          <h3>TTDS Movie Project 2020</h3>
          <div className="search-container">
            <SearchInput getMoviesForQuery={this.getMoviesForQuery} />
          </div>
          {showCards &&
            <Fragment>
              {movies.length > 0 ?
                <MoviesContainer data={movies} genres={genres} /> :
                <Fragment>
                  {Array.apply(null, { length: 5 }).map((e, i) => (
                    <Skeleton variant="rect" width={790} height={170} className="skeleton-card" />
                  ))}
                </Fragment>
              }
            </Fragment>
          }
        </Container>
      </ThemeProvider>
    )
  }
}
