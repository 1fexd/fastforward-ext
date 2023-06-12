__WILDCARD_START = "*://*."
__REGEX_HTTP_SCHEME = "https?:\\/\\/"
__REGEX_WILDCARD_START = f"{__REGEX_HTTP_SCHEME}.*"


def host_to_regex(host):
    return f"{__REGEX_HTTP_SCHEME}{host}\\/.*"


def wildcard_to_regex(wildcard):
    start = ""
    if wildcard.startswith(__WILDCARD_START):
        start = __REGEX_WILDCARD_START
        wildcard = wildcard[len(__WILDCARD_START):]

    wildcard = start + wildcard.replace(".", "\\.").replace("/", "\\/").replace("*", ".*").replace("?", "\\?")

    return wildcard
