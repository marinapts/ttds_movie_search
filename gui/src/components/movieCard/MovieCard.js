import React from 'react'
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card'
import CardMedia from '@material-ui/core/CardMedia'
import CardActions from '@material-ui/core/CardActions'
import CardContent from '@material-ui/core/CardContent'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import logo from '../../logo.svg';

import './movieCard.scss'


export default class MovieCard extends React.Component {
  render() {
    const { title, description, info, img, imgTitle } = this.props

    return (
      <Card raised className="card-container">
        <CardMedia
          className="card-media"
          image={logo} // replace this with img
          title={imgTitle || ''}
        />
        <div className="card-content">
          <CardContent>
            <Typography variant="h5" component="h2">{title}</Typography>
            <Typography variant="body2" component="p">{description}<br />{info}</Typography>
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
