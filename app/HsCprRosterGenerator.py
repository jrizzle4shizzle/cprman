# coding: utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import itertools

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def generate_pdf(course_info, students):
    '''
    Arguments:
    course_info: Dictionary with the following keys
        instructor_name,instructor_id,training_center_name, training_center_id,
        training_center_address,course_location,course_date,card_issue_date,
        card_expire_date,written_test,child_cpr,infant_cpr
    students: List of dictionarys with the following keys
        student_name,student_address_1,student_address_2
    '''


def main():

    course_info = {}
    students = []

    pdf = generate_pdf(course_info, students)

    #write pdf to file
    dir = os.path.realpath('.')
    filename = os.path.join(dir, 'test','test_HS_cards.pdf')
    outputStream = file(filename, "wb")
    merged_cards.write(outputStream)
    outputStream.close()

if __name__ == "__main__":
    main()
