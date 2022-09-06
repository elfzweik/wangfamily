'''Streamfields live in here.'''

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text = 'Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class CardBlock (blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text = 'Add your title')

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length= 40,)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required= False)),
                ("button_url", blocks.URLBlock(required=False, help_text="If button above is selected, that will be used first")),
            ]
        )    
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "edit"
        label ="staff card"

class FullRichTextBlock (blocks.RichTextBlock):

    class Meta:
        template = "streams/full_richtext.html"
        icon = "edit"
        label = "Richtext"