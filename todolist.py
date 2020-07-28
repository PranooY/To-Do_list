
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

while True:
    print(f"1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    action = input()
    today = datetime.today().date()
    if action == '1':
        # Today's tasks
        rows = session.query(Table).filter(Table.deadline == today).all()
        print(f"Today {today.day} {today.strftime('%b')}:")
        for i in range(len(rows)):
            print(f'{i+1}. {rows[i].task}')
        if not rows:
            print('Nothing to do!')
    elif action == '2':
        # Coming Week's task
        for i in range(7):
            post_today = today + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == post_today).all()
            print(post_today.strftime("%A %d %b:"))
            if not rows:
                print('Nothing to do!')
            for j in range(len(rows)):
                print(f"{j+1}. {rows[j].task}")
            print('')
    elif action == '3':
        # All tasks
        rows = session.query(Table.task, Table.deadline).order_by(Table.deadline.asc()).all()
        print('All tasks:')
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
    elif action == '4':
        # Missed tasks
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
    elif action == '5':
        # Add task
        print('Enter task')
        todo_task = input()
        print('Enter deadline')
        deadline_string = input()
        if deadline_string:
            todo_deadline = datetime.strptime(deadline_string, "%Y-%m-%d")
        else:
            todo_deadline = datetime.today().date()
        new_row = Table(task=todo_task, deadline=todo_deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')
    elif action == '6':
        # Delete task
        rows = session.query(Table.task, Table.deadline).order_by(Table.deadline.asc()).all()
        print('Chose the number of the task you want to delete:')
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")

        rows = session.query(Table).all()
        delete_row = rows[int(input()) - 1]
        session.delete(delete_row)
        session.commit()
    elif action == '0':
        break
    else:
        continue
    print('')
