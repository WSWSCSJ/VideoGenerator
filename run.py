from typing import Optional, Awaitable

import tornado.ioloop
import tornado.web
from tornado.web import MissingArgumentError
from loguru import logger

from service.process import Process


class VideoGeneratorHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_argument_no_error(self, key):
        try:
            result = self.get_body_argument(key)
        except MissingArgumentError:
            return None
        except Exception as e:
            logger.error(e)
            return None
        else:
            return result

    def post(self):
        process = Process(self)
        video_stream = process.run
        if not video_stream:
            logger.error(process.failure)
        self.set_header('Content-Type', 'video/mp4')
        self.set_header('Content-Disposition', 'attachment; filename=video.mp4')
        self.write(video_stream)
        self.finish()


app = tornado.web.Application([(r"/video", VideoGeneratorHandler)])
app.listen(5000)
tornado.ioloop.IOLoop.current().start()
