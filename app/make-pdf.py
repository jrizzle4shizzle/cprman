# coding: utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_skills_sheet(student_name="",test_date="",instructor_name="", adult=True, child=True, infant=True):
  output_filename = student_name + "_skillsheet.pdf"

  #create page1 mask
  packet = StringIO.StringIO()
  # create a new PDF with Reportlab
  can = canvas.Canvas(packet, pagesize=(605.8, 785.86))
  #move origin up and to the left
  can.translate(20,24)

  can.drawString(368, 682, student_name)
  can.drawString(346, 657, test_date)

  #check some boxes

  if adult:
    can.drawString(410, 577, u"✓")
    can.drawString(410, 555, u"✓")
    can.drawString(410, 535, u"✓")
    can.drawString(410, 508, u"✓")
    can.drawString(410, 475, u"✓")
    can.drawString(410, 450, u"✓")
    can.drawString(410, 408, u"✓")
    can.drawString(410, 360, u"✓")
    can.drawString(410, 304, u"✓")
    can.drawString(410, 250, u"✓")
    can.drawString(410, 156, u"✓")
    can.drawString(410, 85, u"✓")


  if child:
    can.drawString(514, 577, u"✓")
    can.drawString(514, 555, u"✓")
    can.drawString(514, 535, u"✓")
    can.drawString(514, 475, u"✓")
    can.drawString(514, 450, u"✓")
    can.drawString(514, 408, u"✓")
    can.drawString(514, 360, u"✓")
    can.drawString(514, 304, u"✓")
    can.drawString(514, 250, u"✓")
    can.drawString(514, 195, u"✓")
    can.drawString(514, 156, u"✓")
    can.drawString(514, 85, u"✓")

  #next page!
  can.showPage()
  #move origin up and to the left
  can.translate(20,24)

  can.drawString(356, 682, student_name)
  can.drawString(335, 657, test_date)
  can.drawString(360, 102, instructor_name)
  can.drawString(290, 86, test_date)

  if infant:
    can.drawString(500, 581, u"✓")
    can.drawString(500, 558, u"✓")
    can.drawString(500, 537, u"✓")
    can.drawString(500, 581, u"✓")
    can.drawString(500, 507, u"✓")
    can.drawString(500, 478, u"✓")
    can.drawString(500, 447, u"✓")
    can.drawString(500, 417, u"✓")
    can.drawString(500, 380, u"✓")
    can.drawString(500, 343, u"✓")
    can.drawString(500, 304, u"✓")
    can.drawString(500, 246, u"✓")

  can.save()

  #move to the beginning of the StringIO buffer
  packet.seek(0)
  mask = PdfFileReader(packet)

  #open up template
  output = PdfFileWriter()
  dir = os.path.realpath('.')
  filename = os.path.join(dir, 'templates','HS_CPR_skills.pdf')
  skills_template = PdfFileReader(file(filename, "rb"))

  #merge template with mask

  page = skills_template.getPage(0)
  page.mergePage(mask.getPage(0))
  output.addPage(page)
  page2 = skills_template.getPage(1)
  page2.mergePage(mask.getPage(1))
  output.addPage(page2)


  #write combined pdf to file

  outputStream = file(output_filename, "wb")
  output.write(outputStream)
  outputStream.close()


def main():
    generate_skills_sheet("John Student", "5/15/15", "Jane Instructor", adult=True, child=True, infant=True)

if __name__ == "__main__":
    main()
