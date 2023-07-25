# coding: utf-8
from __future__ import unicode_literals
import sys
import os
import re
import webbrowser
import zipfile

sys.path.append(".")
from yurlungur.user import winapi

try:
    sys.modules[__name__] = sys.modules["pymxs"]
    import yurlungur

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        setattr(sys.modules[__name__], obj, getattr(yurlungur, obj))

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, quit, connect = __App("3dsmax")._actions

    __all__ = ["run", "shell", "quit", "connect"]


__version__ = "0.11.0"
DEFAULT_DOCS_VERSION = "2019"

# Holds the current 3ds Max window object that we send commands to.
# It is filled automatically when sending the first command.
mainwindow = None

# Used to preselect the last 3ds Max window in the quick panel.
last_index = 0

ONLINE_MAXSCRIPT_HELP_URL = {
    "2014": r"http://docs.autodesk.com/3DSMAX/16/ENU/MAXScript-Help/index.html",  # noqa
    "2015": r"http://help.autodesk.com/view/3DSMAX/2015/ENU/index.html",
    "2016": r"http://help.autodesk.com/view/3DSMAX/2016/ENU/index.html",
    "2017": r"http://help.autodesk.com/view/3DSMAX/2017/ENU/index.html",
    "2018": r"http://help.autodesk.com/view/3DSMAX/2018/ENU/index.html",
    "2019": r"http://help.autodesk.com/view/3DSMAX/2019/ENU/index.html",
}

APIPATH = os.path.dirname(os.path.realpath(__file__)) + "\maxscript.api"

# Create the tempfile in "Installed Packages".
TEMPFILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "send_to_3ds_max_temp.ms")

TITLE_IDENTIFIER = "Autodesk 3ds Max"
PREFIX = "Sublime3dsMax:"
NO_SUPPORTED_FILE = (PREFIX + " File type not supported, must be of: "
                              "*.ms, *.mcr, *.mcr, *.mse, *.py")
NO_TEMP = PREFIX + " Could not write to temp file"
NOT_SAVED = PREFIX + " File must be saved before sending to 3ds Max"
MAX_NOT_FOUND = PREFIX + " Could not find a 3ds max instance."
RECORDER_NOT_FOUND = PREFIX + " Could not find MAXScript Macro Recorder"


class TextCommand:
    view = None


def _get_api_lines():
    """Read the mxs API definition file and return as a list of lines."""
    def get_decoded_lines(file_obj):
        content = file_obj.read()
        try:
            content = content.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            pass
        return content.split("\n")

    # Zipped .sublime-package as installed by package control.
    if ".sublime-package" in APIPATH:
        apifile = os.path.basename(APIPATH)
        package = zipfile.ZipFile(os.path.dirname(APIPATH), "r")
        return get_decoded_lines(package.open(apifile))
    # Expanded folder, e.g. during development.
    else:
        return get_decoded_lines(open(APIPATH))


def _is_maxscriptfile(filepath):
    """Return if the file uses one of the MAXScript file extensions."""
    name, ext = os.path.splitext(filepath)
    return ext in (".ms", ".mcr", ".mse", ".mzp")


def _is_pythonfile(filepath):
    """Return if the file uses a Python file extension."""
    name, ext = os.path.splitext(filepath)
    return ext in (".py",)


def _save_to_tempfile(text):
    """Store code in a temporary maxscript file."""
    with open(TEMPFILE, "w") as tempfile:
        tempfile.write(text)


def _send_cmd_to_max(cmd):
    """Try to find the 3ds Max window by title and the mini
    macrorecorder by class.

    Sends a string command and a return-key buttonstroke to it to
    evaluate the command.

    """
    global mainwindow

    if mainwindow is None:
        mainwindow = winapi.Window.find_window(
            TITLE_IDENTIFIER)

    if mainwindow is None:
        print(MAX_NOT_FOUND)
        return

    try:
        mainwindow.find_child(text=None, cls="MXS_Scintilla")
    except OSError:
        # Window handle is invalid, 3ds Max has probably been closed.
        # Call this function again and try to find one automatically.
        mainwindow = None
        _send_cmd_to_max(cmd)
        return

    minimacrorecorder = mainwindow.find_child(text=None, cls="MXS_Scintilla")
    # If the mini macrorecorder was not found, there is still a chance
    # we are targetting an ancient Max version (e.g. 9) where the
    # listener was not Scintilla based, but instead a rich edit box.
    if minimacrorecorder is None:
        statuspanel = mainwindow.find_child(text=None, cls="StatusPanel")
        if statuspanel is None:
            print(RECORDER_NOT_FOUND)
            return
        minimacrorecorder = statuspanel.find_child(text=None, cls="RICHEDIT")
        # Verbatim strings (the @ at sign) are also not yet supported.
        cmd = cmd.replace("@", "")
        cmd = cmd.replace("\\", "\\\\")

    if minimacrorecorder is None:
        print(RECORDER_NOT_FOUND)
        return

    print('Send to 3ds Max: {cmd}'.format(
        **locals())[:-1])  # Cut ';'
    cmd = cmd.encode("utf-8")  # Needed for ST3!
    minimacrorecorder.send(winapi.WM_SETTEXT, 0, cmd)
    minimacrorecorder.send(winapi.WM_CHAR, winapi.VK_RETURN, 0)
    minimacrorecorder = None


