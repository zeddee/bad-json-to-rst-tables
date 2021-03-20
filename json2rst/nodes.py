import base64
from pathlib import Path
from enum import Enum

from . import utils

class Nodes(Enum):
    """Enum type for rst nodes"""
    TABLE_INIT = '..  list-table::\n' #: Start of rst list-table node.
    ATTR_HEADERROWS = '    :header-rows: 1\n' #: Node for the list-table attribute ``:header-rows: 1``. Always set to ``1``.
    ATTR_STUBCOLS   = '    :stub-columns: 1\n' #: Node for the list-table attribute ``:stub-columns: 1``. Always set to ``1``.
    STUB_ITEM  = '    - * ' #: Node for first item in a table row.
    ITEM        = '      * ' #: Node for item in a table row.
    LEFTPAD     = r'        '
    """Pads 8 ``\\s`` characters. Used to pad content in tables so that
they match the indentation of their parent table nodes.
Works only if the root table is at col 0
(told ya this is an inelegant repo)."""
    UL_ITEM = '- '
    OL_ITEM = '#.  '
    # CODE #: Omit. Because we need to surround the content of
    # <code> nodes with double backticks, as opposed to prefixing
    # the node (like with the other Nodes here)
    CODE_BLOCK_INIT = '..  code-block::\n'
    CODE_BLOCK_PAD = '    '
    IMAGE = '..  image:: '

class RichNode:
    RICH_NODE_TYPES = [
        "heading",
        "p",
        "ul",
        "ol",
        "code",
        "code-block",
        "image",
    ]

    def __init__(self,
        srcfile: str,
        node_type: str,
        content: str,
        first: bool,
        prev_node_type: str,
        next_node_type: str,
        ) -> None:
        """
        Args:
            node_type (str): One of RICH_NODE_TYPES.
            content (str): Content of node.
            first (bool): Whether this node is the first 
        """
        self.content = content
        self.n = node_type
        self.first = first
        self.srcfile = srcfile
        self.prev = prev_node_type
        self.next = next_node_type
        
        self._is_rich_node()

    def parse(self) -> str:
        return self._handle_node()

    def _is_rich_node(self) -> bool:
        if self.n not in self.RICH_NODE_TYPES:
            print(f"Invalid node type: [{self.srcfile}]: {self.n}\n" \
                  f"JSON key should be one of {self.RICH_NODE_TYPES}")
            exit(1) # TODO: exception handling.
            # return False

        return True

    def _handle_node(self) -> str:
        """
        Would *really* love to have Python 3.10 pattern matching
        syntax here right now :(

        Args:
            n (str): Node type. Must be one of self.RICH_NODE_TYPES.
        Returns:
            An rST-formatted string ready to plug into our output file.
        """

        LEFTPAD = "" if self.first else Nodes.LEFTPAD.value
        #: If this is the first node in a rich content block, don't add LEFTPAD output

        LINE_END = "\n\n"


        if self.n == "heading":
            return "{}**{}**{}".format(
                LEFTPAD,
                self.content,
                LINE_END,
            )

        elif self.n == "p":
            return "{}{}{}".format(
                LEFTPAD,
                utils.handle_newlines(self.content),
                LINE_END,
            )

        elif self.n == "ul":
            return "{}{}{}{}".format(
                LEFTPAD,
                Nodes.UL_ITEM.value,
                self.content,
                LINE_END,
            )

        elif self.n == "ol":
            return "{}{}{}{}".format(
                LEFTPAD,
                Nodes.OL_ITEM.value,
                self.content,
                LINE_END,
            )

        elif self.n == "code":
            return "{}``{}``{}".format(
                LEFTPAD,
                self.content,
                LINE_END,
            )

        elif self.n == "code-block":
            code_out = ""
            
            if self.prev != "code-block":
                code_out = f"{LEFTPAD}{Nodes.CODE_BLOCK_INIT.value}\n"
            
            code_out = code_out + "{}{}{}".format(
                LEFTPAD,
                Nodes.CODE_BLOCK_PAD.value,
                self.content,
            )

            if self.next == "code-block":
                code_out = code_out + "\n"
            else:
                code_out = code_out + LINE_END

            return code_out
            

        elif self.n == "image":
            # might need to embed as base64 image.
            resource_path = Path(self.srcfile).parent
            if self.content.startswith("./") or self.content.startswith("../"): # if image path is a relative path
                img_path = resource_path.joinpath(Path(self.content)) # just join 
            else:
                img_path = Path(self.content).resolve().absolute()
            img_exts = [".jpg",".png"] #: keep supported image types

            if not img_path.is_file():
                print(f"{img_path} must be an image file. Paths are resolved from directory you're running json2rst in.")
                exit(1)

            if img_path.suffix not in img_exts:
                print(f"{img_path} must have one of these file extensions: {img_exts}")
                exit(1)

            return f"{LEFTPAD}{Nodes.IMAGE.value}data:image/{img_path.suffix.strip('.')};base64,{self._encode_image(img_path)}\n\n"

    def _encode_image(self, file: str) -> str:
        with open(file, "rb") as f:
            img = base64.b64encode(f.read())

        return str(img).strip("b").strip("'")

