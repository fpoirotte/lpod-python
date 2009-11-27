# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Itaapy, ArsAperta, Pierlis, Talend

# Import from the Standard Library
from datetime import date, time, timedelta
from sys import version_info

# Import from itools
from itools import vfs
from itools.handlers import get_handler


# Import from lpod
from lpod.document import odf_new_document_from_type
from lpod.paragraph import odf_create_paragraph
from lpod.heading import odf_create_heading
from lpod.frame import odf_create_frame
from lpod.image import odf_create_image
from lpod.style import odf_create_style
from lpod.variable import odf_create_variable_decl
from lpod.variable import odf_create_variable_set, odf_create_variable_get
from lpod.variable import odf_create_user_field_decl
from lpod.variable import odf_create_user_field_get
from lpod.variable import odf_create_page_number_variable
from lpod.variable import odf_create_page_count_variable
from lpod.variable import odf_create_date_variable, odf_create_time_variable
from lpod.variable import odf_create_chapter_variable
from lpod.variable import odf_create_filename_variable
from lpod.table import odf_create_table
from lpod.styles import rgb2hex
from lpod import __version__, __installation_path__


# Hello messages
print 'lpod installation test'
print ' Version           : %s' %  __version__
print ' Installation path : %s' % __installation_path__
print
print 'Generating test_output/use_case2.odt ...'

# Go
document = odf_new_document_from_type('text')
body = document.get_body()

# 1- The image
# ------------
image_file = get_handler('samples/image.png')
width, height = image_file.get_size()
paragraph = odf_create_paragraph(style=u"Standard")
# 72 ppp
frame = odf_create_frame('frame1', 'Graphics',
                         str(width / 72.0) + 'in',
                         str(height / 72.0) + 'in')
internal_name = 'Pictures/image.png'
image = odf_create_image(internal_name)
frame.append_element(image)
paragraph.append_element(frame)
body.append_element(paragraph)

# And store the data
container = document.container
container.set_part(internal_name, image_file.to_str())


# 2- Congratulations (=> style on paragraph)
# ------------------------------------------
heading = odf_create_heading(1, text=u'Congratulations !')
body.append_element(heading)

# The style
style = odf_create_style('paragraph', u"style1", parent=u"Standard",
        area='text', color=rgb2hex('blue'), background_color=rgb2hex('red'))
document.insert_style(style)

# The paragraph
text =  u'This document has been generated by the lpOD installation test.'
paragraph = odf_create_paragraph(text, style=u"style1")
body.append_element(paragraph)


# 3- Your environment (=> a table)
# --------------------------------
heading = odf_create_heading(1, text=u'Your environment')
body.append_element(heading)

data = []

# lpOD Version
data.append([u'lpOD library version', __version__])

# Python version
data.append([u'Python version', '%d.%d.%d' % version_info[:3]])

# Creation / Insertion
table = odf_create_table(u'table1', width=2, height=2, style=u"Standard")
table.set_table_values(data)
body.append_element(table)


# 4- Description (=> footnote & => highlight)
# -------------------------------------------

heading = odf_create_heading(1, text=u'Description')
body.append_element(heading)

# A paragraph with a note
text = u'The lpOD project is made to generate easily OpenDocuments.'
paragraph = odf_create_paragraph(text, style=u"Standard")
paragraph.insert_note(after=u"lpOD project", note_id='note1',
    citation=u'1', body=u'http://lpod-project.org/')
body.append_element(paragraph)

# A paragraph with a highlighted word

# The style
style = odf_create_style('text', u"style2", parent=u"Standard", area='text',
        background_color=rgb2hex('yellow'))
document.insert_style(style)

# The paragraph
text = (u'The office document file format OpenDocument Format (ODF) '
        u'is an ISO standard ISO 26300 used by many applications.')
paragraph = odf_create_paragraph(text, u"Standard")
paragraph.set_span(u"style2", regex=u"ISO standard")
body.append_element(paragraph)


