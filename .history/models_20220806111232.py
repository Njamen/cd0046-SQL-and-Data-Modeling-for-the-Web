from email.policy import default
from app import db
from sqlalchemy.orm import  backref


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime() , primary_key=True) 

    artist = db.relationship("Artist", backref=backref("shows", cascade="all, delete-orphan" ))
    venue = db.relationship("Venue", backref=backref("shows", cascade="all, delete-orphan" ))
 



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
    artist = db.relationship("Artist", secondary="shows", lazy=False)

    def __repr__(self):
      return f'''<Venue ID: {self.id},\n   name: {self.name }, genres: {self.genres}, 
                  city: {self.city},   state: {self.state }, address: {self.address},
                  phone : {self.phone},   website: {self.website }, seeking_talent: {self.seeking_talent},
                  seeking_description : {self.seeking_description},   image_link: {self.image_link }, 
                  facebook_link: {self.facebook_link} , artist : {self.artist}>''' 

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
    venue = db.relationship("Venue", secondary="shows", lazy=False)


    def __repr__(self):
      return f'''<Artist ID: {self.id},\n   name: {self.name }, genres: {self.genres}, 
                  city: {self.city},   state: {self.state }, phone : {self.phone},   
                  website: {self.website }, seeking_venue: {self.seeking_venue},
                  seeking_description : {self.seeking_description},   image_link: {self.image_link }, 
                  facebook_link: {self.facebook_link} >''' 




# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

