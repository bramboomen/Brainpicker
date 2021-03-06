from __init__ import log as logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
from database import base,\
    Article, Reference,\
    Person, PeopleRel,\
    Organisation, OrganisationRel,\
    Location, LocationRel


class DBSession:

    def __init__(self):
        # engine = create_engine('postgresql://braindb@localhost/braindb')
        engine = create_engine('sqlite:///brain.db')
        base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def insert_article(self, art):
        exists = self.session.query(Article).filter_by(url=art['url']).first()
        article = Article(url=art['url'], title=art['title'], date=art['date'])
        if not exists:
            self.session.add(article)
            logger.write_log("added: " + art['title'] + " to Database")
        self.session.commit()

    def insert_reference(self, ref):
        # Generate unique id for db
        sha_id = hashlib.sha1(bytes(ref['url'] + ref['ref'], 'utf-8'))
        ref['id'] = sha_id.hexdigest()
        exists = self.session.query(Reference).filter_by(id=ref['id']).first()
        if not exists:
            reference = Reference(id=ref['id'], url=ref['url'], ref=ref['ref'])
            self.session.add(reference)
            logger.write_log("added reference from: " + ref['url'] + " to: " + ref['ref'])
        self.session.commit()

    def insert_person(self, person):
        exists = self.session.query(Person).filter_by(name=person['name']).first()
        if not exists:
            pers = Person(name=person['name'])
            self.session.add(pers)
            logger.write_log("added: " + person['name'] + " to database")
        self.session.commit()

    def insert_person_rel(self, rel):
        sha_id = hashlib.sha1(bytes(rel['article'] + rel['person'], 'utf-8'))
        rel['id'] = sha_id.hexdigest()
        exists = self.session.query(PeopleRel).filter_by(id=rel['id']).first()
        if not exists:
            relation = PeopleRel(id=rel['id'],
                                 article=rel['article'],
                                 person=rel['person'],
                                 count=rel['count'],
                                 main_person=rel['main'])
            self.session.add(relation)
            logger.write_log("added relation from: " + rel['article'] + " to: " + rel['person'])
        self.session.commit()

    def insert_organisation(self, organisation):
        exists = self.session.query(Organisation).filter_by(name=organisation['name']).first()
        if not exists:
            org = Organisation(name=organisation['name'])
            self.session.add(org)
            logger.write_log("added: " + organisation['name'] + " to database")
        self.session.commit()

    def insert_organisation_rel(self, rel):
        sha_id = hashlib.sha1(bytes(rel['article'] + rel['organisation'], 'utf-8'))
        rel['id'] = sha_id.hexdigest()
        exists = self.session.query(OrganisationRel).filter_by(id=rel['id']).first()
        if not exists:
            relation = OrganisationRel(id=rel['id'],
                                       article=rel['article'],
                                       organisation=rel['organisation'],
                                       count=rel['count'])
            self.session.add(relation)
            logger.write_log("added relation from: " + rel['article'] + " to: " + rel['organisation'])
        self.session.commit()

    def insert_location(self, location):
        exists = self.session.query(Location).filter_by(name=location['name']).first()
        if not exists:
            loc = Location(name=location['name'])
            self.session.add(loc)
            logger.write_log("added: " + location['name'] + " to database")
        self.session.commit()

    def insert_location_rel(self, rel):
        sha_id = hashlib.sha1(bytes(rel['article'] + rel['location'], 'utf-8'))
        rel['id'] = sha_id.hexdigest()
        exists = self.session.query(LocationRel).filter_by(id=rel['id']).first()
        if not exists:
            relation = LocationRel(id=rel['id'],
                                   article=rel['article'],
                                   location=rel['location'],
                                   count=rel['count'])
            self.session.add(relation)
            logger.write_log("added relation from: " + rel['article'] + " to: " + rel['location'])
        self.session.commit()

    def commit(self):
        self.session.commit()
