#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from copy import deepcopy
import json
from sqlite3 import DatabaseError
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
from flask import jsonify
from datetime import datetime, timedelta, timezone

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

from models import *


migrate = Migrate(app, db)




# db.create_all()

# migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  all_Venue = Venue.query.all()  #.filter(person.name=="Nicanora") 


  all_city_state = Venue.query.with_entities(Venue.city, Venue.state).distinct().all() 
  current_time = datetime.now(tz=timezone.utc)


  data = []
  for city_state in all_city_state :
    dict = {
      "city" : city_state.city,
      "state" : city_state.state, 
      "venues" : [] 
    }
    for venue in all_Venue :
      if ( city_state.city == venue.city and city_state.state == venue.state ) : 
        dict["venues"].append({
          "id" : venue.id,
          "name" : venue.name,
          "num_upcoming_shows" : len(list(filter(lambda it : it.start_time > current_time, venue.show))) 
        })    
    data.append(dict)    

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term =  request.form.get('search_term', "")
  pattern = "%{}%".format(search_term)   
  found_items = Venue.query.filter(Venue.name.ilike(pattern)).all()
  current_time = datetime.now(tz=timezone.utc)

  # print(found)

  response={
    "count": len(found_items),
    "data": [{
      "id": it.id,
      "name":it.name,
      "num_upcoming_shows": len(list(filter(lambda x : x.start_time > current_time, it.shows))) ,
    } for it in found_items ]
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)  #.filter(person.name=="Nicanora") 
  print(venue)

  current_time = datetime.now(tz=timezone.utc)

  _past_shows = list(filter(lambda it : it.start_time < current_time, venue.shows))
  _upcoming_shows = list(filter(lambda it : it.start_time > current_time, venue.shows)) 

  past_shows = [
                  { 
                    "artist_id" : x.artist_id,
                    "artist_name"  : x.artist.name,
                    "artist_image_link" : x.artist.image_link,
                    "start_time" : "{}".format(x.start_time) 
                  }                    
                  for x in _past_shows  
               ]
  
  upcoming_shows = [
                      { 
                        "artist_id" : x.artist_id,
                        "artist_name"  : x.artist.name,
                        "artist_image_link" : x.artist.image_link,
                        "start_time" : "{}".format(x.start_time) 
                      }                    
                      for x in _upcoming_shows  
                   ]

  data = {
    "id": venue.id,
    "name": venue.name ,
    "genres": [venue.genres],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": len(upcoming_shows) ,
  }

  # print(data)


  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion  
  try:
    if( request.form.get('seeking_talent', "n") == "y" ) :
      seeking_talent =  True
    else :
      seeking_talent = False

    venue = Venue (
      name =  request.form['name'],
      city =  request.form['city'],
      state =  request.form['state'],
      address =  request.form['address']  ,
      phone =  request.form.get('phone', None),
      genres =  request.form['genres'],
      facebook_link =  request.form.get('facebook_link', None),
      image_link = request.form.get('image_link', None),
      website =  request.form.get('website_link', None),
      seeking_talent = seeking_talent,
      seeking_description =  request.form.get('seeking_description', None)
    )  

    print(venue)

    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')

  except Exception as e:
    db.session.rollback()
    error=True
    print(e)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    form = VenueForm() 
    return render_template('forms/new_venue.html', form=form)
  finally:
    db.session.close()




  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/




