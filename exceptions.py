class TaskError(Exception):
    '''Базовое исключение ддля ошибок'''

class TaskNotFound(TaskError):
    '''ошибка когда нужный id не будет найден'''
    def __init__(self,task_id:int) -> None:
        super().__init__(f"task with id {task_id} not found")
        self.task_id = task_id

class ValidationError(TaskError):
    '''вызывается когда ввод данных неверный'''
    pass

