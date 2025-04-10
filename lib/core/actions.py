"""
🎮 Core Action Registry
Ce fichier centralise toutes les actions disponibles dans l’application.
Chaque action est importée depuis son module dédié dans `actions/`.

📌 Usage recommandé :
    from core.actions import KThemeAction, KQuitAction

⚠️ Ne contient **aucune instance**, uniquement les classes d’actions !
"""

from actions.kactions import KAction, KWidgetAction, KCheckableAction

# ───────────────────── 🎨 Theme Actions
from actions.kthemesactions import (
    KThemeAction,            # Sélection d’un thème par nom
    KThemeModeAction         # Sélection d’un mode (system/light/dark)
)

# ───────────────────── 🌍 Lang Actions
from actions.klangsaction import (
    KLangsAction              # Sélection de la langue
)

# ───────────────────── 🧪 Debug / Dev Tools (si utiles)
# from actions.kdebugactions import (
#     KShowDebugConsoleAction
# )

# ───────────────────── 💾 VPN Client Actions
from actions.kvpnactions import (
    KStartVpnAction, KStartVpnFullAction, KStartVpnShortAction,
    KStopVpnAction, KStopVpnFullAction, KStopVpnShortAction,
    KRefreshVpnAction, KRefreshVpnFullAction, KRefreshVpnShortAction,
    KOpenTerminalAction, KOpenTerminalFullAction, KOpenTerminalShortAction,
    KOpenBrowserAction, KOpenBrowserFullAction, KOpenBrowserShortAction,
    KToggleAutoStartVpnAction,
)
from actions.kclientactions import (
    KToggleFavoriteAction, KDeleteClientAction
)

# ───────────────────── Manager(App) Actions (❌ Quit / Logs / Misc)
from actions.kmanageractions import (
    KSwitchViewAction,
    KToggleTooltipsAction,
    KOpenAddClientAction,
    KOpenProfilesManagerAction,
    KOpenLogConsoleAction,
    KQuitAppAction
)
# from actions.klogsactions import KOpenLogsAction

# ───────────────────── Exports publics
__all__ = [
    # Basics Actions
    "KAction", "KWidgetAction", "KCheckableAction",
    # Manager Actions (App)
    "KSwitchViewAction",
    "KOpenAddClientAction",
    "KOpenProfilesManagerAction",
    "KOpenLogConsoleAction",
    "KToggleTooltipsAction",
    "KQuitAppAction",
    
    # Themes
    "KThemeAction", "KThemeModeAction",

    # Langs
    "KLangsAction",

    # VPN Actions 
    "KStartVpnAction", "KStartVpnFullAction", "KStartVpnShortAction",
    "KStopVpnAction", "KStopVpnFullAction", "KStopVpnShortAction",
    "KRefreshVpnAction", "KRefreshVpnFullAction", "KRefreshVpnShortAction",
    "KOpenTerminalAction", "KOpenTerminalFullAction", "KOpenTerminalShortAction",
    "KOpenBrowserAction", "KOpenBrowserFullAction", "KOpenBrowserShortAction",
    "KToggleAutoStartVpnAction",

    # Client Actions
    "KToggleFavoriteAction", "KDeleteClientAction"
]
