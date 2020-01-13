import React from 'react'
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card'
import CardMedia from '@material-ui/core/CardMedia'
import CardActions from '@material-ui/core/CardActions'
import CardContent from '@material-ui/core/CardContent'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'

import './movieCard.scss'

export default class MovieCard extends React.Component {

  render() {
    return (
      <Card raised className="card-container">
        <CardMedia
          className="card-media"
          image={this.props.thumbnail}
          title={this.props.title}
        />
        <div className="card-content">
          <CardContent>
            <Typography variant="h5" component="h2">{this.props.title}</Typography>
            <Typography variant="body2" component="p">Rating: {this.props.rating}<br />Year: {this.props.year}</Typography>
            <Typography variant="body2" component="p">Category: {this.props.categories.join(", ")}</Typography>
          </CardContent>
          <CardActions>
            <Button variant="outlined" color="primary">View more</Button>
          </CardActions>   
        </div>
      </Card>
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
