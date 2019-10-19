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
        self.last_request = datetime.datetime.now()

    def request(self, params=None):
        """
        Sends request and returns response, can set additional additional parameters by passing a dictionary

        :param params:
        :rtype: response object
        """
        params = params if params else dict()
        params['key'] = self.api_key
        try:
            response = requests.get(self.api_url, params=params)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        return response


class GoodReadsAPI(APICall):
    def __init__(self):
        """
        Creates a new instance of APICall by passing GoodReads API URL and key
        """
        super(GoodReadsAPI, self).__init__('https://www.goodreads.com/',
                                           current_app.config['GOODREADS_API_KEY'])
    
    def book_search(self, query):
        """
        Sends a book search request with a provided query. Returns a list of refactored
        dictionaries of found books.

        :param query:
        :rtype: list
        """
        self.api_url += 'search/index.xml'
        request = {'q': query}
        try:
            response = self.request(request)
            if response.status_code == 401:
                raise InvalidApiKeyException("Provided API key is not valid")
        except (requests.exceptions.RequestException, InvalidApiKeyException) as e:
            print(e)
            return []
        parsed_response = XMLParser.to_dict(response.text)
        if parsed_response['GoodreadsResponse']['search']['total-results'] == '0':
            return []
        else:
            return self.__refactor_search_dict(parsed_response['GoodreadsResponse']['search']['results']['work'])

    def get_book(self, bid):
        """
        Sends a book request with a provided GoodReads BookID. Returns a dictionary containing
        information about the book

        :param bid:
        :return:
        """
        self.api_url += f'book/show/{bid}.xml'
        try:
            response = self.request()
            if response.status_code == 401:
                raise InvalidApiKeyException("Provided API key is not valid")
        except (requests.exceptions.RequestException, InvalidApiKeyException) as e:
            print(e)
            return []
        print(self.last_request)
        return self.__refactor_book_dict(XMLParser.to_dict(response.text)['GoodreadsResponse']['book'])

    @staticmethod
    def __refactor_search_dict(books):
        result = []
        for book in books:
            book_info = dict()
            book_info['id'] = book['best_book']['id']['#text']
            book_info['title'] = book['best_book']['title']
            if '#text' in book['original_publication_year']:
                book_info['year'] = book['original_publication_year']['#text']
            else:
                book_info['year'] = 'Unknown Year'
            if type(book['best_book']['author']) is list:
                book_info['author'] = [author['name'] for author in book['best_book']['author']]
            else:
                book_info['author'] = [book['best_book']['author']['name']]
            book_info['img_url'] = book['best_book']['image_url']
            result.append(book_info)
        return result

    @staticmethod
    def __refactor_book_dict(book):
        book_info = dict()
        book_info['title'] = book['title']
        book_info['img_url'] = book['image_url']
        if type(book['authors']['author']) is list:
            book_info['author'] = [author['name'] for author in book['authors']['author']]
        else:
            book_info['author'] = [book['authors']['author']['name']]
        if 'publication_year' in book:
            book_info['year'] = book['publication_year']
        else:
            book_info['year'] = 'Unknown Year'

        book_info['isbn'] = book['isbn'] or book['isbn13']
        return book_info


class XMLParser(object):
    @staticmethod
    def to_dict(xml_string):
        """Converts the XML string into a dictionary using xmltodict module"""
        return xmltodict.parse(xml_string)


class InvalidApiKeyException(Exception):
    """Exception raised for invalid GoodReads API Key in config"""
    def __init__(self, message):
        self.message = '[GoodReadsAPI Error]: ' + message
        super().__init__(self.message)
