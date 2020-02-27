import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Grid, FormControlLabel, Switch, TextField, Button, Link, Typography, Checkbox } from '@material-ui/core'

import AdvancedSearch from '../advancedSearch/AdvancedSearch'

import './searchInput.scss'

export default class SearchInput extends Component {
  constructor(props) {
    super(props)

    this.state = {
      query: '',
      movieTitle: '',
      actor: '',
      year: '',
      fromYear: '',
      toYear: '',
      keywords: '',
      enableAdvancedSearch: false,
      movieSearchEnabled: false,
      invalidMessage: ''
    }
  }

  componentDidMount() {
    this.setState({ showErrorMsg: false, invalidMessage: '' })
  }

  onSearchChange = e => {
    this.setState({ query: e.target.value })
  }

  setSearchInput = (event) => {
    this.setState({ query: event.target.text }, this.selectSearch)
  }

  toggleAdvancedSearch = () => this.setState({ enableAdvancedSearch: !this.state.enableAdvancedSearch })

  onAdvancedSearchChange = (field, value) => {
    let invalidMessage = ''

    if (field === 'year') {
      let [fromYear, toYear] = value.split('-')
      fromYear = parseInt(fromYear)
      toYear = parseInt(toYear)

      if ((fromYear.length && isNaN(fromYear)) || (toYear.length && isNaN(toYear))) {
        invalidMessage = 'Year should be a number in the range 1900-2020'
      } else {
        if (fromYear && toYear) {
          value = `${fromYear}-${toYear}`
          if (fromYear > toYear || fromYear < 1900 || toYear > 2020) {
            invalidMessage = 'Invalid year range'
          }
        } else if (!fromYear && !toYear) {
          value = ''
        } else if (!fromYear && toYear) {
          value = `1900-${toYear}`
        } else if (fromYear && !toYear) {
          value = `${fromYear}-2020`
        }
      }
    }
    this.setState({ [field]: value, invalidMessage })
  }

  /**
   * Select between a quote search or movie search
   * @param  {Event} e - event from submitting the button
   */
  selectSearch = e => {
    e && e.preventDefault()
    const { query, movieTitle, actor, year, keywords } = this.state
    const advancedSearchParams = { movieTitle, actor, year, keywords }
    this.props.performSearch({query, ...advancedSearchParams}, this.state.movieSearchEnabled)
  }

  /**
   * Perform movie search if there is a query provided and the user enables movie search.
   * Otherwise do nothing.
   * @param  {Event} e - event from toggling the checkbox
   */
  toggleMovieSearch = (e) => {
    const { query, movieTitle, actor, year, keywords } = this.state
    const movieSearchEnabled = e.target.checked

    this.setState({ movieSearchEnabled }, () => {
      if (query.length) {
        const advancedSearchParams = { movieTitle, actor, year, keywords }
        this.props.performSearch({query, ...advancedSearchParams}, movieSearchEnabled)

      }
    })
  }

  render() {
    const { enableAdvancedSearch, movieTitle, actor, year, keywords, movieSearchEnabled, invalidMessage } = this.state
    const { showErrorMsg, showExamples } = this.props
    const advancedSearchData = { movieTitle, actor, year, keywords }

    return (
      <Grid item xs={12}>
        <form noValidate autoComplete="off" onSubmit={this.selectSearch}>
          <div className="search-form">
            <div className="search-input">
              <TextField
                id="outlined-basic"
                label="Search for a movie quote..."
                variant="outlined"
                fullWidth
                onChange={this.onSearchChange}
                value = {this.state.query}
              />
            </div>
            <Button
              className="search-button"
              variant="outlined"
              color="primary"
              type="submit"
            >Search</Button>

            <FormControlLabel className="movie-search"
              control={
                <Checkbox
                  checked={movieSearchEnabled}
                  onChange={this.toggleMovieSearch}
                  color="primary"
                  inputProps={{ 'aria-label': 'primary checkbox' }}
                />
              }
              label="Search for movies"
            />
          </div>

          <FormControlLabel
            className="advanced-search-button"
            color="primary"
            control={
              <Switch
                checked={enableAdvancedSearch}
                onChange={this.toggleAdvancedSearch}
                value="checkedB"
                color="primary"
              />
            }
            label="Advanced Search"
          />

          <AdvancedSearch
            enableAdvancedSearch={enableAdvancedSearch}
            data={advancedSearchData}
            onAdvancedSearchChange={this.onAdvancedSearchChange}
          />
          {invalidMessage.length ? <Typography variant="body1" className="error-message">{invalidMessage}</Typography> : ''}
        </form>


        {showExamples &&
          <Typography variant="h6" color="primary" className="examples">
            <span>
              Try <Link color="primary" underline="none" variant="inherit" onClick={this.setSearchInput}>
                Carpe Diem
              </Link>
            </span>
            <span> or <Link color="primary" underline="none" variant="inherit" onClick={this.setSearchInput}>
                Following's not really my style
              </Link>
            </span>
          </Typography>
        }
        {showErrorMsg &&
          <h6 className="error-container">
            Error: API not running. Go to ttds_movie_search/api and run ./run.sh
          </h6>
        }
      </Grid>
    )
  }
}

SearchInput.propTypes = {
  performSearch: PropTypes.func.isRequired,
  showExamples: PropTypes.bool.isRequired,
  showErrorMsg: PropTypes.bool.isRequired
}
