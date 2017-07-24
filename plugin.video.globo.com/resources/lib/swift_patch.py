import xbmcswift2


def patch():
    # set_resolved_url to receive a listItem dict
    xbmcswift2.Plugin.set_resolved_url = set_resolved_url
    # ListItem addStreamInfo implementation
    xbmcswift2.ListItem.add_stream_info = add_stream_info
    # for cli only
    try:
        xbmcswift2.mockxbmc.xbmcgui.ListItem.__init__ = __init__
        xbmcswift2.mockxbmc.xbmcgui.ListItem.addStreamInfo = addStreamInfo
    except:
        pass


def set_resolved_url(self, url=None, mimetype=None, succeeded=True):
    if isinstance(url, basestring):
        item = xbmcswift2.ListItem(path=url)
    elif type(url) == dict:
        item = xbmcswift2.ListItem.from_dict(**url)
    elif succeeded:
        msg = ('set_resolved_url accepts a url or dict item when resolve '
               + 'success, or you have to call it with succeeded=False.')
        assert False, msg
    else:
        # dummy item for the failed setResolvedUrl call only.
        item = xbmcswift2.ListItem()
    if mimetype:
        item.set_property('mimetype', mimetype)
    item.set_played(True)
    if not self._end_of_directory:
        xbmcswift2.xbmcplugin.setResolvedUrl(self.handle, succeeded,
                                             item.as_xbmc_listitem())
        # prevent from auto call endOfDirectory, which will not work
        # because the handle already be erased by xbmc
        self._end_of_directory = True
        return [item]
    assert False, 'Already called endOfDirectory or setResolvedUrl.'


def add_stream_info(self, type, values):
    '''Sets the listitems streamInfo'''
    if hasattr(self._listitem, 'addStreamInfo'):
        return self._listitem.addStreamInfo(type, values)
    else:
        if 'duration' in values and isinstance(values['duration'], int):
            from datetime import timedelta
            values['duration'] = str(timedelta(seconds=values['duration']))
        self._listitem.setInfo(type, values)


def __init__(self, label=None, label2=None, iconImage=None,
             thumbnailImage=None, path=None):
    self.label = label
    self.label2 = label2
    self.iconImage = iconImage
    self.thumbnailImage = thumbnailImage
    self.path = path
    self.properties = {}
    self.stream_info = {}
    self.selected = False
    self.infolabels = {}


def addStreamInfo(self, stream_type, stream_values):
    self.stream_info.update({stream_type: stream_values})
