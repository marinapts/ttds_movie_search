import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Card, CardContent, Typography, Button } from '@material-ui/core'

import './detailsCard.scss'

export default class DetailsCard extends Component {
  render() {
    const { details } = this.props

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
                    details.cast.map((item) =>
                      <Typography key={item.actor} variant="body1">{item.actor} as <i>{item.character}</i></Typography>
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