@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  print("deleting Venue .... ")
  
  try:
    venue = Venue.query.get(venue_id) 
    db.session.delete(venue)
    db.session.commit()
    flash('Venue  was successfully deleted!')
    return redirect(url_for('venues'))  
  except Exception as e:
    db.session.rollback()
    error=True
    print(e)
    flash('An error occurred. Venue  could not be deleted.')
    return redirect(url_for('show_venue', venue_id=venue_id))
  finally :   
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  all_artist = Artist.query.with_entities(Artist.id, Artist.name).all()  #.filter(person.name=="Nicanora") 

  data = [dict(v) for v in all_artist]




  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term =  request.form.get('search_term', "")
  pattern = "%{}%".format(search_term)   
  found_items = Artist.query.filter(Artist.name.ilike(pattern)).all()
  current_time = datetime.now(tz=timezone.utc)

  # print(found)

  response={
    "count": len(found_items),
    "data": [{
      "id": it.id,
      "name":it.name,
      "num_upcoming_shows": len(list(filter(lambda x : x.start_time > current_time, it.shows))) ,
    } for it in found_items ]
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id


  artist = Artist.query.get(artist_id)  #.filter(person.name=="Nicanora") 
  print(artist)

  current_time = datetime.now(tz=timezone.utc)

  _past_shows = list(filter(lambda it : it.start_time < current_time, artist.Show))
  _upcoming_shows = list(filter(lambda it : it.start_time > current_time, artist.Show)) 

  past_shows = [
                  { 
                    "venue_id" : x.artist_id,
                    "venue_name"  : x.artist.name,
                    "venue_image_link" : x.artist.image_link,
                    "start_time" : "{}".format(x.start_time) 
                  }                    
                  for x in _past_shows  
               ]
  
  upcoming_shows = [
                      { 
                        "venue_id" : x.artist_id,
                        "venue_name"  : x.artist.name,
                        "venue_image_link" : x.artist.image_link,
                        "start_time" : "{}".format(x.start_time) 
                      }                    
                      for x in _upcoming_shows  
                   ]

  data = {
    "id": artist.id,
    "name": artist.name ,
    "genres": [artist.genres],
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": len(upcoming_shows) ,
  }


  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id) 

  form.name.data = artist.name
  form.city.data = artist.city
  form.phone.data = artist.phone 
  form.image_link.data = artist.image_link 
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website
  form.seeking_venue.data =  artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.genres.data = [2,3] 
  form.state.default =  "ID"


  

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes


  try:
    artist = Artist.query.get(artist_id) 



    if( request.form.get('seeking_talent', "n") == "y" ) :
      seeking_venue =  True
    else :
      seeking_venue = False


    artist.name =  request.form.get('name')
    artist.city =  request.form.get('city')
    artist.state =  request.form.get('state')
    artist.phone =  request.form.get('phone', None)
    artist.genres =  request.form.get('genres')
    artist.facebook_link =  request.form.get('facebook_link', None)
    artist.image_link = request.form.get('image_link', None)
    artist.website =  request.form.get('website_link', None)
    artist.seeking_venue = seeking_venue
    artist.seeking_description =  request.form.get('seeking_description', None)  

    db.session.commit()
    # db.session.close()
    flash('Artist  was successfully updated!')
    # return render_template('pages/home.html')
    return redirect(url_for('show_artist', artist_id=artist_id))


  except Exception as e:
    db.session.rollback()
    error=True
    print(e)
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    form = ArtistForm()   
    return render_template('forms/edit_artist.html', form=form, artist=artist)
  finally : 
    db.session.close() 
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  form = VenueForm()  

  venue = Venue.query.get(venue_id)   

  form.name.data = venue.name
  form.city.data = venue.city
  form.address.data = venue.address
  form.phone.data = venue.phone 
  form.image_link.data = venue.image_link 
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website
  form.seeking_talent.data =  venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  form.genres.data = [2,3] 
  form.state.default =  "ID"


  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  try:
    venue = Venue.query.get(venue_id) 



    if( request.form.get('seeking_talent', "n") == "y" ) :
      seeking_talent =  True
    else :
      seeking_talent = False


    venue.name =  request.form.get('name')
    venue.city =  request.form.get('city')
    venue.state =  request.form.get('state')
    venue.address =  request.form.get('address')  
    venue.phone =  request.form.get('phone', None)
    venue.genres =  request.form.get('genres')
    venue.facebook_link =  request.form.get('facebook_link', None)
    venue.image_link = request.form.get('image_link', None)
    venue.website =  request.form.get('website_link', None)
    venue.seeking_talent = seeking_talent
    venue.seeking_description =  request.form.get('seeking_description', None)  

    db.session.commit()
    # db.session.close()
    flash('Venue  was successfully updated!')
    # return render_template('pages/home.html')
    return redirect(url_for('show_venue', venue_id=venue_id))


  except Exception as e:
    db.session.rollback()
    error=True
    print("ERRor: ")
    print(e)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    form = VenueForm() 


    return render_template('forms/edit_venue.html', form=form, venue=venue)
    # return redirect(url_for('show_venue', venue_id=venue_id))

  finally:
    db.session.close()





#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  try:
    if( request.form.get('seeking_venue', "n") == "y" ) :
      seeking_venue =  True
    else :
      seeking_venue = False

    artist = Artist (
      name =  request.form['name'],
      city =  request.form['city'],
      state =  request.form['state'],
      phone =  request.form.get('phone', None),
      genres =  request.form['genres'],
      facebook_link =  request.form.get('facebook_link', None),
      image_link = request.form.get('image_link', None),
      website =  request.form.get('website_link', None),
      seeking_venue = seeking_venue,
      seeking_description =  request.form.get('seeking_description', None)
    )  


    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    db.session.close()
    return render_template('pages/home.html')

  except Exception as e:
    db.session.rollback()
    error=True
    print(e)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    form = ArtistForm() 
    db.session.close()
    return render_template('forms/new_artist.html', form=form)
    

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion 
  # on successful db insert, flash success   
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')




#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. 

  all_shows = Show.query.all() 

  data = [ {
    "venue_id": it.venue_id ,
    "venue_name": it.venue.name,
    "artist_id": it.artist_id,
    "artist_name": it.artist.name,
    "artist_image_link": it.artist.image_link ,
    "start_time": "{}".format(it.start_time) 
    }   for it in all_shows
  ]


  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  try: 

    show = Show (
      artist_id =  request.form['artist_id'],
      venue_id =  request.form['venue_id'],
      start_time =  request.form['start_time']      
    )  


    db.session.add(show)
    db.session.commit()
    flash('show  was successfully listed!')
    db.session.close()
    # return render_template('pages/shows.html')
    return redirect(url_for('shows'))


  except Exception as e:
    db.session.rollback()
    error=True
    print(e)
    flash('An error occurred. show could not be listed.')
    form = ShowForm() 
    db.session.close()
    return render_template('forms/new_show.html', form=form)
  

  

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
