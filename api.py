from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
spark = SparkSession.builder.master("local[*]").getOrCreate()

@app.route("/execute", methods=["POST", "OPTIONS"])
def execute_spark():
   if request.method == "OPTIONS":
       return "", 200

   code = request.get_data(as_text=True)
   try:
       # Capture result
       locals_dict = {}
       exec(code, globals(), locals_dict)
       result = locals_dict.get('result')

       if result:
           return jsonify({
               "schema": [{"name": f.name, "type": str(f.dataType)}
                         for f in result.schema],
               "data": [row.asDict() for row in result.collect()]
           })
       return jsonify({"error": "No result found"})
   except Exception as e:
       return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