# 6- A variable
# -------------

# A variable "spam" with the value 42
variable_set = odf_create_variable_set('spam', 42)
value_type = variable_set.get_attribute('office:value-type')
variable_decl = odf_create_variable_decl('spam', value_type)

# Insert
heading = odf_create_heading(1, text=u'A variable')
body.append_element(heading)

decl = body.get_variable_decls()
decl.append_element(variable_decl)

text = u'Set of spam.'
paragraph = odf_create_paragraph(text, style=u"Standard")
body.append_element(paragraph)
paragraph._insert_between(variable_set, u"Set", u"spam.")

text = u'The value of spam is: '
value = body.get_variable_value('spam')
variable_get = odf_create_variable_get('spam', value)
paragraph = odf_create_paragraph(text, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(variable_get, u"is: ")


# 7- An user field
# ----------------

# An user field "pi5" with the value 3.14159
user_field_decl = odf_create_user_field_decl('pi5', value=3.14159)

# Insert
heading = odf_create_heading(1, text=u'An user field')
body.append_element(heading)

decl = body.get_user_field_decls()
decl.append_element(user_field_decl)

text = u'The value of pi5 is: '
value = body.get_user_field_value('pi5')
user_field_get = odf_create_user_field_get('pi5', value)
paragraph = odf_create_paragraph(text, style=u"Standard")
body.append_element(paragraph)
paragraph._insert_between(user_field_get, u"The", u"is: ")


# 8- Page number
# --------------

heading = odf_create_heading(1, text=u'Page number')
body.append_element(heading)

text1 = u'The current page is: '
text2 = u'The previous page is: '
text3 = u'The next page is: '
text4 = u'The total page number is: '

paragraph = odf_create_paragraph(text1, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_page_number_variable(), u"is: ")

paragraph = odf_create_paragraph(text2, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_page_number_variable(select_page='previous'),
        u"is: ")

paragraph = odf_create_paragraph(text3, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_page_number_variable(select_page='next'),
        u"is: ")

paragraph = odf_create_paragraph(text4, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_page_count_variable(), u"is: ")


# 9- Date
# -------

heading = odf_create_heading(1, text=u'Date insertion')
body.append_element(heading)

text1 = u'A fixed date: '
text2 = u'Today: '

paragraph = odf_create_paragraph(text1, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_date_variable(date(2009, 7, 20),
    fixed=True), u"date: ")

paragraph = odf_create_paragraph(text2, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_date_variable(date(2009, 7, 20)),
    u"Today: ")


# 10- Time
# --------

heading = odf_create_heading(1, text=u'Time insertion')
body.append_element(heading)

text1 = u'A fixed time: '
text2 = u'Now: '
text3 = u'In 1 hour: '

paragraph = odf_create_paragraph(text1, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_time_variable(time(19, 30), fixed=True),
        u"time: ")

paragraph = odf_create_paragraph(text2, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_time_variable(time(19, 30)), u"Now: ")

paragraph = odf_create_paragraph(text3, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_time_variable(time(19, 30),
    time_adjust=timedelta(hours=1)), u"hour: ")


# 11- Chapter
# -----------

heading = odf_create_heading(1, text=u'Chapter')
body.append_element(heading)

text = u'The current chapter is: '

paragraph = odf_create_paragraph(text, style=u"Standard")
body.append_element(paragraph)
paragraph.insert_variable(odf_create_chapter_variable(display='number-and-name'),
        u"is: ")


# 11- Filename
# ------------

heading = odf_create_heading(1, text=u'Filename')
body.append_element(heading)

text = u'The current file name is: '

paragraph = odf_create_paragraph(text, style=u"Standard")
body.append_element(paragraph)
paragraph._insert_between(odf_create_filename_variable(), u"The", u"is: ")




# Save
# ----

vfs.make_folder('test_output')
document.save('test_output/use_case2.odt', pretty=True)


