import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Grid, Collapse, TextField } from '@material-ui/core'
import TheatersOutlinedIcon from '@material-ui/icons/TheatersOutlined'
import HourglassEmptyOutlinedIcon from '@material-ui/icons/HourglassEmptyOutlined'
import VpnKeyOutlinedIcon from '@material-ui/icons/VpnKeyOutlined'
import RecentActorsIcon from '@material-ui/icons/RecentActors'

import './advancedSearch.scss'

export default class AdvancedSearch extends Component {
  onHandleChange = (field, value) => {
    this.props.onAdvancedSearchChange(field, value)
  }

  render() {
    const { enableAdvancedSearch, data } = this.props

    return(
      <Collapse in={enableAdvancedSearch}>
        <div className="adv-search">
          <div className="adv-search-container">
            <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
              <Grid item><TheatersOutlinedIcon color="primary" /></Grid>
              <Grid item>
                <TextField value={data.movieTitle} label="Movie title" onChange={e => this.onHandleChange('movieTitle', e.target.value)} />
              </Grid>
            </Grid>
            <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
              <Grid item><RecentActorsIcon color="primary" /></Grid>
              <Grid item>
                <TextField value={data.actor} label="Actor/Actress" onChange={e => this.onHandleChange('actor', e.target.value)} />
              </Grid>
            </Grid>
          </div>
          <div className="adv-search-container">
            <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
              <Grid item><HourglassEmptyOutlinedIcon color="primary" /></Grid>
              <Grid item>
                <TextField value={data.year} label="Year" onChange={e => this.onHandleChange('year', e.target.value)} />
              </Grid>
            </Grid>
             <Grid container spacing={1} alignItems="space-between" className="adv-search-item">
                <Grid item><VpnKeyOutlinedIcon color="primary" /></Grid>
                <Grid item>
                  <TextField value={data.keywords} label="Keywords" onChange={e => this.onHandleChange('keywords', e.target.value)} />
                </Grid>
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
