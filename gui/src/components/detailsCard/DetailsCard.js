import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { Card, CardContent, Typography, Button, Link } from '@material-ui/core'

import './detailsCard.scss'

export default class DetailsCard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      moreCastVisible: false
    }
  }

  componentDidUpdate(prevProps) {
    if (prevProps.details.movie_id !== this.props.details.movie_id) {
      this.setState({ moreCastVisible: false })
    }
  }

  showMoreCast = e => {
    e.preventDefault()
    this.setState({ moreCastVisible: !this.state.moreCastVisible })
  }

  render() {
    const { details } = this.props
    const { moreCastVisible } = this.state
    const castSlice = details.cast.length > 10 ? 10 : details.cast.length

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
                  {details.cast.length > 0 && <Typography variant="h5">Cast</Typography>}

                  {details.cast.slice(0, castSlice).map((item) =>
                    <Typography key={item.actor} variant="body1">{item.actor} as <i>{item.character}</i></Typography>
                  )}

                  {details.cast.length > 10 &&
                    <Fragment>
                      {!moreCastVisible && <Link onClick={this.showMoreCast}><Typography>Show more...</Typography></Link>}
                      {moreCastVisible && details.cast.slice(10, -1).map((item) =>
                          <Typography key={item.actor} variant="body1">{item.actor} as <i>{item.character}</i></Typography>
                        )
                      }
                    </Fragment>
                  }
                  <br/>
                  <Typography variant="body1" gutterBottom></Typography>
                  <Button target="_blank" variant="contained" color="primary" href={`https://www.imdb.com/title/${details.movie_id}`}>View in IMDB</Button>
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
