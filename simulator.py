import os
import sqlite3

class _Simulator:
    def __init__(self):
        if os.path.isfile("world.db"):
            self.conn=sqlite3.connect("world.db")
            self.occupiedTasks = []

    def isFileExist(self):
        return os.path.isfile("world.db")

    def getAllTasks(self):
        cursor = self.conn().cursor()
        return cursor.execute("""
        SELECT id, task_name, worker_id, time_to_make FROM tasks
        """).fetchall()

    def isoccupied(self,taskname):
        return taskname in self.occupiedTasks

    def isWorkerBusy(self, workerId):
        cursor = self.conn().cursor()
        status=cursor.execute("""
            SELECT status FROM workers WHERE id=(?)
            """, [workerId]).fetchone()
        return status == "idle"

    def getAllFinishedTasks(self):
        cursor = self.conn().cursor()
        return cursor.execute("""
                SELECT task_name, worker_id, time_to_make FROM tasks WHERE time_to_make=0
                """).fetchall()

    def updateWorkerStatus(self,workerId, status):
        self.conn.execute("UPDATE workers SET status=(?) WHERE id=(?)",[status,workerId])

    def deleteTask(self,taskId):
        self.conn.execute("DELETE FROM tasks WHERE id=(?)",[taskId])

# assume there is more then one step left for task, assume worker in working on task
    def reduce(self,taskid, workerId):
# assume worker is idle
    def assign(self, taskName):
        self.occupiedTasks.append(self,)
# assume 0 steps left for task
    def finishTask(self, taskName):


    def isTasksNotEmpty(self, taskName):








