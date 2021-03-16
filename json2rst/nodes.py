from enum import Enum
import utils

class Nodes(Enum):
    """Enum type for rst nodes"""
    TABLE_INIT = '..  list-table::' #: Start of rst list-table node.
    ATTR_HEADERROWS = '    :header-rows: 1' #: Node for the list-table attribute ``:header-rows: 1``. Always set to ``1``.
    ATTR_STUBCOLS   = '    :stub-columns: 1' #: Node for the list-table attribute ``:stub-columns: 1``. Always set to ``1``.
    STUB_ITEM  = '    - * ' #: Node for first item in a table row.
    ITEM        = '      * ' #: Node for item in a table row.
    LEFTPAD     = '        '
    """Pads 6 \s characters. Used to pad content in tables so that
they match the indentation of their parent table nodes.
Works only if the root table is at col 0
(told ya this is an inelegant repo)."""
    UL_ITEM = '- '
    OL_ITEM = '#.  '
    # CODE #: Omit. Because we need to surround the content of
    # <code> nodes with double backticks, as opposed to prefixing
    # the node (like with the other Nodes here)
    CODE_BLOCK_INIT = '..  code-block::'
    CODE_BLOCK_PAD = '    '
    IMAGE = '..  image:: '

class RichNode:
    RICH_NODE_TYPES = [
        "h1",
        "h2",
        "h3",
        "p",
        "ul",
        "ol",
        "code",
        "code-block",
        "image",
    ]

    def __init__(self, node_type: str, content: str, first: bool) -> None:
        """
        Args:
            node_type (str): One of RICH_NODE_TYPES.
            content (str): Content of node.
            first (bool): Whether this node is the first 
        """
        self.content = content
        self.n = node_type
        self.first = first
        
        self._is_rich_node()

    def parse(self) -> str:
        return f"{self._handle_node()}\n\n"

    def _is_rich_node(self) -> bool:
        if self.n not in self.RICH_NODE_TYPES:
            print(f"Invalid node type: {node_type}: {content}.\n" \
                  "JSON key should be one of {self.RICH_NODE_TYPES}")
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
        """If this is the first node in a rich content block, don't add LEFTPAD output"""

        if self.n == "h1":
            H1_rst = "*" * (len(self.content) + 2) # Make sure that heading marker is slightly longer than len(self.content)
            return f"{LEFTPAD}{self.content}\n{Nodes.LEFTPAD.value}{H1_rst}"

        elif self.n == "h2":
            H2_rst = "=" * (len(self.content) + 2) # Make sure that heading marker is slightly longer than len(self.content)
            return f"{LEFTPAD}{self.content}\n{Nodes.LEFTPAD.value}{H2_rst}"

        elif self.n == "h2":
            H3_rst = "-" * (len(self.content) + 2) # Make sure that heading marker is slightly longer than len(self.content)
            return f"{LEFTPAD}{self.content}\n{Nodes.LEFTPAD.value}{H3_rst}"

        elif self.n == "p":
            return f"{LEFTPAD}{utils.handle_newlines(self.content)}"

        elif self.n == "ul":
            return f"{LEFTPAD}{Nodes.UL_ITEM.value}{self.content}"

        elif self.n == "ol":
            return f"{LEFTPAD}{Nodes.OL_ITEM.value}{self.content}"

        elif self.n == "code":
            return f"{LEFTPAD}``{self.content}``"

        elif self.n == "code-block":
            # this needs more complex handling. Need to know if there are multiple code-block-items in sequence.
            pass

        elif self.n == "image":
            # might need to embed as base64 image.
            return f"{LEFTPAD}{Nodes.IMAGE.value}{content}"

    def _code_block_start() -> str:
        """remember to add {LEFTPAD} with the calling function"""
        return f"{Nodes.CODE_BLOCK_INIT.value}\n\n"

    def _code_block_body() -> str:
        """remember to add {LEFTPAD} with the calling function"""
        return f"{Nodes.CODE_BLOCK_PAD.value}{self.content}"
