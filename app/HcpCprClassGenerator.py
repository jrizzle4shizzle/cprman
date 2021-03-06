# coding: utf-8
import sys, getopt
import os
import csv
import HsCprCardGenerator
import HcpSkillsGenerator
import HcpCprRosterGenerator
import itertools
import StringIO
from PyPDF2 import PdfFileMerger, PdfFileReader


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def generate_class_paperwork(course_info, students):
    '''
    Arguments:
    course_info: Dictionary with the following keys
        instructor_name,instructor_id,training_center_name,training_center_id,
        training_center_address,course_location,course_date,card_issue_date,
        card_expire_date,written_test,child_cpr,infant_cpr
    students: List of dictionarys with the following keys
        student_name,student_address_1,student_address_2

    returns a list of PdfFileWriters
    '''

    skillsheets = []
    print_cards = []
    archive_cards = []

    child_cpr = (course_info["child_cpr"] == "yes")
    infant_cpr = (course_info["infant_cpr"] == "yes")
    written_test = (course_info["written_test"] == "yes")

    print "generating skillsheets..."

    #first, create the skill sheets for each student
    for row in students:
        if(row["student_name"] != ''):
            next_skillsheet = HcpCprSkillsGenerator.generate_pdf(row["student_name"],
                course_info["course_date"], course_info["instructor_name"],
                adult=True, child=child_cpr, infant=infant_cpr)
            ss_packet = StringIO.StringIO()
            next_skillsheet.write(ss_packet)
            skillsheets.append(ss_packet)

    print "generating cards..."
    #next, create the cards for printing and archiving
    for student1, student2 in grouper(students, 2):
        if(student2 != None):
            next_card_mask = HsCprCardGenerator.generate_pdf(
                tc_name=course_info["training_center_name"]+" "+course_info["training_center_id"],
                tc_address=course_info["training_center_address"],
                course_location=course_info["course_location"],
                instructor_name_id=course_info["instructor_name"]+" "+course_info["instructor_id"],
                issue_date=course_info["card_issue_date"],
                expire_date=course_info["card_expire_date"],
                test=written_test, child=child_cpr, infant=infant_cpr,
                student1_name=student1["student_name"],
                student1_address_1=student1["student_address_1"],
                student1_address_2=student1["student_address_2"],
                student2_name=student2["student_name"],
                student2_address_1=student2["student_address_1"],
                student2_address_2=student2["student_address_2"])
        else:
            next_card_mask = HsCprCardGenerator.generate_pdf(
                tc_name=course_info["training_center_name"],
                tc_address=course_info["training_center_address"],
                course_location=course_info["course_location"],
                instructor_name_id=course_info["instructor_name"]+" "+course_info["instructor_id"],
                issue_date=course_info["card_issue_date"],
                expire_date=course_info["card_expire_date"],
                test=written_test, child=child_cpr, infant=infant_cpr,
                student1_name=student1["student_name"],
                student1_address_1=student1["student_address_1"],
                student1_address_2=student1["student_address_2"])

        print_card = HcpCprCardGenerator.generate_cards_with_no_background(next_card_mask)
        archive_card = HcpCprCardGenerator.generate_cards_with_background(next_card_mask)

        #save the PDFs off as strings that we can merge later
        pc_packet = StringIO.StringIO()
        ac_packet = StringIO.StringIO()
        print_card.write(pc_packet)
        archive_card.write(ac_packet)

        print_cards.append(pc_packet)
        archive_cards.append(ac_packet)

    print "generating roster"

    roster = HcpCprRosterGenerator.generate_pdf(course_info, students)

    print "combining output..."

    #merge the pdfs
    combined_pdfs = {}

    combined_pdfs['roster'] = roster

    merged_skillsheets = PdfFileMerger()
    for next_skillsheet in skillsheets:
        next_skillsheet.seek(0)
        merged_skillsheets.append(PdfFileReader(next_skillsheet))

    combined_pdfs['skillsheets'] = merged_skillsheets

    merged_print_cards = PdfFileMerger()
    for next_print_card in print_cards:
        next_print_card.seek(0)
        merged_print_cards.append(PdfFileReader(next_print_card))

    combined_pdfs['print_cards'] = merged_print_cards

    merged_archive_cards = PdfFileMerger()
    for next_archive_card in archive_cards:
        next_archive_card.seek(0)
        merged_archive_cards.append(PdfFileReader(next_archive_card))

    combined_pdfs['archive_cards'] = merged_archive_cards

    #return the list of combined pdfs
    return combined_pdfs



def main(argv):
    info_file = ''
    students_file = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:",["ifile=","sfile="])
    except getopt.GetoptError:
        print 'HsCprClassGenerator.py -i <course_info.csv> -s <students.csv>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'HsCprClassGenerator.py -i <course_info.csv> -s <students.csv>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            info_file = arg
        elif opt in ("-s", "--sfile"):
            students_file = arg

    test = False

    dir = os.path.realpath('.')
    if(students_file == ''):
        print "No student file name provided ... entering test mode"
        test = True
        students_file = os.path.join(dir, 'test','students.csv')

    students = []
    with open(students_file, 'rb') as csvfile:
        students_csv = csv.DictReader(csvfile)
        for row in students_csv:
            if(row["student_name"] != ''):
                students.append(row)

    if(info_file == ''):
        print "No course info file provided ... entering test mode"
        test = True
        info_file = os.path.join(dir, 'test', 'HS_CPR_course_info.csv')

    course_info = {}
    with open (info_file, 'rb') as course_info_csv:
        course_info_csv = csv.DictReader(course_info_csv)
        for row in course_info_csv:
            course_info = row


    #pdf_dict = generate_class_paperwork(course_info, students)

    roster = HcpCprRosterGenerator.generate_pdf(course_info, students)

    cd = course_info['course_date'].replace('/','_')

    if test:
        cd = "TEST"

    #ss_filename = os.path.join(dir, 'output',cd+'_HS_skillsheets.pdf')
    #ss_outputStream = file(ss_filename, "wb")
    #pdf_dict['skillsheets'].write(ss_outputStream)
    #ss_outputStream.close()

    #pc_filename = os.path.join(dir, 'output',cd+'_HS_cards_print.pdf')
    #pc_outputStream = file(pc_filename, "wb")
    #pdf_dict['print_cards'].write(pc_outputStream)
    #pc_outputStream.close()

    #ac_filename = os.path.join(dir, 'output',cd+'_HS_cards_archive.pdf')
    #ac_outputStream = file(ac_filename, "wb")
    #pdf_dict['archive_cards'].write(ac_outputStream)
    #ac_outputStream.close()

    r_filename = os.path.join(dir, 'output',cd+'_HCP_roster.pdf')
    r_outputStream = file(r_filename, "wb")
    #pdf_dict['roster'].write(r_outputStream)
    roster.write(r_outputStream)
    r_outputStream.close()


if __name__ == "__main__":
    main(sys.argv[1:])
