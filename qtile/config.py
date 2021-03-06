#                                                                                                                
#                                                                                                                
#                                                  /')                                                           
#      ____        ____        ,____             /' /'     O           ____               ____                   
#    /'    )--   /'    )--    /'    )         -/'--'     /'          /'    )            /'    )--         /'    /
#  /'          /'    /'     /'    /'         /'        /'          /'    /'           /'    /'          /'    /' 
# (___,/      (___,/'     /'    /(__       /(_____    (__         (___,/(__  O      /(___,/'           (___,/(__ 
#                                        /'                          /'           /'                      /'     
#                                      /'                    /     /'           /'                /     /'       
#                                    /'                     (___,/'           /'                 (___,/'         
# 
import os
import subprocess
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])

mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Change float back to tile

    Key([mod], "t", lazy.window.toggle_floating()),

    # Launch different programs
    Key([mod], "p", lazy.spawn("rofi -show run"), desc="run rofi"),
    Key([mod], "i", lazy.spawn("pcmanfm"), desc="run pcman"),
    Key([mod], "f", lazy.spawn("firefox-developer-edition"), desc="run firefox"),
    Key([mod], "c", lazy.spawn("code-oss"), desc="run vscode"),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
           # Key(
           #     [mod, "shift"],
           #     i.name,
           #     lazy.window.togroup(i.name, switch_group=True),
           #     desc="Switch to & move focused window to group {}".format(i.name),
           # ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
             Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                 desc="move focused window to group {}".format(i.name)),
        ]
    )
#
colors = {
    'black': '#32302F',
    'green': '#B8BB26',
    'red': '#F46565',
    'dark_yellow': '#DF9555',
    'dark_magenta': '#9F6B67',
    'whiteish': '#F5E2A9',
    'blue': '#83A598'

}

layouts = [
     layout.Max(),
     layout.MonadTall(
         margin = 15,
         border_focus = colors['green'],
         border_normal = colors['dark_yellow'],
         border_width = 4
         ),
]

widget_defaults = dict(
    font="Cascadia Code",
    fontsize=14,
    padding=5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(

            [
                widget.CurrentLayout(
                foreground = colors['green']),
                widget.Sep(foreground = colors['dark_yellow']),
                widget.GroupBox(
                    background = colors['black'],
                    rounded = True,
                    highlight_method = "text",
                    inactive = colors['dark_magenta'],
                    active = colors['whiteish'],
                    this_current_screen_border = colors['red'],
                    ),

                widget.Sep(foreground = colors['dark_yellow'], padding=3),
                #widget.Prompt(),
                widget.WindowName(
                max_chars = 40,
                foreground = colors['green']),
                widget.CPU(foreground=colors['green']),
                widget.Sep(foreground = colors['dark_yellow']),
                widget.Memory(foreground=colors['green'], measure_mem='G'),
                widget.Sep(foreground = colors['dark_yellow']),
                widget.Net(foreground=colors['green'], interface='enp4s0'),
                widget.Sep(foreground = colors['dark_yellow']),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %H:%M",
                             foreground = colors['green']),
            ],
            30,

                background = colors['black'],
                # margin = [2, 17, 2, 17],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(

    border_normal = colors['dark_yellow'],
    border_focus = colors['green'],

    border_width = 4,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
