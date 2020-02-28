import React from 'react'
import PropTypes from 'prop-types';
import { Card, CardMedia, CardContent, CardActionArea, Typography } from '@material-ui/core'

import './movieCard.scss'

const QUOTE_LIMIT = 200

export default class MovieCard extends React.Component {
  viewDetails = () => {
    this.props.viewDetails(this.props.movie_id)
  }

  convertMsToTime = time_ms => {
    let seconds = Math.floor((time_ms / 1000) % 60)
    let minutes = Math.floor((time_ms / (1000 * 60)) % 60)
    let hours = Math.floor((time_ms / (1000 * 60 * 60)) % 24)

    hours = (hours < 10) ? '0' + hours : hours
    minutes = (minutes < 10) ? '0' + minutes : minutes
    seconds = (seconds < 10) ? '0' + seconds : seconds

    return `${hours}:${minutes}:${seconds}`
  }

  render() {
    let { full_quote, title, character, categories, time_ms, plotKeywords } = this.props
    // const keywords = plotKeywords.length > 5 ? plotKeywords.slice(0, 5) : plotKeywords
    const truncatedQuote = full_quote && full_quote.length > QUOTE_LIMIT ? `${full_quote.substr(0, QUOTE_LIMIT)}...` : full_quote
    const quote = character ? `“${truncatedQuote}” - ${character}` : `“${truncatedQuote}”`

    return (
      <div>
        <Card raised className="card-container">
          <CardMedia
            className="card-media"
            image={this.props.thumbnail}
          />
          <CardActionArea onClick={this.viewDetails}>
            <div className="card-content">
              <CardContent>
                {full_quote && <Typography variant="h5">{quote}</Typography>}
                <Typography variant="h6">{title}</Typography>
                <br/>
                {time_ms && <Typography variant="body2">Quote was said at {this.convertMsToTime(time_ms)}</Typography>}
                <Typography variant="body2">Category: {categories.join(', ')}</Typography>
              </CardContent>
            </div>
          </CardActionArea>
        </Card>
      </div>
    )
  }
}

MovieCard.propTypes = {
  // movie is an object of this particular shape
  movie: PropTypes.shape({
    title: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    info: PropTypes.string,
    img: PropTypes.string,
    imgTitle: PropTypes.string
  })
}
