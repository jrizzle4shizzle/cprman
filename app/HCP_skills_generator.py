# coding: utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_pdf(student_name="",test_date="",instructor_name=""):
  output_filename = student_name + "_skillsheet.pdf"

  #create page1 mask
  packet = StringIO.StringIO()
  # create a new PDF with Reportlab
  can = canvas.Canvas(packet, pagesize=(605.8, 785.86))
  #move origin up and to the left
  #can.translate(20,24)

  can.drawString(113, 665, student_name)
  can.drawString(450, 665, test_date)

  #check some boxes

  can.drawString(516, 550, u"✓")
  can.drawString(516, 533, u"✓")
  can.drawString(516, 515, u"✓")
  can.drawString(540, 483, u"✓")
  can.drawString(540, 457, u"<18")
  can.drawString(540, 435, u"✓")
  can.drawString(540, 416, u"✓")
  can.drawString(540, 397, u"✓")
  can.drawString(516, 349, u"✓")
  can.drawString(516, 330, u"✓")
  can.drawString(516, 314, u"✓")
  can.drawString(516, 296, u"✓")
  can.drawString(494, 239, u"✓")
  can.drawString(538, 239, u"✓")
  can.drawString(494, 219, u"✓")
  can.drawString(538, 219, u"✓")

  can.drawString(146, 71, instructor_name)
  can.drawString(84, 55, test_date)

  #next page!
  can.showPage()
  #move origin up and to the left
  #can.translate(20,24)



  can.save()

  #move to the beginning of the StringIO buffer
  packet.seek(0)
  mask = PdfFileReader(packet)

  #open up template
  output = PdfFileWriter()
  dir = os.path.realpath('.')
  filename = os.path.join(dir, 'templates','HCP_adult_skills.pdf')
  skills_template = PdfFileReader(file(filename, "rb"))

  #merge template with mask

  page = skills_template.getPage(0)
  page.mergePage(mask.getPage(0))
  output.addPage(page)
#  page2 = skills_template.getPage(1)
#  page2.mergePage(mask.getPage(1))
#  output.addPage(page2)


  #write combined pdf to file

  outputStream = file(output_filename, "wb")
  output.write(outputStream)
  outputStream.close()


def main():
    generate_pdf("John Student", "5/15/15", "Jane Instructor")

if __name__ == "__main__":
    main()
