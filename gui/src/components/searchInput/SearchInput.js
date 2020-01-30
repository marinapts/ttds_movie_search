import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Grid from '@material-ui/core/Grid'
import { TextField, Button, Link, Typography } from '@material-ui/core'
import API from '../../utils/API'

import './searchInput.scss'

export default class SearchInput extends Component {
  constructor(props) {
    super(props)

    this.state = {
      query: '',
      showErrorMsg: false,
      showExamples: true
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

  querySearch = async (e) => {
    e && e.preventDefault()
    const { query } = this.state

    if (query.length > 0) {
      try {
        const response = await API.post('/query_search', { query })
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
    const { showErrorMsg, showExamples } = this.state

    return (
      <Grid item xs={8}>
        <form className="search-container" noValidate autoComplete="off" onSubmit={this.querySearch}>
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
        </form>
        {showExamples &&
          <Typography variant="h6" color="primary">
            <span>
              Try <Link color="primary" underline="none" variant="inherit" onClick={this.setSearchInput}>
                I can do this all day
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
