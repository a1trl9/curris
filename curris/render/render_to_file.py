""" util function
render content to the path
"""

def render_to_file(content, path):
    """ render entry
    """
    with open(path, 'w') as writer:
        writer.write(content)