def _get_max_version():
    """Try to determine the version of 3ds Max we are connected to."""
    global mainwindow
    if mainwindow is None:
        mainwindow = winapi.Window.find_window(
            TITLE_IDENTIFIER)

    # Default to 2018 help, this has the most updated docs and will
    # filter to Maxscript results.
    max_version = DEFAULT_DOCS_VERSION

    if mainwindow is not None:
        window_text = mainwindow.get_text()
        matches = re.findall(r"(?:Max )(2\d{3})", window_text)
        if matches:
            last_match = matches[-1]
            max_version = last_match

    return max_version


class SendFileToMaxCommand(TextCommand):
    """Send the current file by using 'fileIn <file>'."""

    def run(self, edit):
        currentfile = self.view.file_name()
        if currentfile is None:
            print(NOT_SAVED)
            return

        is_mxs = _is_maxscriptfile(currentfile)
        is_python = _is_pythonfile(currentfile)

        if is_mxs:
            cmd = 'fileIn @"{0}"\r\n'.format(currentfile)
            _send_cmd_to_max(cmd)
        elif is_python:
            cmd = 'python.executeFile @"{0}"\r\n'.format(currentfile)
            _send_cmd_to_max(cmd)
        else:
            print(NO_SUPPORTED_FILE)


class SendSelectionToMaxCommand(TextCommand):
    """Send selected part of the file.

    Selection is extended to full line(s).

    """
    def expand(self, line):
        """Expand selection to encompass whole line."""
        self.view.run_command("expand_selection", {"to": line.begin()})

    def run(self, edit):
        """Analyse selection and determine a method to send it to 3ds Max.

        Single line maxscript commands can be send directly. Python
        commands could, but since we wrap them we may get issues with
        quotation marks or backslashes, so it is safer to send them via
        a temporary file that we import. That is also the method to send
        multiline code, since the mini macrorecorder does not accept
        multiline input.
        """
        def get_mxs_tempfile_import():
            return 'fileIn @"{0}"\r\n'.format(TEMPFILE)

        def get_python_tempfile_import():
            return 'python.executeFile @"{0}"\r\n'.format(TEMPFILE)

        # We need the user to have an actual file opened so that we can
        # derive the language from its file extension.
        currentfile = self.view.file_name()
        if not currentfile:
            print(NOT_SAVED)
            return

        is_mxs = _is_maxscriptfile(currentfile)
        is_python = _is_pythonfile(currentfile)

        regions = [region for region in self.view.sel()]
        for region in regions:
            line = self.view.line(region)
            text = self.view.substr(line)

            is_empty = region.empty()
            is_singleline = len(text.split("\n")) == 1
            is_multiline = not (is_empty or is_singleline)

            if is_multiline:
                self.expand(line)
                _save_to_tempfile(text)
                if not os.path.isfile(TEMPFILE):
                    print(NO_TEMP)
                    return

                if is_mxs:
                    cmd = get_mxs_tempfile_import()
                else:
                    cmd = get_python_tempfile_import()

                _send_cmd_to_max(cmd)
                return
            else:
                if is_empty:
                    self.expand(line)
                    text = self.view.substr(self.view.line(region))
                elif is_singleline:
                    text = self.view.substr(region)

                if is_mxs:
                    cmd = '{0}\r\n'.format(text)
                elif is_python:
                    _save_to_tempfile(text)
                    if not os.path.isfile(TEMPFILE):
                        print(NO_TEMP)
                        return
                    cmd = get_python_tempfile_import()

                _send_cmd_to_max(cmd)
                return


class OpenMaxHelpCommand(TextCommand):
    """Open the online MAXScript help searching for the current selection."""

    # Based on: https://forum.sublimetext.com/t/select-word-under-cursor-for-further-processing/10913  # noqa
    def run(self, edit):
        for region in self.view.sel():
            if region.begin() == region.end():
                word = self.view.word(region)
            else:
                word = region
            if not word.empty():
                keyword = self.view.substr(word)
                url = self.get_query_help_url(keyword)
                webbrowser.open(url, new=0, autoraise=True)

    def get_query_help_url(self, keyword):
        """Return a URL to the MAXScript help, looking for given keyword.

        The docs may need special handling regarding filtering and query
        parameters.

        Test URL for Max 2019:

        http://help.autodesk.com/view/3DSMAX/2019/ENU/index.html?query=polyOp&cg=Scripting%20%26%20Customization  # noqa
        """
        query_param = "?query=" + keyword
        max_version = _get_max_version()
        url = ONLINE_MAXSCRIPT_HELP_URL[max_version] + query_param
        if max_version == DEFAULT_DOCS_VERSION:
            # Make sure to search in a specific section of the docs.
            url += r"&cg=Scripting%20%26%20Customization"
        return url


class SelectMaxInstanceCommand(TextCommand):
    """Display a dialog of open 3ds Max instances to pick one.

    The chosen instance is used from then on to send commands to.
    """
    def run(self, edit):
        item2window = {}
        candidates = winapi.Window.find_windows(
            TITLE_IDENTIFIER)
        for window in candidates:
            text = window.get_text()
            normtext = text.replace("b'", "").replace("'", "")
            item = ("{txt} ({hwnd})".format(txt=normtext,
                                            hwnd=window.get_handle()))
            item2window[item] = window

        items = list(item2window.keys())

        def on_select(idx):
            if idx == -1:
                return

            global last_index
            last_index = idx

            item = items[idx]
            global mainwindow
            mainwindow = item2window[item]

            print(PREFIX + " Now connected to: \n\n" + item)

        def on_highlighted(idx):
            pass

        sublime.active_window().show_quick_panel(items,
                                                 on_select,
                                                 0,
                                                 last_index,
                                                 on_highlighted)

def plugin_unloaded():
    """Perform cleanup work."""
    if os.path.isfile(TEMPFILE):
        try:
            os.remove(TEMPFILE)
        except OSError:
            pass
