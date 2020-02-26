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

    this.setState({ data, showDetails: false })
  }

  viewMovieInfoCard = async movieId => {
    const response = await API.get(`/movie/${movieId}`)
    console.log(response)
    let errorMovieInfoMsg = ''
    let movieInfo = {}

    if (response.status === 404) {
      errorMovieInfoMsg = 'Movie could not be retrieved! Please click on another movie'
    } else {
      movieInfo = response.data
    }

    this.setState({ showDetails: true, movieInfo, errorMovieInfoMsg })
  }

  handleClick = (offset) => {
    this.setState({ offset })
  }

  render() {
    const { showDetails, data, offset, perPage, movieInfo, errorMovieInfoMsg } = this.state
    const { genres } = this.props

    return(
      <div>
        <Grid container className="movies-container" spacing={6}>
          {data.length > 0 &&
            <Grid item xs={12}><GenreFilter genres={genres} filterByGenre={this.filterByGenre} /></Grid>
          }

          <Grid item xs={8}>
            <Typography variant="h6" color="primary">{`Query results: ${data.length} movies`}</Typography>

            {data.slice(offset, offset + perPage).map((movie, idx) =>
              <MovieCard key={idx} viewDetails={this.viewMovieInfoCard} {...movie} />
            )}
          </Grid>

          {showDetails &&
            <Grid item xs={4}>
              <Zoom in={showDetails} style={{ transitionDelay: showDetails ? '100ms' : '0ms' }}>
                <DetailsCard details={movieInfo} errorMovieInfoMsg={errorMovieInfoMsg} />
              </Zoom>
            </Grid>
          }
        </Grid>
        {data.length > 0 &&
          <Pagination
            limit={perPage}
            offset={offset}
            total={data.length}
            onClick={(e, offset) => this.handleClick(offset)}
          />
        }
      </div>
    )
  }
}

MoviesContainer.propTypes = {
  movies: PropTypes.array.isRequired,
  genres: PropTypes.array.isRequired
}
