from reportportal_client import RPClient as _RPClient  # type: ignore
from engine.logs import logger

class RPClient(_RPClient):
    """Extended Report-Portal client.

    Adds an optional *launch_uuid* parameter to ``finish_launch`` so you can
    explicitly specify which launch to close **without** mutating the
    ``launch_id`` attribute on the client (which is read-only in recent
    library versions).
    """

    def finish_launch(
        self,
        *,
        end_time,
        status=None,
        attributes=None,
        launch_uuid=None,
        **kwargs,
    ):  # pylint: disable=arguments-differ
        # If caller supplies an explicit launch UUID, use it; otherwise fall
        # back to the one stored in the client instance.
        target_launch = launch_uuid or self.launch_id

        # Safety check
        if not target_launch:
            from reportportal_client.static.defines import NOT_FOUND  # type: ignore
            if self.launch_id is NOT_FOUND or not self.launch_id:
                # Mirror the original behaviour

                logger.warning(
                    "Attempt to finish non-existent launch"
                )
                return

        # Construct the same request as the base class but using **target_launch**
        from reportportal_client.helpers import uri_join  # type: ignore
        from reportportal_client.core.rp_requests import LaunchFinishRequest  # type: ignore
        from reportportal_client.core.rp_requests import HttpRequest  # type: ignore

        url = uri_join(self.base_url_v2, "launch", target_launch, "finish")
        request_payload = LaunchFinishRequest(
            end_time,
            status=status,
            attributes=attributes,
            description=kwargs.get("description"),
        ).payload

        response = HttpRequest(
            self.session.put,
            url=url,
            json=request_payload,
            verify_ssl=self.verify_ssl,
            name="Finish Launch",
        ).make()

        if not response:
            return

        # Log and return response like original implementation
        import logging

        logger.debug(f"response message: {response}")
        return response.message
        