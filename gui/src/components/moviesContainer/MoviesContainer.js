import React from 'react'
import MovieCard from '../movieCard/MovieCard'
import Grid from '@material-ui/core/Grid'

import './moviesContainer.scss'

export default class MoviesContainer extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: []
    }
  }

  componentDidMount() {
    // retrieve movies
    const movies = [
      {
        id: 1,
        title: 'Movie Title 1',
        description: 'Movie Description 1',
        info: 'Movie Info 1',
      },
      {
        id: 2,
        title: 'Movie Title 2',
        description: 'Movie Description 2',
        info: 'Movie Info 2',
      },
      {
        id: 3,
        title: 'Movie Title 3',
        description: 'Movie Description 3',
        info: 'Movie Info 3',
      },
      {
        id: 4,
        title: 'Movie Title 4',
        description: 'Movie Description 4',
        info: 'Movie Info 4',
      }
    ]

    this.setState({ data: movies })
  }


  render() {
    const { data } = this.state

    return(
      <Grid item xs={8}>
        {
          data.map(movie => (
            <MovieCard
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
