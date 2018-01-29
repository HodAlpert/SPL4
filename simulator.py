import os
import sqlite3
import atexit


class _Simulator:
    def __init__(self):
         self.conn=sqlite3.connect("world.db")
         self.occupiedTasks = []
         self.cursor = self.conn().cursor()
#checks if sql file exists
    def isFileExist(self):
        return os.path.isfile("world.db")
#gets all tasks in tasks table
    def getAllTasks(self):
        return self.cursor.execute("""
        SELECT id, task_name, worker_id, time_to_make FROM tasks
        """).fetchall()
# checks if task is currently performed by worker
    def isTaskOccupied(self, taskname):
        return taskname in self.occupiedTasks
# checks if worker status is Idle
    def isWorkerIdle(self, workerId):
        status=self.cursor.execute("""
            SELECT status FROM workers WHERE id=(?)
            """, [workerId]).fetchone()
        return status == "idle"
#returns all finished tasks
    def getAllFinishedTasks(self):
        return self.cursor.execute("""
                SELECT id, worker_id FROM tasks WHERE time_to_make=0
                """).fetchall()
# update worker status
    def updateWorkerStatus(self,workerId, status):
        self.conn.execute("UPDATE workers SET status=(?) WHERE id=(?)",[status,workerId])

    def deleteTask(self,taskId):
        self.conn.execute("DELETE FROM tasks WHERE id=(?)",[taskId])

# assume there is more then one step left for task, assume worker in working on task
    def reduce(self,taskid):

# assume worker is idle
    def assign(self, taskid):
        self.cursor.execute("""
                SELECT worker_id FROM tasks WHERE id=(?)
                """, (taskid))
        workerId = self.cursor.fetch()
        self.occupiedTasks.append(self,workerId)

# assume 0 steps left for task
    def finishTask(self, taskid):
        self.cursor.execute("""
                        SELECT worker_id FROM tasks WHERE id=(?)
                        """, (taskid))
        workerId = self.cursor.fetch()
        self.updateWorkerStatus(self,workerId,"idle")
        self.deleteTask(self,taskid)
        self.cursor.execute("""
                                SELECT name FROM workers WHERE id=(?)
                                """, (workerId))
        workerName = self.cursor.fetch()
        print(workerName+" says: All Done!")


    def isTasksNotEmpty(self):
        return len(self.occupiedTasks)!=0
    def close(self):
        self.conn.commit()
        self.conn.close()

def main():
    # checks if file already exists
    if os.path.isfile("world.db"):
        s = _Simulator()
        atexit.register(s.close())
        while s.isFileExist() and s.isTasksNotEmpty():
            tasks = s.getAllTasks()
            for task in tasks:
                if s.isTaskOccupied(task[0]):
                    s.reduce(task[0])
                elif s.isWorkerIdle(task[1]):
                    s.assign(task[0])
            finishedTasks = s.getAllFinishedTasks()
            for task in finishedTasks:
                s.finishTask(task[0])

if __name__ == '__main__':
    main()









