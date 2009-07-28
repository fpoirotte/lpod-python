# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Itaapy, ArsAperta, Pierlis, Talend

# Import from lpod
from lpod.document import odf_new_document_from_type
from lpod.document import odf_create_paragraph, odf_create_heading
from lpod.document import odf_create_style, odf_create_style_text_properties
from lpod.document import odf_create_list, odf_create_list_item
from lpod.document import odf_create_note, odf_create_annotation
from lpod.styles import rgb2hex


# Creation of the document
document = odf_new_document_from_type('text')

# Get the elements
body = document.get_body()
styles = document.get_xmlpart('styles')
named_styles = styles.get_category_context('named')


# A paragraph with a style
heading = odf_create_heading(1, text=u'A paragraph with a style')
body.append_element(heading)

style = odf_create_style('style1', 'paragraph')
style.set_attribute('style:parent-style-name', 'Standard')
properties = odf_create_style_text_properties()
properties.set_attribute('fo:color', rgb2hex('blue'))
properties.set_attribute('fo:background-color', rgb2hex('red'))
style.append_element(properties)
named_styles.append_element(style)

text =  u'This document has been generated by the lpOD.'
paragraph = odf_create_paragraph('style1', text)
body.append_element(paragraph)


# A list
heading = odf_create_heading(1, text=u'A list')
body.append_element(heading)

my_list = odf_create_list('Standard')
for i in range(1, 4):
    item = odf_create_list_item(u'item <%d>' % i)
    my_list.append_element(item)
body.append_element(my_list)


# Footnote, endnote, annotations
heading = odf_create_heading(1, text=u'Footnotes, end notes, annotations')
body.append_element(heading)

text1 = u'A paragraph with a footnote.'
text2 = u'A paragraph with an end note.'
text3 = u'A paragraph with an annotation.'

offset = len(u'A paragraph')

footnote = odf_create_note(u'1 ', id='note1', body=u'A footnote')
paragraph = odf_create_paragraph('Standard', text1)
paragraph.wrap_text(footnote, offset=offset)
body.append_element(paragraph)

endnote = odf_create_note(u'i ', note_class='endnote', id='note1',
                          body=u'An end note')
paragraph = odf_create_paragraph('Standard', text2)
paragraph.wrap_text(endnote, offset=offset)
body.append_element(paragraph)

annotation = odf_create_annotation(u'Anonymous', u'An annotation')
paragraph = odf_create_paragraph('Standard', text3)
paragraph.wrap_text(annotation, offset=offset)
body.append_element(paragraph)


# Save
document.save('basic-text.odt', pretty=True)


