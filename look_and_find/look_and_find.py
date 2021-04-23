import argparse
import os
import random
from fpdf import FPDF
from typing import List, Tuple

Question = List[Tuple[str, int]]


class LookAndFindWorksheet:

    def __init__(self):
        self.question_count, self.output_filename = self.parse()
        self.question_title = 'Count the objects and tell whether there is an odd or even number of objects'
        self.image_range = (8, 25) # (8, 25) minimum 8 objects and maximum 25 objects of a specific image will be randomly generated
        self.maximum_objects_per_question = 18 * 12
        self.pngs = ['..\\assets\\png\\{}'.format(f) for f in os.listdir('..\\assets\\png') if f.endswith('.png')]
        self.pdf = FPDF()

    def parse(self):
        """
        Parse input arguments
        :return: input arguments
        """
        parser = argparse.ArgumentParser(description='Generate Look and Find Exercise Worksheet')
        parser.add_argument('-n', '--question_count', type=int, default='15', help='total number of questions (default: 15)')
        parser.add_argument('-o', '--output_filename', default='sample.pdf', help='Output file name (default: sample.pdf)')
        args = parser.parse_args()
        return args.question_count, args.output_filename

    def generate(self):
        """
        Generate the worksheet PDF
        """
        self.pdf.set_font('Arial', size=10)
        questions = self.generate_questions(self.question_count)
        self.render_question_pages(questions)
        self.render_answer_pages(questions)
        self.pdf.output(self.output_filename)

    def generate_question(self) -> Question:
        """
        Generate a question with answer, randomly selected 12 pngs from the pool
        :return: list of images and their count
        """
        random.shuffle(self.pngs)
        return [(png, random.randint(self.image_range[0], self.image_range[1])) for png in self.pngs[:12]]

    def generate_questions(self, question_count: int) -> List[Question]:
        """
        Generate a list of questions with answer
        :param question_count: number of question to be generated
        :return: list of questions with answer
        """
        questions = []
        while len(questions) < question_count:
            question = self.generate_question()
            if self.is_question_valid(question):
                questions.append(question)
        return questions

    def is_question_valid(self, question: Question) -> bool:
        """
        Check whether the question is valid
        :param question:
        :return: True/False
        """
        return sum(item[1] for item in question) <= self.maximum_objects_per_question

    def render_question_pages(self, questions: List[Question]):
        """
        Render questions
        :param questions: questions
        """
        for question_number in range(len(questions)):
            self.render_question(question_number, questions[question_number])

    def render_question(self, question_number: int, question: Question):
        """
        Render a question
        :param question_number:
        :param question:
        """
        image_size = 8
        max_row_size = 18
        self.pdf.add_page(orientation='L')
        images = []
        for item in question:
            for i in range(item[1]):
                images.append(item[0])
        random.shuffle(images)
        image_count = len(images)
        item_count = len(question)
        total_image_row = image_count // max_row_size + (1 if image_count % max_row_size > 0 else 0)
        self.pdf.cell(210, 10, txt=f'{question_number + 1}) {self.question_title}', align='L', ln=1)
        self.pdf.cell(210, 10, border='LTR', ln=1)
        for row_index in range(max(item_count, total_image_row)):
            if row_index < total_image_row:
                self.pdf.cell(10, 12, border='L', align='C')
                for column_index in range(max_row_size):
                    image_index = row_index * max_row_size + column_index
                    if image_index < image_count:
                        self.pdf.image(name=images[image_index], x=self.pdf.get_x() - 3 + column_index * 11, y=self.pdf.get_y() - 3, w=9, h=9)
                self.pdf.cell(200, 12, border='R')
            else:
                self.pdf.cell(210, 12, border='LR')
            if row_index < item_count:
                self.pdf.cell(20, 12, txt='How many', align='R')
                self.pdf.image(name=question[row_index][0], x=self.pdf.get_x() + 1, y=self.pdf.get_y() + 2, w=image_size, h=image_size)
                self.pdf.cell(16, 12, txt='?  ', align='R')
                self.pdf.cell(10, 8, border='B')
                self.pdf.cell(20, 12, txt=' ( Odd / Even )')
            self.pdf.ln()
        self.pdf.cell(210, 10, border='T')

    def render_answer_pages(self, questions):
        """
        Render answers
        :param questions:
        """
        self.pdf.add_page(orientation='L')
        self.pdf.cell(200, 10, txt='Answers', ln=1)
        image_size = 8
        for i in range(len(questions)):
            self.pdf.cell(10, 10, txt=f'{i + 1}:', border='TLB', align='R')
            for question in questions[i]:
                self.pdf.image(name=question[0], x=self.pdf.get_x() + 1, y=self.pdf.get_y() + 1, w=image_size, h=image_size)
                self.pdf.cell(20, 10, txt=f'    {question[1]}', border='TB', align='C')
            self.pdf.cell(2, 10, border='TRB', align='R', ln=1)


if __name__ == "__main__":
    LookAndFindWorksheet().generate()
