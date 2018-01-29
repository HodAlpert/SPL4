import sqlite3
import sys
import os

def readFile(filename, cursor):
    taskId = 1
    filehandle = open(filename)
    for line in filehandle:
        newLine = line.split(',')
        newLine[-1] = newLine[-1].replace('\n', '')
        if newLine[0] == 'worker':
            cursor.execute("""INSERT INTO workers VALUES(?,?,?)""", (int(newLine[1]),newLine[2],'idle'))
        elif len(newLine) == 2:
            cursor.execute("INSERT INTO resources VALUES(?,?)", (newLine[0], int(newLine[1])))
        else:
            cursor.execute("""INSERT INTO tasks VALUES(?,?,?,?,?,?)""", (taskId,newLine[0],int(newLine[1]),int(newLine[4]),newLine[2],newLine[3]))
            taskId = taskId+1

    filehandle.close()

def createDB():
    databaseexisted = os.path.isfile('world.db')

    dbcon = sqlite3.connect('world.db')
    with dbcon:
        cursor = dbcon.cursor()
        if not databaseexisted:  # First time creating the database. Create the tables
            cursor.execute("CREATE TABLE workers(id INTEGER PRIMARY KEY,name TEXT NOT NULL,status TEXT NOT NULL)")
            cursor.execute("CREATE TABLE resources(name TEXT PRIMARY KEY,amount INTEGER NOT NULL)")
            cursor.execute("CREATE TABLE tasks(id INTEGER PRIMARY KEY, task_name TEXT NOT NULL,worker_id INTEGER REFERENCES workers(id),time_to_make INTEGER NOT NULL,resource_name TEXT NOT NULL,resource_amount INTEGER NOT NULL)")
            filename = os.path.abspath(os.path.realpath(sys.argv[1]))
            readFile(filename, cursor)

            # cursor.execute("SELECT * FROM workers")
            # workerslist = cursor.fetchall()
            # print("All workers as list:")
            # print(workerslist)
            # print("-------------------------------")
            # cursor.execute("SELECT * FROM resources")
            # resourceslist = cursor.fetchall()
            # print("All resources as list:")
            # print(resourceslist)
            # print("-------------------------------")
            # cursor.execute("SELECT * FROM tasks")
            # taskslist = cursor.fetchall()
            # print("All tasks as list:")
            # print(taskslist)
            # print("-------------------------------")
    dbcon.commit()
    dbcon.close()
    # os.remove('world.db')

if __name__ == '__main__':
    createDB()


