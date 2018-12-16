from app import db

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    nameFirst = db.Column(db.String(100),default='')
    nameLast = db.Column(db.String(100),default='')
    nameMiddle = db.Column(db.String(100),default='')
    nameExt = db.Column(db.String(100),default='')
    contactTel = db.Column(db.String(100),default='')
    contactMobile = db.Column(db.String(100),default='')
    contactEmail = db.Column(db.String(100),default='')
    # audit
    updatedAt = db.Column(db.BIGINT,default=0)
    updatedBy = db.Column(db.String(100),default='')
    deletedAt = db.Column(db.BIGINT,default=0)
    deletedBy = db.Column(db.String(100),default='')
    #
    type = db.Column(db.String(100),default='')


class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True)
    #
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    
    type = db.Column(db.String(100),default='')
    #
    timeIn = db.Column(db.BIGINT,default=0)
    timeOut = db.Column(db.BIGINT,default=0)
    
    # audit
    updatedAt = db.Column(db.BIGINT,default=0)
    updatedBy = db.Column(db.String(100),default='')
    deletedAt = db.Column(db.BIGINT,default=0)
    deletedBy = db.Column(db.String(100),default='')
    
    

# Create Tables
if __name__ == "__main__":
    db.drop_all()
    db.create_all()
