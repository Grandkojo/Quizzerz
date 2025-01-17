from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Users(db.Model):
    """ The users table """
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200))
    email = Column(String(200), unique=True)
    password = Column(String(200))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.userid
    
    def to_dict(self):
        return {
            "user_id": self.userid,
            "user_name": self.username,
            "email": self.email
        }

class Questions(db.Model):
    """ The questions table """
    __tablename__ = 'questions'
    questionid = Column(Integer, primary_key=True, autoincrement=True)
    question_category = Column(String)

class Categories(db.Model):
    """ The categories table """
    __tablename__ = 'categories'
    categoryid = Column(Integer, primary_key=True, autoincrement=True)
    cat_alias = Column(String, unique=True)
    category_name = Column(String)

class QuestionDetails(db.Model):
    """ The question_details table """
    __tablename__ = 'question_details'
    question_detailid = Column(Integer, primary_key=True, autoincrement=True)
    questionid = Column(Integer, ForeignKey('questions.questionid'))
    cat_alias = Column(String, ForeignKey('categories.cat_alias'))
    question_text = Column(String)
    
    question = relationship("Questions", back_populates="question_details")
    category = relationship("Categories", back_populates="question_details")

    def to_dict(self):
        return {
            "id": self.questionid,
            "question_text": self.question_text,
            "cat_alias": self.cat_alias
        }

class QuizResults(db.Model):
    """ The quiz_results table """
    __tablename__ = 'quiz_results'
    quiz_resultid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    catalias = Column(String, ForeignKey('categories.cat_alias'))
    result = Column(Float)
    details = Column(JSONB)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    
    user = relationship("Users", back_populates="quiz_results")
    category = relationship("Categories", back_populates="quiz_results")

    def to_dict(self):
        return {
            "userid": self.userid,
            "category": self.catalias,
            "result": self.result
        }
    def to_dict_details(self):
        return {
            "userid": self.userid,
            "quiz_details": self.details
        }

class AnswerOptions(db.Model):
    """ The answer_options table """
    __tablename__ = 'answer_options'
    answerid = Column(Integer, primary_key=True, autoincrement=True)
    questionid = Column(Integer, ForeignKey('questions.questionid'))
    answer_text = Column(String)
    is_correct = Column(Boolean)
    
    question = relationship("Questions", back_populates="answer_options")

    def to_dict(self):
        return {
            "questionid": self.questionid,
            "answerid": self.answerid,
            "answer_text": self.answer_text,
            "is_correct": self.is_correct
        }
    
class Admin(db.Model):
    """ The admin table """
    __tablename__ = 'admin'
    adminid = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String(200))
    admin_password = Column(String(200))
    admin_email = Column(String(200), unique=True)

    def set_password(self, password):
        self.admin_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.admin_password, password)
    

# Define back_populates on both sides of the relationships
Questions.question_details = relationship("QuestionDetails", back_populates="question")
Categories.question_details = relationship("QuestionDetails", back_populates="category")
Users.quiz_results = relationship("QuizResults", back_populates="user")
Categories.quiz_results = relationship("QuizResults", back_populates="category")
Questions.answer_options = relationship("AnswerOptions", back_populates="question")
