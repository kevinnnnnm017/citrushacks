from fpdf import FPDF
import webbrowser
import os


class PDF(FPDF):
    def header(self):
            # Logo
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(50, 10, 'Summarized Notes', 1, 0, 'C')
            # Line break
            self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def getPDF(strArr):
    u = u'hello\u2019world'
    # a = "\u13E0\u19E0\u1320\u2019"
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 14)
    # for i in strArr:
    #     i.encode()
        
    # strArr.set_character_set('utf8')
    for i in strArr:
        if i.find('\u2019') != -1:
            u.replace(u'\u2019', '').encode('latin-1')
        else:
            pdf.cell(0, 10, '-' + i, 0, 1)
    # pdf.output('Notes Summary.pdf', 'F')
    # pdf.output('Notes Summary.pdf', 'I')
    # pdf.output('I', 'Note Summary.pdf')
    # pdf.pdf_it("sampleee.txt")
    pdf.output('Summary Article Notes.pdf', 'F')

    return pdf

