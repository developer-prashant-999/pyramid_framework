import pandas as pd
import json
from waitress import serve
from pyramid.response import Response
from pyramid.config import Configurator
import math
from scipy.stats import chi2

def benford(request):
    if 'csv_file' in request.POST:
        csv_file = request.POST['csv_file'].file
        df = pd.read_csv(csv_file, header=None)
        print(df)
        first_digits = df.iloc[:, 0].astype(str).str[:1]
        print(first_digits)
        freq_observed = first_digits.value_counts().sort_index()
        freq_observed = freq_observed.reindex(index=range(1, 10), fill_value=0)

        print(freq_observed)

        benford_exp = pd.Series([math.log10(1 + 1 / d) for d in range(1, 10)], index=range(1, 10))
        benford_exp *= len(first_digits)
        chi_squared_stat_test= freq_observed-benford_exp
        print(chi_squared_stat_test)

        chi_squared_stat = ((freq_observed - benford_exp) ** 2 / benford_exp).sum()
        
        print(chi_squared_stat)
        degrees_of_freedom = 4  
        p_value = 1 - chi2.cdf(chi_squared_stat, degrees_of_freedom)
        print(p_value)
        if p_value >= 0.05:
            result_json = {'status': 'success', 'message': 'The input CSV file conforms to Benford’s law on first digits.'}
        else:
            result_json = {'status': 'failure', 'message': 'The input CSV file does not conform to Benford’s law on first digits.'}
        return Response(json.dumps(result_json), content_type='application/json; charset=utf-8')
    else:
        html = """
        <!DOCTYPE html>
<html>
  <head>
    <title>Benford's Law Checker</title>
    <style>
      body {
        font-family: sans-serif;
        margin: 0;
        padding: 0;
      }
      h1 {
        background-color: #1a1a1a;
        color: white;
        margin: 0;
        padding: 1em;
      }
      form {
        background-color: #f2f2f2;
        border: 1px solid #ccc;
        margin: 2em auto;
        padding: 1em;
        max-width: 600px;
      }
      label {
        display: block;
        font-weight: bold;
        margin-bottom: 0.5em;
      }
      input[type="file"] {
        display: block;
        margin-bottom: 1em;
      }
      button[type="submit"] {
        background-color: #4CAF50;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 1.2em;
        padding: 0.5em 1em;
        transition: background-color 0.2s;
      }
      button[type="submit"]:hover {
        background-color: #0099ff;
      }
    </style>
    <script>
      function validateForm() {
        var fileInput = document.getElementById('csv_file');
        if (!fileInput || !fileInput.files || !fileInput.files[0]) {
          alert('Please select a CSV file.');
          return false;
        }
        return true;
      }
    </script>
  </head>
  <body>
    <h1>Benford's Law Checker</h1>
    <form method="POST" enctype="multipart/form-data" onsubmit="return validateForm();">
      <label for="csv_file">Select a CSV file:</label>
      <input type="file" name="csv_file" id="csv_file">
      <button type="submit">Check</button>
    </form>
  </body>
</html>

        """
        return Response(html)


if __name__ == '__main__':
    config = Configurator()
    config.add_route('benford', '/benford')
    config.add_view(benford, route_name='benford')
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=8080)
