import React from 'react'
import PropTypes from 'prop-types';
import { Card, CardMedia, CardContent, CardActionArea, Typography } from '@material-ui/core'

import './movieCard.scss'

const QUOTE_LIMIT = 200

export default class MovieCard extends React.Component {
  viewDetails = () => {
    this.props.viewDetails(this.props.movie_id)
  }

  render() {
    let { full_quote, title, character_name, categories, plotKeywords } = this.props
    // const keywords = plotKeywords.length > 5 ? plotKeywords.slice(0, 5) : plotKeywords
    const truncatedQuote = full_quote.length > QUOTE_LIMIT ? `${full_quote.substr(0, QUOTE_LIMIT)}...` : full_quote

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
                <Typography variant="h5">{truncatedQuote}</Typography>
                <Typography variant="h6">{title}</Typography>
                <br/>
                <Typography variant="body2">Character: {character_name}</Typography>
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
