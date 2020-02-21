import React from 'react'
import PropTypes from 'prop-types'
import { Grid, Zoom, Typography } from '@material-ui/core'
import Pagination from 'material-ui-flat-pagination'

import MovieCard from '../movieCard/MovieCard'
import DetailsCard from '../detailsCard/DetailsCard'
import GenreFilter from '../genreFilter/GenreFilter'


import './moviesContainer.scss'

export default class MoviesContainer extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: [],
      showDetails: false,
      quoteId: null,
      offset: 0,
      perPage: 10
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

  viewDetailsCard = quoteId => {
    this.setState({ showDetails: true, quoteId })
  }

  handleClick = (offset) => {
    this.setState({ offset })
  }

  render() {
    const { showDetails, quoteId, data, offset, perPage } = this.state
    const { genres } = this.props

    return(
      <div>
        <Grid container className="movies-container" spacing={6}>
          {data.length > 0 &&
            <Grid item xs={12}><GenreFilter genres={genres} filterByGenre={this.filterByGenre} /></Grid>
          }

          <Grid item xs={8}>
            <Typography variant="body1" className="query-results">{`Query results: ${data.length} movies`}</Typography>

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
              <MovieCard key={idx} viewDetails={this.viewDetailsCard} {...movie} />
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
                <DetailsCard details={data.find(d => d.quote_id === quoteId)} />
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
  genres: PropTypes.array.isRequired
}
