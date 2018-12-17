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
    

    def getFullName(self):
        return '{}, {} {} {}'.format(self.nameLast,self.nameFirst,self.nameMiddle,self.nameExt)


class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True)
    #
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # this cannot be changed even if the type of the person has changed
    # non-retroactivity
    type = db.Column(db.String(100),default='')
    #
    timeIn = db.Column(db.BIGINT,default=0)
    timeInBy = db.Column(db.String(100),default='') # SCross:Sistine Cross
    timeOut = db.Column(db.BIGINT,default=0)
    timeOutBy = db.Column(db.String(100),default='') # SCross:Sistine Cross
    
    # audit
    deletedAt = db.Column(db.BIGINT,default=0)
    deletedBy = db.Column(db.String(100),default='')
    
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    nameFirst = db.Column(db.String(100),default='')
    nameLast = db.Column(db.String(100),default='')
    nameMiddle = db.Column(db.String(100),default='')
    nameExt = db.Column(db.String(100),default='')
    # audit
    updatedAt = db.Column(db.BIGINT,default=0)
    updatedBy = db.Column(db.String(100),default='')
    deletedAt = db.Column(db.BIGINT,default=0)
    deletedBy = db.Column(db.String(100),default='')
    # claims
    access = db.Column(db.String(100),default='')
    
    def getFullName(self):
        return '{}, {} {} {}'.format(self.nameLast,self.nameFirst,self.nameMiddle,self.nameExt)
        
    pass # end class
    
    
    
    
    

# Create Tables
if __name__ == "__main__":
    db.drop_all()
    db.create_all()
