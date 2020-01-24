import React from 'react'
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card'
import CardMedia from '@material-ui/core/CardMedia'
import CardActions from '@material-ui/core/CardActions'
import CardContent from '@material-ui/core/CardContent'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import CardActionArea from '@material-ui/core/CardActionArea'

import './movieCard.scss'

export default class MovieCard extends React.Component {
  constructor(props){
    super(props);
    this.state = {
       viewMore: false,
    };
    this.viewMoreAction = this.viewMoreAction.bind(this);
  }
  viewMoreAction(){
    const {viewMore} =  this.state;
    this.setState({ 
      viewMore: !viewMore,
    });
  }
  render() {
    const castList = Object.entries(this.props.cast).map(([key,value])=>{
      return (
        <div>{key} as {value}</div>
      );
    })
    const {viewMore} = this.state;
    return (
      <>
      <Card raised className="card-container">
      <CardMedia
          className="card-media"
          image={this.props.thumbnail}
        />
      <CardActionArea onClick={this.viewMoreAction}>
        <div className="card-content">
          <CardContent>
            <Typography variant="h5" component="h2">{this.props.full_quote}</Typography>
            <Typography variant="h5" component="h2">{this.props.title}</Typography>
            <Typography variant="body2" component="p">Rating: {this.props.rating}<br />Year: {this.props.year}</Typography>
            <Typography variant="body2" component="p">Category: {this.props.categories}</Typography>
          </CardContent>
          <CardActions>
            <Button variant="outlined" color="primary">viewMore</Button>
          </CardActions>   
        </div>
        </CardActionArea>
      </Card>
      {viewMore && (
        <Card raised className="card-container-view-more">
          <div>
            <CardContent>
                <Typography>{castList}</Typography>
            </CardContent>
          </div>
        </Card>
      )}
      </>
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