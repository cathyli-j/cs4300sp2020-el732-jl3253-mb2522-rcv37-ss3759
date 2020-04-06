from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Better Yelp Recommendations"
net_id = "Emanuele Lusso: el732, Cathy Li: jl3253, Matias Blake: mb2522, Robert Villaluz: rcv37, Saaqeb Siddiqi: ss3759"

@irsystem.route('/page1', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = 'hello world'
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



