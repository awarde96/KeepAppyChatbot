from requests import get, post
from typing import Callable


class Event:
    """
    Event class hanldes parsing and callback methods.
    Callback Manager allows you to set et use callback methods for each event
    type :
    - message
    - postback
    - read
    - delivery
    - optin
    """

    REPLY_URI = '/me/messages'
    GRAPH_URL = 'graph.facebook.com/v2.6'

    def __init__(self, sender_id: str, recipient_id: str,
                 page_id: str, page_token: str) -> None:
        """
        Init for Event.
        """
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.page_id = page_id
        self.page_token = page_token

        self.timestamp = None
        self.event_type = None
        self.content = None
        self.raw = None

    @staticmethod
    def from_json(json_data: dict, page_id: str, page_token: str) -> object:
        """
        Parse and event from facebook
        Returns:
            an Event instance
        """
        event = Event(json_data['sender']['id'], json_data['recipient']['id'],
                      page_id, page_token)
        json_data.pop('sender')
        json_data.pop('recipient')

        if 'timestamp' in json_data:
            event.timestamp = json_data['timestamp']
            json_data.pop('timestamp')

        event.event_type = next(iter(json_data.keys()))
        event.content = json_data[event.event_type]
        event.raw = json_data
        return event

    def user_info(self) -> dict:
        req = get(url="https://{graph_url}/{sender_id}"
                  .format(
                      graph_url=self.GRAPH_URL,
                      sender_id=self.sender_id),
                  params={
                      'fiels': 'first_name,last_name,profile_pic,\
                      locale,timezone,gender',
                      'access_token': self.page_token
                      }
                  )
        return req.json()

    def signal(self, signal_type: str) -> None:
        signal = {
            'recipient': {
                'id': self.sender_id,
            },
            'sender_action': signal_type
        }
        post('https://{graph_url}{reply_uri}?access_token={token}'
             .format(graph_url=self.GRAPH_URL,
                     reply_uri=self.REPLY_URI,
                     token=self.page_token), json=signal)

    def reply(self, msg: dict) -> None:
        """
        This function allows sending a message to the user that triggered the event.
        Args:
            msg (dict): the content of the message to send back to the user
        """
        data = {
            'recipient': {
                'id': self.sender_id,
            },
            'message': msg,
        }
        post('https://{graph_url}{reply_uri}?access_token={token}'
             .format(graph_url=self.GRAPH_URL,
                     reply_uri=self.REPLY_URI,
                     token=self.page_token), json=data)

    def send_file(self, data: dict) -> None:
        """
        This function allows sending files to the user that triggered the event.
        Args:
            data (dict): form-data files to send back to the user
        """
        data = {
            'recipient': {
                'id': self.sender_id,
            },
            'message': {
                "attachment": {
                    "type": "image",
                    "payload": { "is_reusable": False }
                }
            },
            'filedata': '@{path};type=image/{type}'.format(path=data.path, type=data.type),
        }
        post('https://{graph_url}{reply_uri}?access_token={token}'
             .format(graph_url=self.GRAPH_URL,
                     reply_uri=self.REPLY_URI,
token=self.page_token), data=data)
