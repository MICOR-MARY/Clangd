# Copyright (C) 2017 YouCompleteMe contributors
#
# This file is part of YouCompleteMe.
#
# YouCompleteMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YouCompleteMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.
import json
from unittest import mock
HTTP_OK = 200


class FakeResponse:
  """A fake version of a requests response object, just about suitable for
  mocking a server response. Not usually used directly. See
  MockServerResponse* methods"""
  def __init__( self, response, exception ):
    self._json = response
    self._exception = exception
    self.code = HTTP_OK


  def read( self ):
    if self._exception:
      raise self._exception
    return json.dumps( self._json ).encode( 'utf-8' )


  def close( self ):
    pass


class FakeFuture:
  """A fake version of a future response object, just about suitable for
  mocking a server response as generated by PostDataToHandlerAsync.
  Not usually used directly. See MockAsyncServerResponse* methods"""
  def __init__( self, done, response = None, exception = None ):
    self._done = done

    if not done:
      self._result = None
    else:
      self._result = FakeResponse( response, exception )


  def done( self ):
    return self._done


  def result( self ):
    return self._result


def MockAsyncServerResponseDone( response ):
  """Return a MessagePoll containing a fake future object that is complete with
  the supplied response message. Suitable for mocking a response future within
  a client request. For example:

  with MockVimBuffers( [ current_buffer ], [ current_buffer ], ( 1, 1 ) ) as v:
    mock_response = MockAsyncServerResponseDone( response )
    with patch.dict( ycm._message_poll_requests, {} ):
      ycm._message_poll_requests[ filetype ] = MessagesPoll( v.current.buffer )
      ycm._message_poll_requests[ filetype ]._response_future = mock_response
      # Needed to keep a reference to the mocked dictionary
      mock_future = ycm._message_poll_requests[ filetype ]._response_future
      ycm.OnPeriodicTick() # Uses ycm._message_poll_requests[ filetype ] ...
  """
  return mock.MagicMock( wraps = FakeFuture( True, response ) )


def MockAsyncServerResponseInProgress():
  """Return a fake future object that is incomplete. Suitable for mocking a
  response future within a client request. For example:

  with MockVimBuffers( [ current_buffer ], [ current_buffer ], ( 1, 1 ) ) as v:
    mock_response = MockAsyncServerResponseInProgress()
    with patch.dict( ycm._message_poll_requests, {} ):
      ycm._message_poll_requests[ filetype ] = MessagesPoll( v.current.buffer )
      ycm._message_poll_requests[ filetype ]._response_future = mock_response
      # Needed to keep a reference to the mocked dictionary
      mock_future = ycm._message_poll_requests[ filetype ]._response_future
      ycm.OnPeriodicTick() # Uses ycm._message_poll_requests[ filetype ] ...
  """
  return mock.MagicMock( wraps = FakeFuture( False ) )


def MockAsyncServerResponseException( exception ):
  """Return a fake future object that is complete, but raises an exception.
  Suitable for mocking a response future within a client request. For example:

  with MockVimBuffers( [ current_buffer ], [ current_buffer ], ( 1, 1 ) ) as v:
    mock_response = MockAsyncServerResponseException( exception )
    with patch.dict( ycm._message_poll_requests, {} ):
      ycm._message_poll_requests[ filetype ] = MessagesPoll( v.current.buffer )
      ycm._message_poll_requests[ filetype ]._response_future = mock_response
      # Needed to keep a reference to the mocked dictionary
      mock_future = ycm._message_poll_requests[ filetype ]._response_future
      ycm.OnPeriodicTick() # Uses ycm._message_poll_requests[ filetype ] ...
  """
  return mock.MagicMock( wraps = FakeFuture( True, None, exception ) )


# TODO: In future, implement MockServerResponse and MockServerResponseException
# for synchronous cases when such test cases are needed.
