from fastapi import FastAPI

api = FastAPI()

all_todos=[
    {'todo_id':1,'todo_name':'Sports','todo_description':'Go to the gym'},
    {'todo_id':2,'todo_name':'Read','todo_description':'Read 10 pages'},
    {'todo_id':3,'todo_name':'Shop','todo_description':'Go shopping'},
    {'todo_id':4,'todo_name':'Study','todo_description':'Study for exam'},
    {'todo_id':5,'todo_name':'Meditate','todo_description':'Meditate for 20 mins'}

]

# GET , POST, PUT , DELETE

@api.get('/')
def index():
    return {'message':'Hello World'}


# get data from database - this should be a asynchronous request
# retrieve something from todo using path parameters pass from {todo_id} to function

@api.get('/todos/{todo_id}')
def get_data_from_db(todo_id:int):
    for todo in all_todos:
        if todo['todo_id']== todo_id:
            return {'result': todo}


# this for getting first n values 

@api.get('/todos')
def get_todos(first_n:int = None):            # pydantic automatically validates it as string
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
 
@api.post('/todos')
def create_todo(todo:dict):
    new_todo_id= max(todo['todo_id'] for todo in all_todos) + 1
    new_todo= {
        'todo_id' : new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }

    all_todos.append(new_todo)

    return new_todo


@api.put('/todos/{todo_id}')
def update_todo(todo_id:int, updated_todo:dict):
    for todo in all_todos:
        if todo in all_todos:
            if todo['todo_id']==todo_id:
                todo['todo_name']=update_todo['todo_name']
                todo['todo_description']=update_todo['todo_description']
                return todo
    return "Error not found"

@api.delete('/todos/{todo_id}')
def delete_todo(todo_id:int):
    for index, todo in enumerate(all_todos):
        if todo['todo_id']==todo_id:
            deleted_todo =all_todos.pop(index)
            return deleted_todo

        return "Error not found"
