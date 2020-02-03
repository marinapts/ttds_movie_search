import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Grid, FormControlLabel, Switch, TextField, Button, Link, Typography } from '@material-ui/core'
import API from '../../utils/API'
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
      showErrorMsg: false,
      showExamples: true,
      enableAdvancedSearch: false
    }
  }

  componentDidMount() {
    this.setState({ showErrorMsg: false })
  }

  onSearchChange = e => {
    this.setState({ query: e.target.value })
  }

  setSearchInput = (event) => {
    this.setState({ query: event.target.text }, this.querySearch)
  }

  toggleAdvancedSearch = () => this.setState({ enableAdvancedSearch: !this.state.enableAdvancedSearch })

  onAdvancedSearchChange = (field, value) => this.setState({ [field]: value })

  querySearch = async (e) => {
    e && e.preventDefault()
    const { query, movieTitle, actor, year, keywords } = this.state
    console.log(query, movieTitle, actor, year, keywords)

    if (query.length > 0) {
      try {
        const response = await API.post('/query_search', { query, movie_title: movieTitle, actor, year, keywords })
        this.props.getMoviesForQuery(response.data)
        this.setState({ showErrorMsg: false, showExamples: false })
      } catch (error) {
        // @TODO: Show a proper error message to the user
        console.error(error)
        this.setState({ showErrorMsg: true, showExamples: true })
      }
    }
  }

  render() {
    const { showErrorMsg, showExamples, enableAdvancedSearch, movieTitle, actor, year, keywords } = this.state
    const advancedSearchData = { movieTitle, actor, year, keywords }

    return (
      <Grid item xs={12}>
        <form noValidate autoComplete="off" onSubmit={this.querySearch}>
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
          </div>

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
  getMoviesForQuery: PropTypes.func.isRequired
}
