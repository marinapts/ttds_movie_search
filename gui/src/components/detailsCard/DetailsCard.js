import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Card, CardContent, Typography, Button } from '@material-ui/core'

import './detailsCard.scss'

export default class DetailsCard extends Component {
  render() {
    const { details } = this.props

    let cast = []
    if (details && details.cast) {
      cast = Object.entries(details.cast)
      if (cast.length > 10) {
        cast = cast.slice(0, 10)
      }
    }

    return(
      <div {...this.props} className="details-card">
        <Card raised className="card-container">
          <CardContent>
            <div className="card-content">
              {details &&
                <CardContent>
                  <Typography variant="h5">{details.title}</Typography>
                  <Typography variant="body1">{details.description}</Typography>
                  <Typography variant="body1"><b>Year:</b> {details.year}</Typography>
                  <Typography variant="body1" gutterBottom><b>Rating:</b> {details.rating}</Typography>
                  <Typography variant="h5">Cast</Typography>
                  {
                    cast.map(([actor, character]) =>
                      <Typography variant="body1">{actor} as <i>{character}</i></Typography>
                    )
                  }
                  <Typography variant="body1" gutterBottom></Typography>
                  {Object.entries(details.cast).length > 10 && <Button variant="outlined" color="primary">See more</Button>}
                </CardContent>
              }
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }
}

DetailsCard.propTypes = {
  details: PropTypes.object.isRequired
}
