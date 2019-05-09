from application import app
from flask_script import Server, Manager


manager = Manager(app)
manager.add_command("runserver", Server('0.0.0.0', port=8000))
	
if __name__ == "__main__":
	manager.run()