import React from 'react'
import MovieCard from '../movieCard/MovieCard'
import  Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'


import './moviesContainer.scss'

export default class MoviesContainer extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      movies: []
    }
  }

  componentDidMount() {
    this.setState({ movies: this.props.movies })
  }


  render() {
    const { movies } = this.state

    return(
      <Grid item xs={8}>
        <Typography variant="h6" color="primary">{`Query results: ${movies.length} movies`}</Typography>

        {movies.map((movie, idx) => (
          <MovieCard
            key={idx}
            title={movie.title}
            description={movie.description}
            info={movie.info}
          />
        ))
      }
      </Grid>
    )
  }
}
