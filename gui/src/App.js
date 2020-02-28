import React, { Component, Fragment } from 'react'
import { Container } from '@material-ui/core'
import Skeleton from '@material-ui/lab/Skeleton'
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles'

import SearchInput from './components/searchInput/SearchInput'
import MoviesContainer from './components/moviesContainer/MoviesContainer'
import API from './utils/API'

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
      showCards: false,
      showExamples: true,
      showErrorMsg: false,
      loading: false,
      queryTime: 0
    }
  }

  performSearch = (data, isMovieSearch) => {
    const { query, movieTitle, actor, year, keywords } = data

    this.setState({ loading: true }, async () => {
      try {
        const response = await API.post(
          isMovieSearch ? '/movie_search' : '/query_search',
          { query, movie_title: movieTitle, actor, year, keywords }
        )
        this.setState({
          movies: response.data.movies,
          genres: response.data.category_list,
          queryTime: response.data.query_time,
          showCards: true,
          showExamples: false,
          loading: false
        })
      } catch (error) {
        // @TODO: Show a proper error message to the user
        console.error(error)
        this.setState({
          showErrorMsg: true,
          showExamples: true,
          loading: false
        })
      }
    })
  }

  render() {
    const { showCards, movies, genres, showExamples, showErrorMsg, loading, queryTime } = this.state

    return (
      <ThemeProvider theme={darkTheme}>
        <Container className="app">
          <h3>TTDS Movie Project 2020</h3>
          <div className="search-container">
            <SearchInput
              performSearch={this.performSearch}
              showExamples={showExamples}
              showErrorMsg={showErrorMsg}
            />
          </div>
          <Fragment>
            {loading ?
              <Fragment>
                {Array.apply(null, { length: 5 }).map((e, i) => (
                  <Skeleton variant="rect" width={790} height={170} className="skeleton-card" />
                ))}
              </Fragment>
              : showCards && <MoviesContainer data={movies} genres={genres} queryTime={queryTime} />
            }
          </Fragment>
        </Container>
      </ThemeProvider>
    )
  }
}
