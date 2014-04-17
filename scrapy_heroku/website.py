from datetime import datetime

from twisted.web import resource, static
from twisted.application.service import IServiceCollection

from scrapy.utils.misc import load_object
from scrapyd.website import Root, Home, Jobs

from scrapyd.interfaces import IPoller, IEggStorage, ISpiderScheduler


class Root(Root):

    def __init__(self, config, app):
        resource.Resource.__init__(self)
        self.debug = config.getboolean('debug', False)
        self.runner = config.get('runner')
        logsdir = config.get('logs_dir')
        itemsdir = config.get('items_dir')
        show_home = config.getboolean('show_home', False)
        show_jobs = config.getboolean('show_jobs', False)
        self.app = app
        if show_home:
            self.putChild('', Home(self))
        else:
            self.putChild('', Blank(self))
        if logsdir:
            self.putChild('logs', static.File(logsdir, 'text/plain'))
        if itemsdir:
            self.putChild('items', static.File(itemsdir, 'text/plain'))
        if show_jobs:
            self.putChild('jobs', Jobs(self))
        services = config.items('services', ())
        for servName, servClsName in services:
            servCls = load_object(servClsName)
            self.putChild(servName, servCls(self))
        self.update_projects()


class Blank(resource.Resource):

    def __init__(self, root):
        resource.Resource.__init__(self)
        self.root = root

    def render_GET(self, txrequest):
        return ""
