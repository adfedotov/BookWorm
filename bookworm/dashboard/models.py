from .. import db
import datetime
import requests
from flask import current_app
import xmltodict


class Note(db.Model):
    __tablename__ = 'NOTES'

    nid = db.Column('NID', db.Integer, primary_key=True)  # NoteID
    uid = db.Column('UID', db.Integer, db.ForeignKey('USERS.UID'), nullable=False)  # UserID
    bid = db.Column('BID', db.String(13), nullable=False)  # BookID
    note = db.Column('NoteText', db.String)  # Note text
    last_update = db.Column('LastUpdate', db.DateTime, nullable=False)  # Last updated

    def __init__(self, uid, bid):
        """
        Constructor to create a note instance in the database

        :param uid:
        :param bid:
        """
        self.uid = uid
        self.bid = bid

    def __repr__(self):
        return f'<Note {self.nid}>'

    def set_note(self, note):
        """
        Sets note body text

        :param note:
        :rtype: str
        """
        self.note = note

    def update_date(self):
        """
        Updates the last updated field
        """
        self.last_update = datetime.datetime.now()

    @staticmethod
    def get_note(uid, bid):
        """
        Returns note if exists or None if not

        :param uid:
        :param bid:
        """
        return Note.query.filter_by(uid=uid, bid=bid).first()

    @staticmethod
    def get_user_notes(uid):
        """
        Returns a list of tuples with ISBN codes

        :param uid:
        """
        return Note.query.filter_by(uid=uid).order_by(Note.last_update.desc()).all()


class APICall(object):
    def __init__(self, api_url, api_key):
        """
        Constructor for the APICall. Sets API URL and API key

        :param api_url:
        :param api_key:
        """
        self.api_url = api_url
        self.api_key = api_key

    def request(self, params={}):
        """
        Sends request and returns response text, can set additional additional parameters by passing a dictionary

        :param params:
        :rtype: str
        """
        params['key'] = self.api_key
        response = requests.get(self.api_url, params=params)
        return response.text


class GoodReadsAPI(APICall):
    def __init__(self):
        """
        Creates a new instance of APICall by passing GoodReads API URL and key
        """
        super(GoodReadsAPI, self).__init__('https://www.goodreads.com/',
                                           current_app.config['GOODREADS_API_KEY'])
    
    def book_search(self, query):  # TODO: Error Handling
        """
        Sends a book search request with a provided query. Returns a list of refactored
        dictionaries of found books.

        :param query:
        :rtype: list
        """
        self.api_url += 'search/index.xml'
        request = {'q': query}
        response = self.request(request)
        return self.__refactor_search_dict(XMLParser.to_dict(response)['GoodreadsResponse']['search']['results']['work'])

    def get_book(self, bid):
        """
        Sends a book request with a provided GoodReads BookID. Returns a dictionary containing
        information about the book

        :param bid:
        :return:
        """
        self.api_url += f'book/show/{bid}.xml'
        response = self.request()
        return self.__refactor_book_dict(XMLParser.to_dict(response)['GoodreadsResponse']['book'])

    @staticmethod
    def __refactor_search_dict(books):
        result = []
        for book in books:
            book_info = dict()
            book_info['id'] = book['best_book']['id']['#text']
            book_info['title'] = book['best_book']['title']
            book_info['year'] = book['original_publication_year']['#text']
            if type(book['best_book']['author']) is list:
                book_info['author'] = book['best_book']['author'][0]['name']
            else:
                book_info['author'] = book['best_book']['author']['name']
            book_info['img_url'] = book['best_book']['image_url']
            result.append(book_info)
        return result

    @staticmethod
    def __refactor_book_dict(book):
        book_info = dict()
        book_info['title'] = book['title']
        book_info['img_url'] = book['image_url']
        # if a book has multiple authors, only the first one will be returned TODO: Allow multiple authors
        if type(book['authors']['author']) is list:
            book_info['author'] = book['authors']['author'][0]['name']
        else:
            book_info['author'] = book['authors']['author']['name']
        book_info['year'] = book['publication_year']
        book_info['isbn'] = book['isbn'] or book['isbn13']
        return book_info


class XMLParser(object):
    # TODO: Implement own parser
    @staticmethod
    def to_dict(xml_string):
        """Converts the XML string into a dictionary using xmltodict module"""
        return xmltodict.parse(xml_string)
