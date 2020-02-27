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
    if (prevProps.details._id !== this.props.details._id) {
      this.setState({ moreCastVisible: false })
    }
  }

  showMoreCast = e => {
    e.preventDefault()
    this.setState({ moreCastVisible: !this.state.moreCastVisible })
  }

  render() {
    const { details, errorMovieInfoMsg } = this.props
    const { moreCastVisible } = this.state

    let castSlice = 0
    if (details.cast) {
      castSlice = details.cast.length > 10 ? 10 : details.cast.length
    }

    return(
      <div {...this.props} className="details-card">
        <Card raised className="card-container">
          <CardContent>
            <div className="card-content">
              {errorMovieInfoMsg.length ?
                <CardContent>
                  <Typography variant="h6" color="secondary">{errorMovieInfoMsg}</Typography>
                </CardContent>
              : details &&
                <CardContent>
                  <Typography variant="h5">{details.title}</Typography>
                  <Typography variant="body1">{details.description}</Typography>
                  {details.year && <Typography variant="body1"><b>Year:</b> {details.year}</Typography>}
                  <Typography variant="body1" gutterBottom><b>Rating:</b> {details.rating}</Typography>
                  {castSlice > 0 && details.cast.length > 0 && <Typography variant="h5">Cast</Typography>}

                  {castSlice > 0 && details.cast.slice(0, castSlice).map((item) =>
                    <Typography key={item.actor} variant="body1">{item.actor} as <i>{item.character}</i></Typography>
                  )}

                  {castSlice > 0 && details.cast.length > 10 &&
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
                  <Button target="_blank" variant="contained" color="primary" href={`https://www.imdb.com/title/${details._id}`}>View in IMDB</Button>
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
  details: PropTypes.object.isRequired,
  errorMovieInfoMsg: PropTypes.object.isRequired
}
