import weechat
import re

weechat.register("hyperlinks", "Avahe Kellenberger", "1.0", "GPL2",
        "Redisplays wrapped URLs as short hyperlinks", "", "UTF-8")

weechat.hook_signal("*,irc_in2_privmsg", "hyperlink_injector", "")

def hyperlink_injector(data, signal, signal_data):
    """
    Detects URLs provided in signal_data, and provides a short hyperlink
    in the same buffer after the message with the URL. 
   
    Parameters
    ----------
   @see https://weechat.org/files/doc/stable/weechat_scripting.en.html#irc_catch_messages

    signal: string
       The metadata of the message, as "xxx,irc_in|irc_in2_yyy"
       With xxx as the IRC internal server name,
       and yyy as the IRC command name (such as JOIN, QUIT, PRIVMSG, 301...)
    signal_data: string
       An IRC message, e.g. ":nick!user@host JOIN :#channel"
    """
    server = signal.split(",")[0]
    msg = weechat.info_get_hashtable("irc_message_parse",
            {"message": signal_data})
    buffer = weechat.info_get("irc_buffer", "%s,%s" % (server, msg["channel"]))
    if buffer:
        matches = find_urls(msg["text"])
        for match in matches:
            hyperlink = weechat.color("blue") + create_hyperlink("Link", match)
            print_hyperlink(buffer, hyperlink)
    return weechat.WEECHAT_RC_OK

def print_hyperlink(buffer, hyperlink):
    """Prints the hyperlink to the given buffer.

    Parameters
    ----------
    buffer: str
        The string representation of the buffer's pointer.
    hyperlink: str
        The hyperlink to print to the buffer.
    """
    weechat.prnt(buffer, hyperlink)

def create_hyperlink(text, url):
    """Creates a hyperlink from the given text and url.

    Parameters
    ----------
    text: str
        The text of the hyperlink to print.
    url: str
        The URL the hyperlink will navigate toward.

    Returns
    -------
    A textual representation of the hyperlink to be printed to the terminal.
    """
    return "\e]8;;" + url + "\e\\" + text + "\e8;;\e\\"

def find_urls(data):
    """Detects URLs in the given string.

    Parameters
    ----------
    data: string
        A string of text.

    Returns
    -------
    A set of URLs found in the string.
    """
    # Pattern from:
    # http://www.regexguru.com/2008/11/detecting-urls-in-a-block-of-text/
    p = re.compile("\\b(?:(?:https?|ftp|file)://|www\\.|ftp\\.)"
            + "(?:\\([-A-Z0-9+&@#/%=~_|$?!:,.]*\\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*"
            + "(?:\\([-A-Z0-9+&@#/%=~_|$?!:,.]*\\)|[A-Z0-9+&@#/%=~_|$])",
            re.IGNORECASE)
    return set(p.findall(data))
