from email.policy import default
# from matplotlib import *
from app import db


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(500), nullable=True)  
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))   
    seeking_talent = db.Column( db.Boolean(), default=False ) 
    seeking_description = db.Column(db.String(200), default = "" )  
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))    

    def __repr__(self):
      return f'''<Venue ID: {self.id},\n   name: {self.name }, genres: {self.genres}, 
                  city: {self.city},   state: {self.state }, address: {self.address},
                  phone : {self.phone},   website: {self.website }, seeking_talent: {self.seeking_talent},
                  seeking_description : {self.seeking_description},   image_link: {self.image_link }, 
                  facebook_link: {self.facebook_link} >''' 

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String) 
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column( db.Boolean(), default=False, nullable=False ) 
    website =  db.Column(db.String(120))   
    seeking_description = db.Column(db.String(200), default = "" )  
    shartist = db.relationship(Artist, backref='list', lazy=False, uselist = False) 


    def __repr__(self):
      return f'''<Artist ID: {self.id},\n   name: {self.name }, genres: {self.genres}, 
                  city: {self.city},   state: {self.state }, phone : {self.phone},   
                  website: {self.website }, seeking_venue: {self.seeking_venue},
                  seeking_description : {self.seeking_description},   image_link: {self.image_link }, 
                  facebook_link: {self.facebook_link} >''' 


class Show(db.Model):
    __tablename__ = 'Shows'
    
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), nullable=False, primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True), primary_key=True)
    artist = db.relationship(Artist, backref='list', lazy=False, uselist = False) 
    Venue = db.relationship(Venue, backref='list', lazy=False, uselist = False)





# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.



   # show artist
#   data1={
#     "id": 4,
#     "name": "Guns N Petals",
#     "genres": ["Rock n Roll"],
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "326-123-5000",
#     "website": "https://www.gunsnpetalsband.com",
#     "facebook_link": "https://www.facebook.com/GunsNPetals",
#     "seeking_venue": True,
#     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     "past_shows": [{
#       "venue_id": 1,
#       "venue_name": "The Musical Hop",
#       "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#       "start_time": "2019-05-21T21:30:00.000Z"
#     }],
#     "upcoming_shows": [],
#     "past_shows_count": 1,
#     "upcoming_shows_count": 0,
#   }