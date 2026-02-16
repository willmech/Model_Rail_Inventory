from rail_inventory.database.db import initialize_database
from rail_inventory.gui.app import run_qt_app

from PySide6.QtCore import QLibraryInfo
import os


def main() -> None:
    initialize_database()

    # Ensure Qt can find its platform plugins (macOS cocoa)
    plugins_path = QLibraryInfo.path(QLibraryInfo.PluginsPath)
    os.environ.setdefault("QT_PLUGIN_PATH", plugins_path)
    os.environ.setdefault(
        "QT_QPA_PLATFORM_PLUGIN_PATH",
        os.path.join(plugins_path, "platforms"),
    )

    run_qt_app()


if __name__ == "__main__":
    main()
