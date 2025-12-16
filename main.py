from sqlalchemy import create_engine, Integer, String, or_, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import json


class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///db1.sqlite', echo=True)

class Student(Base):
    __tablename__ = 'student'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"id:{self.id}, fullname:{self.fullname}"
    
Base.metadata.create_all(engine)


########### 10 ta malumot qushish ########### 
with Session(engine) as s:
    s1 = Student(fullname="HasanHusanov", age=19)
    s2 = Student(fullname="AliValiyev", age=20)
    s3 = Student(fullname="NappiAliyev", age=34)
    s4 = Student(fullname="MurodMurodov", age=12)
    s5 = Student(fullname="AbdurashidRashidov", age=16)
    s6 = Student(fullname="MuhammadYusupov", age=14)
    s7 = Student(fullname="AzizAhmedov", age=15)
    s8 = Student(fullname="HoshimHoshimov", age=113)
    s9 = Student(fullname="AbdurahmonHusanov", age=10)
    s10 = Student(fullname="UmidNuriddinov", age=9)

    s.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
    s.commit()


########### yoshi 30 dan kattalarini chiqarish ###########
with Session(engine) as s:
    students = s.query(Student).filter(Student.age > 30).all()

    for i in students:
        print(i)


########### faqat grade = "A" bo‘lgan studentlar ###########
with Session(engine) as s:
    students = s.query(Student).filter(Student.fullname.like("A%")).all()
    for i in students:
        print(i)


########### studentlarni name bo’yicha alfabet tartibida ###########
with Session(engine) as s:
    students = s.query(Student).order_by(Student.fullname.asc()).all()
    for i in students:
        print(i)


########### json fileda bir nechta userlarni uqib db ga yozish ###########
with open('students.json', 'r') as f:
        data = json.load(f)

with Session(engine) as s:
    for i in data:
        fullname = i.get('fullname')
        age = i.get('age')

        if fullname is None or age is None:
            raise ValueError("student object not found")
        
        student = Student(fullname=fullname, age=age)
        s.add_all(student)
    s.commit()


########### Userlari name i ichida “ali” yoki “jon” qatnashga barcha userlar ###########
with Session(engine) as s:
    students = s.query(Student).filter(or_(Student.fullname.like("%Ali%"), Student.fullname.like("%Jon%"))).all()
    for i in students:
        print(i)


########### User ichida Yosh eng kichik 3 tasini ekranga chiqarish ###########
with Session(engine) as s:
    students = s.query(Student).order_by(Student.age.asc()).limit(3).all()
    for i in students:
        print(students)


########### User ichida Yosh eng kichik 3 tasini ekranga chiqarish ###########
with Session(engine) as s:
    students = s.query(Student).filter(and_(Student.phone.like("+99891%"), Student.adress == 'Fergana')).all()
    for i in students:
        print(i)

########### Book nomli model yaratish, 10 ta malumot qushish va db ga qushish ###########
class Book(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    desc: Mapped[str]
    price: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"title:{self.title}"
    
with Session(engine) as b:
    b1 = Book(title='python', desc='aljsdhfaj', price=20000, year=2026)
    b2 = Book(title='Atom_Odatlari', desc='aklsdjf', price=30000, year=2024)
    b3 = Book(title='HurryPoter', desc='a;ljsdf', price=60000, year=2022)
    b4 = Book(title='Garri', desc='a;lkshdf', price=90000, year=2011)
    b5 = Book(title='Intersteller', desc='alk;sdf', price=100000, year=1870)
    b6 = Book(title='Horror', desc='aljsdhfaj', price=23000, year=2001)
    b7 = Book(title='Kelajak', desc='alkj;sdhf', price=250000, year=2000)
    b9 = Book(title='Boon', desc='alksdnf', price=30000, price=1999)
    b10 = Book(title='Artist', desc=';alksdhf', price=50000, year=2022)

    b.add_all([b1,b2,b3,b4,b5,b6,b7,b9,b10])
    b.commit()


with Session(engine) as b:
    books = b.query(Book).all()

with open("book.json", 'w') as f:
    data = []
    for i in books:
        data.append({
            "id": i.id,
            "title": i.title,
            "desc": i.desc,
            "price": i.price
        })
    json.dump(data, f, indent=4)


########### Book narxi 50_000 dan katta va 2020 dan keyin chiqarilgan kitoblar ###########
with Session(engine) as b:
    books = b.query(Book).filter(and_(Book.price > 50000, Book.year > 2020)).all()
    for i in books:
        print(i)


########### Book tablidagi kitoblarni narxi bo’yicha kamayish taribida ###########
with Session(engine) as b:
    books = b.query(Book).order_by(Book.price.desc()).all()

    for i in books:
        print(i)