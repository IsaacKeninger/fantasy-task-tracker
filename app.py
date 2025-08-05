
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

class toDo:

    # Initialize an overall list
    def __init__(self, title, theme):
        self.title = title
        self.theme = theme
        self.items = []
        self.completedItems = []

    def __len__(self):
        return len(self.items)
    
    def addItem(self, item):
        if len(self.items) > 14:
            print("item limit reached")
            return 
        self.items.append(item)

    def removeItem(self,item):
        if item in self.completedItems:
            self.completedItems.remove(item)
        elif item in self.items:
            self.items.remove(item)


    def completeItem(self, item):
        self.completedItems.append(item)
        self.items.remove(item)

    def to_dict(self):
        return {
            'title': self.title,
            'theme': self.theme,
            'items': self.items,
            'completedItems': self.completedItems
        }
    
    def uncompleteItem(self, item):
        if item in self.completedItems:
            self.completedItems.remove(item)
            self.items.append(item)

    # Magic method for the print function
    def __repr__(self):
        return "Items to Do: " + str(self.items) +  " Items Completed: " + str(self.completedItems)
    

# Initiate Flask Application

app = Flask(__name__)
CORS(app)

# Global todo list instance
todo_list = toDo("Task Tracker", "default")

#Routes

@app.route('/')
def index():
    #Serves to main html page.
    return render_template('index.html')

@app.route('/api/todo', methods=['GET'])
def get_todo():
    return jsonify(todo_list.to_dict())

@app.route('/api/todo/add', methods=['POST'])
def add_item():

    if len(todo_list) > 14:
        return jsonify({'error': 'Item Limit Reached'}), 400
    
    data = request.get_json()
    if not data or 'item' not in data:
        return jsonify({'error': 'Item is required'}), 400
        
    item = data['item'].strip()
    if not item:
        return jsonify({'error': 'Item cannot be empty'}), 400

    todo_list.addItem(item)
    return jsonify({'message': 'Item added successfully', 'todo': todo_list.to_dict()})



@app.route('/api/todo/remove', methods=['POST'])
def remove_item():
    """Remove an item from the todo list"""
    data = request.get_json()
    if not data or 'item' not in data:
        return jsonify({'error': 'Item is required'}), 400
    
    item = data['item']
    todo_list.removeItem(item)
    return jsonify({'message': 'Item removed successfully', 'todo': todo_list.to_dict()})

@app.route('/api/todo/complete', methods=['POST'])
def complete_item():
    """Mark an item as completed"""
    data = request.get_json()
    if not data or 'item' not in data:
        return jsonify({'error': 'Item is required'}), 400
    
    item = data['item']
    todo_list.completeItem(item)
    return jsonify({'message': 'Item completed successfully', 'todo': todo_list.to_dict()})

@app.route('/api/todo/uncomplete', methods=['POST'])
def uncomplete_item():
    """Mark a completed item as incomplete"""
    data = request.get_json()
    if not data or 'item' not in data:
        return jsonify({'error': 'Item is required'}), 400
    
    item = data['item']
    todo_list.uncompleteItem(item)
    return jsonify({'message': 'Item marked as incomplete', 'todo': todo_list.to_dict()})

@app.route('/api/todo/update', methods=['POST'])
def update_todo():
    """Update todo list title and theme"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Data is required'}), 400
    
    if 'title' in data:
        todo_list.title = data['title']
    if 'theme' in data:
        todo_list.theme = data['theme']
    
    return jsonify({'message': 'Todo list updated successfully', 'todo': todo_list.to_dict()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
