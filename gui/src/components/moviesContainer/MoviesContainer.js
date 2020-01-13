import React from 'react'
import PropTypes from 'prop-types'
import MovieCard from '../movieCard/MovieCard'
import  Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'


import './moviesContainer.scss'

export default class MoviesContainer extends React.Component {
  render() {
    const { movies } = this.props

    return(
      <Grid item xs={8}>
        <Typography variant="h6" color="primary">{`Query results: ${movies.length} movies`}</Typography>

        {movies.map((movie, idx) => (
          <MovieCard key={idx} {...movie} />
        ))
      }
      </Grid>
    )
  }
}

MoviesContainer.propTypes = {
  movies: PropTypes.array.isRequired
}
