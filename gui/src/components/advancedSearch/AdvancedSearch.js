import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Grid, Collapse, TextField } from '@material-ui/core'
import TheatersOutlinedIcon from '@material-ui/icons/TheatersOutlined'
import HourglassEmptyOutlinedIcon from '@material-ui/icons/HourglassEmptyOutlined'
import VpnKeyOutlinedIcon from '@material-ui/icons/VpnKeyOutlined'
import RecentActorsIcon from '@material-ui/icons/RecentActors'

import './advancedSearch.scss'

export default class AdvancedSearch extends Component {
  constructor(props) {
    super(props)
    this.state = {
      fromYear: '',
      toYear: '',
      year: ''
    }
  }

  onHandleYearChange = (field, value) => this.setState({ [field]: value })

  onHandleChange = (field, value) => {
    if (field === 'year') {
      value = `${this.state.fromYear}-${this.state.toYear}`
    }
    this.props.onAdvancedSearchChange(field, value)
  }

  render() {
    const { fromYear, toYear } = this.state
    const { enableAdvancedSearch, data } = this.props

    return(
      <Collapse in={enableAdvancedSearch}>
        <div className="adv-search">
          <div className="adv-search-container">
            <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
              <TheatersOutlinedIcon className="adv-search-icon" color="primary" />
              <TextField className="adv-search-input" value={data.movieTitle} label="Movie title" onChange={e => this.onHandleChange('movieTitle', e.target.value)} />
            </Grid>
            <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
              <RecentActorsIcon className="adv-search-icon" color="primary" />
              <TextField className="adv-search-input" value={data.actor} label="Actor/Actress" onChange={e => this.onHandleChange('actor', e.target.value)} />
            </Grid>
          </div>
          <div className="adv-search-container">
            <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
              <HourglassEmptyOutlinedIcon className="adv-search-icon" color="primary" />
              <div className="year">
                <TextField
                  className="adv-search-input year-input"
                  value={fromYear} label="From year"
                  onChange={e => this.onHandleYearChange('fromYear', e.target.value)}
                  onBlur={e => setTimeout(() => this.onHandleChange('year', this.state.year), 0.5)}
                />
                <TextField
                  className="adv-search-input year-input"
                  value={toYear} label="To year"
                  onChange={e => this.onHandleYearChange('toYear', e.target.value)}
                  onBlur={e => this.onHandleChange('year', this.state.year)}
                />
              </div>
            </Grid>
             <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
                <VpnKeyOutlinedIcon className="adv-search-icon" color="primary" />
                <TextField className="adv-search-input" value={data.keywords} label="Keywords" onChange={e => this.onHandleChange('keywords', e.target.value)} />
              </Grid>
          </div>
        </div>
      </Collapse>
    )
  }
}

AdvancedSearch.propTypes = {
  enableAdvancedSearch: PropTypes.bool.isRequired,
  data: PropTypes.shape({
    movieTitle: PropTypes.string,
    actor: PropTypes.string,
    year: PropTypes.string,
    keywords: PropTypes.string,
  }).isRequired,
  onAdvancedSearchChange: PropTypes.func.isRequired
}
