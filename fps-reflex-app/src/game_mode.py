class GameMode:
    MODES = {
        "quick": {"name": "10 Targets", "targets": 10},
        "normal": {"name": "20 Targets", "targets": 20},
        "burst": {"name": "Burst - 30 Targets", "targets": 30},
        "extended": {"name": "50 Targets", "targets": 50}
    }

    @staticmethod
    def get_mode_info(mode_key):
        return GameMode.MODES.get(mode_key)

    @staticmethod
    def get_all_modes():
        return GameMode.MODES
