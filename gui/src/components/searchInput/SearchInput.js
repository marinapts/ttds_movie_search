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
      keywords: '',
      enableAdvancedSearch: false,
      movieSearchEnabled: false
    }
  }

  componentDidMount() {
    this.setState({ showErrorMsg: false })
  }

  onSearchChange = e => {
    this.setState({ query: e.target.value })
  }

  setSearchInput = (event) => {
    this.setState({ query: event.target.text }, this.selectSearch)
  }

  toggleAdvancedSearch = () => this.setState({ enableAdvancedSearch: !this.state.enableAdvancedSearch })

  onAdvancedSearchChange = (field, value) => this.setState({ [field]: value })

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
    console.log(movieSearchEnabled)
    this.setState({ movieSearchEnabled }, () => {
      if (query.length) {
        const advancedSearchParams = { movieTitle, actor, year, keywords }
        this.props.performSearch({query, ...advancedSearchParams}, movieSearchEnabled)

      }
    })
  }

  render() {
    const { enableAdvancedSearch, movieTitle, actor, year, keywords, movieSearchEnabled } = this.state
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
        </form>


        {showExamples &&
          <Typography variant="h6" color="primary">
            <span>
              Try <Link color="primary" underline="none" variant="inherit" onClick={this.setSearchInput}>
                I see dead people
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
  performSearch: PropTypes.func.isRequired
}
