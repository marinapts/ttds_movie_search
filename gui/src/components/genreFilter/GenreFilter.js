import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { ButtonGroup, Button } from '@material-ui/core'

import './genreFilter.scss'

export default class GenreFilter extends Component {
  constructor(props) {
    super(props)
    this.state = {
      variants: {},
      selectedGenres: []
    }
  }

  componentWillMount() {
    const variants = {}
    this.props.genres.forEach(genre => {
      variants[genre] = 'text'
    })
    this.setState({ variants })
  }

  filterByGenre = (genre) => {
    const { variants } = this.state

    const selectedGenres = Object.keys(variants).filter(genre => {
      const variant = variants[genre]
      return variant === 'contained'
    })

    // Unselect the genre if clicked twice
    for (let variant in variants) {
      if (!(variant in selectedGenres)) {
        variants[variant] = 'text'
      }
    }

    if (!(selectedGenres.includes(genre))) {
      variants[genre] = 'contained'
    }

    this.setState({ variants }, () => this.props.filterByGenre(variants))
  }

  render() {
    const { genres } = this.props

    return(
      <ButtonGroup color="primary" aria-label="primary button group">
      {
        genres.map((genre, value) =>
          <GenreButton
            key={genre}
            genre={genre}
            variant={this.state.variants[genre]}
            filterByGenre={this.filterByGenre}
          />
        )
      }
      </ButtonGroup>
    )
  }
}


class GenreButton extends Component {
  onGenreClick = genre => {
    this.props.filterByGenre(genre)
  }

  render() {
    const { genre, variant } = this.props

    return(
      <Button
        variant={variant}
        color="primary"
        id={genre}
        onClick={() => this.onGenreClick(genre)}>{genre}</Button>
    )
  }
}


GenreFilter.propTypes = {
  genres: PropTypes.array.isRequired,
  filterByGenre: PropTypes.func.isRequired
}
