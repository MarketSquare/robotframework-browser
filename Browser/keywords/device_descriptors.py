import json

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger


class Devices(LibraryComponent):
    @keyword(tags=["DeviceDescriptor"])
    def get_devices(self):
        """ Return a dict of all playwright device descriptors.

            See Playwright's [https://github.com/Microsoft/playwright/blob/master/src/deviceDescriptors.ts | deviceDescriptors.ts]
            for a formatted list.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDevices(Request().Empty())
            logger.debug(response.log)
            return json.loads(response.body)

    @keyword(tags=["DeviceDescriptor"])
    def get_device(self, name: str):
        """ Get a single device decriptor with name exactly matching name.

            Allows a concise syntax to set website testing values to exact matches of specific
            mobile devices.

            Use by passing to a context. After creating a context with devicedescriptor,
            before using ensure your active page is on that context.
            Usage:

            | ${device}=   | Get Device        | iPhone X
            |              | New Context       | &{device}
            |              | New Page          |
            |              | Get Viewport Size | returns { "width": 375, "height": 812 }
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDevice(Request().Device(name=name))
            logger.debug(response.log)
            return json.loads(response.body)
