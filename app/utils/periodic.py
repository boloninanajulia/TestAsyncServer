import logging

import asyncio
from contextlib import suppress

logger = logging.getLogger(__name__)


class Periodic:
    def __init__(self, func, time: int):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self) -> None:
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._run())

    async def stop(self) -> None:
        if self.is_started:
            self.is_started = False
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self) -> None:
        try:
            while True:
                await asyncio.gather(
                    self.func(),
                    asyncio.sleep(self.time),
                )
        except Exception as ex:
            logging.error(ex)
