import React from 'react'
import PropTypes from 'prop-types'
import { Grid, Zoom, Typography } from '@material-ui/core'
import Pagination from 'material-ui-flat-pagination'

import MovieCard from '../movieCard/MovieCard'
import DetailsCard from '../detailsCard/DetailsCard'
import GenreFilter from '../genreFilter/GenreFilter'
import API from '../../utils/API'

import './moviesContainer.scss'

export default class MoviesContainer extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: [],
      showDetails: false,
      quoteId: null,
      offset: 0,
      perPage: 10,
      errorMovieInfoMsg: '',
      movieInfo: {}
    }
  }

  componentDidMount() {
    this.setState({ data: this.props.data, showDetails: false })
  }

  filterByGenre = genres => {
    let data = this.props.data
    const selectedGenre = Object.keys(genres).filter(genre => genres[genre] === 'contained')

    // Filter data if there is a selected genre
    if (selectedGenre.length) {
      data = data.filter(d => d.categories.includes(selectedGenre[0]))
    }

    this.setState({ data, showDetails: false, offset: 0 })
  }

  viewMovieInfoCard = async movieId => {
    let errorMovieInfoMsg = ''
    let movieInfo = {}
    try {
      const response = await API.get(`/movie/${movieId}`)
      movieInfo = response.data
    } catch(error) {
      errorMovieInfoMsg = 'Movie not found'
      movieInfo = {}
    }

    this.setState({ showDetails: true, movieInfo, errorMovieInfoMsg })
  }

  handleClick = (offset) => {
    this.setState({ offset })
  }

  render() {
    const { showDetails, data, offset, perPage, movieInfo, errorMovieInfoMsg } = this.state
    const { genres, queryTime } = this.props
    const time = (Math.round(queryTime * 100) / 100).toFixed(3)

    return(
      <div>
        <Grid container className="movies-container" spacing={6}>
          {data.length > 0 &&
            <Grid item xs={12}><GenreFilter genres={genres} filterByGenre={this.filterByGenre} /></Grid>
          }

          <Grid item xs={8}>
            <Typography variant="body1" className="query-results">{`Query results: ${data.length} movies (${time} seconds)`}</Typography>

            {data.length > perPage &&
              <Pagination
                limit={perPage}
                offset={offset}
                total={data.length}
                currentPageColor="primary"
                onClick={(e, offset) => this.handleClick(offset)}
              />
            }

            {data.slice(offset, offset + perPage).map((movie, idx) =>
              <MovieCard key={idx} viewDetails={this.viewMovieInfoCard} {...movie} />
            )}

            {data.length > perPage &&
              <Pagination
                limit={perPage}
                offset={offset}
                total={data.length}
                currentPageColor="primary"
                onClick={(e, offset) => this.handleClick(offset)}
              />
            }
          </Grid>

          {showDetails &&
            <Grid item xs={4}>
              <Zoom in={showDetails} style={{ transitionDelay: showDetails ? '100ms' : '0ms' }}>
                <DetailsCard details={movieInfo} errorMovieInfoMsg={errorMovieInfoMsg} />
              </Zoom>
            </Grid>
          }
        </Grid>
      </div>
    )
  }
}

MoviesContainer.propTypes = {
  movies: PropTypes.array.isRequired,
  genres: PropTypes.array.isRequired,
  queryTime: PropTypes.number.isRequired
}
