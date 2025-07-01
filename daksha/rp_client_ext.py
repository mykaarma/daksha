from reportportal_client import RPClient as _RPClient

class RPClient(_RPClient):
    """
    Extension of the official Report-Portal client that lets you pass
    launch_uuid explicitly when finishing a launch.
    """

    def finish_launch(self,
                      end_time,
                      status=None,
                      attributes=None,
                      launch_uuid=None,
                      **kwargs):
        if launch_uuid:                          # accept optional UUID
            self.launch_id = launch_uuid         # sync both holders
            self._log_manager.launch_id = launch_uuid
        return super().finish_launch(end_time=end_time,
                                     status=status,
                                     attributes=attributes,
                                     **kwargs)