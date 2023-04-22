from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render_to_response
import pandas as pd
from waitress import serve

def csv_to_json(request):
 
    if 'csv_file' in request.POST:
     
        csv_file = request.POST['csv_file'].file
        df = pd.read_csv(csv_file)
        json_data = df.to_json()
        response = Response(json_data)
        response.headers['Content-Disposition'] = 'attachment; filename="converted.json"'
        return response
    else:
       
        form_html = render_to_response('form.html', {}, request=request)
        return form_html

if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_jinja2')


    config.add_jinja2_renderer('.html')
    config.add_route('csv_to_json', '/benford')
    config.add_view(csv_to_json, route_name='csv_to_json', renderer='string')
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=8080)
