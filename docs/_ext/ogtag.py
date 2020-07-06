"""Automatically generates Open Graph tags for Sphinx html docs.
Based on https://sphinx-users.jp/cookbook/ogp/index.html
"""

from docutils import nodes
from sphinx import addnodes
from urllib.parse import urljoin


class Visitor:
    def __init__(self, document):
        self.document = document
        self.text_list = []
        self.images = []
        self.n_sections = 0

    def dispatch_visit(self, node):
        # Skip toctree
        if isinstance(node, addnodes.compact_paragraph) and node.get("toctree"):
            raise nodes.SkipChildren

        # Collect images
        if isinstance(node, nodes.image):
            self.images.append(node)

        # Collect text (first three sections)
        if self.n_sections < 3:

            # Collect paragraphs
            if isinstance(node, nodes.paragraph):
                self.text_list.append(node.astext().replace("\n", " "))

            # Include only paragraphs
            if isinstance(node, nodes.section):
                self.n_sections += 1

    def dispatch_departure(self, node):
        pass

    def get_og_description(self):
        # TODO: Find optimal length for description text
        text = " ".join(self.text_list)
        if len(text) > 200:
            text = text[:197] + "..."
        return text

    def get_og_image_url(self, page_url):
        # TODO: Check if picking first image makes sense
        # TODO: Return fallback image if no image found on page
        if self.images:
            return urljoin(page_url, self.images[0]["uri"])
        else:
            return None


def get_og_tags(context, doctree, config):
    # page_url
    site_url = config.og_site_url
    page_url = urljoin(site_url, context["pagename"] + context["file_suffix"])

    # collection
    visitor = Visitor(doctree)
    doctree.walkabout(visitor)

    # og:description
    og_desc = visitor.get_og_description()

    # og:image
    og_image = visitor.get_og_image_url(page_url)

    # OGP
    tags = """
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:site" content="{cfg[og_twitter_site]}" />
    <meta property="og:site_name" content="{ctx[shorttitle]}">
    <meta property="og:title" content="{ctx[title]}">
    <meta property="og:description" content="{desc}">
    <meta property='og:url' content="{page_url}">
    """.format(
        ctx=context, desc=og_desc, page_url=page_url, cfg=config
    )
    # Add image if present, use default image if no image is found
    if og_image:
        tags += f'<meta property="og:image" content="{og_image}">'
    elif config.og_fallback_image:
        tags += f'<meta property="og:image" content="{config.og_fallback_image}">'
    return tags


def html_page_context(app, pagename, templatename, context, doctree):
    if not doctree:
        return

    context["metatags"] += get_og_tags(context, doctree, app.config)


def setup(app):
    app.add_config_value("og_site_url", None, "html")
    app.add_config_value("og_twitter_site", None, "html")
    app.add_config_value("og_fallback_image", None, "html")
    app.connect("html-page-context", html_page_context)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
