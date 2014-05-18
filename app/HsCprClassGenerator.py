# coding: utf-8
import os
import csv

def generate_class_paperwork(course_info, students):
    '''
    Takes two dicts as arguments, with the following keys:
    course_info: Instructor Name,Instructor ID,Training Center Name,
        Training Center Address,Course Location,Course Date,Card Issue Date,
        Card Expire Date,Written Test?,Child CPR?,Infant CPR?
    students: student_name,student_address_1,student_address_2

    returns a list of PDFs
    '''

    skillsheets = []
    print_cards = []
    archive_cards = []

    #first, create the skill sheets for each student

    #next, create the cards for printing and archiving

    #merge the pdfs

    #return the list of combined pdfs



def main():
    dir = os.path.realpath('.')
    filename = os.path.join(dir, 'test','students.csv')
    students = {}
    with open(filename, 'rb') as csvfile:
        students = csv.DictReader(csvfile)
        for row in students:
            print row

    course_info = {}
    course_info_filename = os.path.join(dir, 'test', 'HS_CPR_course_info.csv')
    with open (course_info_filename, 'rb') as course_info_csv:
        course_info = csv.DictReader(course_info_csv)
        for row in course_info:
            print row

    pdf_list = generate_class_paperwork(course_info, students)

if __name__ == "__main__":
    main()
