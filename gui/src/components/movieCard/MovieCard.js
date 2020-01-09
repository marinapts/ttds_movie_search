import React from 'react'
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card'
import CardActions from '@material-ui/core/CardActions'
import CardContent from '@material-ui/core/CardContent'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'

import './movieCard.scss'


export default class MovieCard extends React.Component {
  render() {
    const { title, description, info } = this.props

    return (
      <Card raised className="card-container">
        <CardContent>
          <Typography variant="h5" component="h2">{title}</Typography>
          <Typography variant="body2" component="p">{description}<br />{info}</Typography>
        </CardContent>
        <CardActions>
          <Button variant="outlined" color="primary">View more</Button>
        </CardActions>
      </Card>
    )
  }
}

MovieCard.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  info: PropTypes.string
}
