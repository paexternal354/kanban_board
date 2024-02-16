from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dummy in-memory data structure to store tasks
tasks = {
    'To Do': [],
    'In Progress': [],
    'Done': []
}

@app.route('/')
def index():
    return render_template('kanban.html', tasks=tasks)

@app.route('/add-task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        tasks['To Do'].append({'title': title})
        return jsonify({"message": "Task added successfully"})
    return jsonify({"message": "Empty task title"}), 400

@app.route('/update-task', methods=['POST'])
def update_task():
    title = request.form.get('title')
    old_status = request.form.get('old_status')
    new_status = request.form.get('new_status')

    if title and old_status in tasks and new_status in tasks:
        if title in [task['title'] for task in tasks[old_status]]:
            tasks[old_status].remove({'title': title})
            tasks[new_status].append({'title': title})
            return jsonify({"message": "Task updated successfully"})
    return jsonify({"message": "Invalid request"}), 400

@app.route('/delete-task', methods=['POST'])
def delete_task():
    title = request.form.get('title')
    status = request.form.get('status')

    if title and status in tasks:
        if title in [task['title'] for task in tasks[status]]:
            tasks[status].remove({'title': title})
            return jsonify({"message": "Task deleted successfully"})
    return jsonify({"message": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)