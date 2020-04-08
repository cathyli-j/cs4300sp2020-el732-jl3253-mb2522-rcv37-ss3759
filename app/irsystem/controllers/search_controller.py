from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Tastes Like Home"
net_id = "Cathy Li: jl3253, Matías Blake: mb2522, Emanuele Lusso: el732, Saaqeb Siddiqi: ss3759, Robert Villaluz: rcv37"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



