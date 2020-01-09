import React from 'react'
import Grid from '@material-ui/core/Grid'
import { TextField } from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles(theme => ({
  root: {
    '& > *': {
      width: '100%',
    },
  }
}));

export default function SearchInput() {
  const classes = useStyles();

  return (
    <Grid item xs={8}>
      <form className={classes.root} noValidate autoComplete="off">
        <TextField id="outlined-basic" label="Search for a movie quote..." variant="outlined" />
      </form>
    </Grid>
  )
}
