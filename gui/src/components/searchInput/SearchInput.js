import React from 'react'
import PropTypes from 'prop-types'
import Grid from '@material-ui/core/Grid'
import { TextField, Button } from '@material-ui/core'
import API from '../../utils/API'

import './searchInput.scss'

export default class SearchInput extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      query: '',
      showErrorMsg: false
    }
  }

  componentDidMount() {
    this.setState({ showErrorMsg: false })
  }

  onSearchChange = e => {
    this.setState({ query: e.target.value })
  }

  querySearch = async () => {
    const { query } = this.state;

    if (query.length > 0) {
      try {
        const response = await API.post('/query_search', { query })
        this.props.getMoviesForQuery(response.data)
        this.setState({ showErrorMsg: false })
      } catch (error) {
        // @TODO: Show a proper error message to the user
        console.error(error)
        this.setState({ showErrorMsg: true })
      }
    }
  }

  render() {
    const { showErrorMsg } = this.state

    return (
      <Grid item xs={8}>
        <form className="search-container" noValidate autoComplete="off">
          <div className="search-input">
            <TextField
              id="outlined-basic"
              label="Search for a movie quote..."
              variant="outlined"
              fullWidth
              onChange={this.onSearchChange}
            />
          </div>
          <Button
            className="search-button"
            variant="outlined"
            color="primary"
            onClick={this.querySearch}
          >Search</Button>
        </form>
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
