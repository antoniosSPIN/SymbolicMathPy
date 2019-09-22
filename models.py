import datetime
import enum
from sqlalchemy.orm import relationship

from app import db


class Base(db.Model):
    """Base model that provides some common features, such as automatic 'created'
    and 'modified' date columns.
    """

    __abstract__ = True
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=datetime.datetime.now, nullable=False)


class UserRole(Base):
    """A class representing the different user roles that a user can have in the system.
    """

    def __init__(self, name):
        self.name = name
    
    __tablename__ = 'user_role'
    user_role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)


class AuthUser(Base):
    """A class representing a user that can be authenticated to the system.
    """

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
    
    auth_user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(63), nullable=False)
    last_name = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(127), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class HasUserRole(Base):
    """A class representing the relationship of a user having been assigned a role.
    """

    def __init__(self, auth_user_id, user_role_id):
        self.auth_user_id = auth_user_id
        self.user_role_id = user_role_id

    __tablename__ = 'has_user_role'

    has_user_role_id = db.Column(db.Integer, primary_key=True)
    auth_user_id = db.Column(db.ForeignKey('auth_user.auth_user_id'), nullable=False, index=True)
    user_role_id = db.Column(db.ForeignKey('user_role.user_role_id'), nullable=False, index=True)

    auth_user = relationship('AuthUser')
    user_role = relationship('UserRole')


class Test(Base):
    """A class representing the test
    """

    def __init__(self, name, creator_id):
        self.name = name
        self.creator_id = creator_id
    
    __tablename__ = 'test'

    test_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False, index=True)
    creator_id = db.Column(db.ForeignKey('auth_user.auth_user_id'), nullable=False, index=True)

    auth_user = relationship('AuthUser')


class Problem(Base):
    """A class representing a problem of a test
    """

    def __init__(self, problem_statement, test_id):
        self.problem_statement = problem_statement
        self.test_id = test_id
    
    __tablename__ = 'problem'

    problem_id = db.Column(db.Integer, primary_key=True)
    problem_statement = db.Column(db.String(511), nullable=False)
    test_id = db.Column(db.ForeignKey('test.test_id'), nullable=False, index=True)

    test = relationship('Test')


class Difficulty(enum.Enum):
    EASY = 1
    EASY_MEDIUM = 2
    MEDIUM = 3
    MEDIUM_HARD = 4
    HARD = 5


class Question(Base):
    """A class representing a question of a problem
    """

    def __init__(self, question, difficulty, marks, answer, solution, problem_id):
        self.question = question
        self.difficulty = difficulty
        self.marks = marks
        self.answer = answer
        self.solution = solution
        self.problem_id = problem_id
    
    __tablename__ = 'question'

    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(511), nullable=False)
    difficulty = db.Column(db.Enum(Difficulty))
    marks = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    solution = db.Column(db.String(2047), nullable=False)
    problem_id = db.Column(db.ForeignKey('problem.problem_id'), nullable=False, index=True)

    problem = relationship('Problem')


class HasTakenTest(Base):
    """A class representing the relationship between the student and the test they have taken
    """

    def __init__(self, student_id, test_id, score):
        self.student_id = student_id
        self.test_id = test_id
        self.score = score
    
    __tablename__ = 'has_taken_test'

    has_taken_test_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.ForeignKey('auth_user.auth_user_id'), nullable=False, index=True)
    test_id = db.Column(db.ForeignKey('test.test_id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False, index=True)

    auth_user = relationship('AuthUser')
    test = relationship('Test')
