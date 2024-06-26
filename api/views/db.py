from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Users(db.Model):
    """ The users table
    """
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True)
    username = Column(String(200))
    email = Column(String(200), unique=True)
    password = Column(String(200))

class Questions(db.Model):
    """ The questions table
    """
    __tablename__ = 'questions'
    questionid = Column(Integer, primary_key=True)
    question_category = Column(String)

class Categories(db.Model):
    """ The categories table
    """
    __tablename__ = 'categories'
    categoryid = Column(Integer, primary_key=True)
    category_name = Column(String)

class QuestionDetails(db.Model):
    """ The question_details table
    """
    __tablename__ = 'question_details'
    questionid = Column(Integer, ForeignKey('questions.questionid'), primary_key=True)
    categoryid = Column(Integer, ForeignKey('categories.categoryid'), primary_key=True)
    question_text = Column(String)
    question = relationship("Questions")

class QuizResults(db.Model):
    """ The quiz_results table
    """
    __tablename__ = 'quiz_results'
    quiz_resultid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    categoryid = Column(Integer, ForeignKey('categories.categoryid'))
    result = Column(Float)
    user = relationship("Users")
    category = relationship("Categories")

class AnswerOptions(db.Model):
    """ The answer_options table
    """
    __tablename__ = 'answer_options'
    answerid = Column(Integer, primary_key=True)
    questionid = Column(Integer, ForeignKey('questions.questionid'))
    answer_text = Column(String)
    is_correct = Column(Boolean)
    question = relationship("Questions")

# Additional foreign key constraints
Questions.question_details = relationship("QuestionDetails", back_populates="question")
Categories.question_details = relationship("QuestionDetails", back_populates="category")
Users.quiz_results = relationship("QuizResults", back_populates="user")
Categories.quiz_results = relationship("QuizResults", back_populates="category")
Questions.answer_options = relationship("AnswerOptions", back_populates="question")
