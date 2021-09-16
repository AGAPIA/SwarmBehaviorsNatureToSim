import carla

class SettingsBuilder():

    def get_sync_world_confing():
        return carla.WorldSettings(synchronous_mode=True, no_rendering_mode=False ,fixed_delta_seconds=0.01)

    def get_async_world_config():
        return carla.WorldSettings(synchronous_mode=False, no_rendering_mode=False ,fixed_delta_seconds=0.0)

    def get_world_config(synchronous_mode=True, no_rendering_mode=False ,fixed_delta_seconds=0.01) -> carla.WorldSettings:
        return carla.WorldSettings(synchronous_mode,no_rendering_mode,fixed_delta_seconds)