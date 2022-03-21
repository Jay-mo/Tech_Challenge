from flask import Flask , jsonify, request
import os
from database import URL
from mongoengine import connect
from mongoengine.queryset.visitor import Q


app = Flask(__name__)


#use mongoengine to connect to mongodb database
# connect(host="mongodb://172.17.0.1:27017/cns_url_db")

MONGODB_HOSTNAME = os.environ.get('MONGODB_HOSTNAME', 'mongodb')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', 'malware_url_db')

connect(host="mongodb://"+ MONGODB_HOSTNAME + ":27017/" + MONGODB_DATABASE)


#An endpoint to submit a hostname and port and receive response to determine if url should be blocked or not.
@app.route("/urlinfo/1/<string:hostname_and_port>/<string:original_path_and_query_string>")
def get_url_status(hostname_and_port,original_path_and_query_string):

    #variables to hold query strings and originalpath
    query_string = request.query_string.decode("utf-8")
    original_path = original_path_and_query_string 

    if query_string:
        original_path += query_string
        
        

    hostname, port = hostname_and_port.rsplit(':')
                 

    #query to find if there is an entry in the db for the submitted hostname and port number
    url_query = URL.objects(Q(url=hostname) & Q(port=port))

    
    try:
        url_query_result = url_query.first().to_mongo().to_dict()
    except:
        url_query_result = {}

    #return a response with the block status of the submitted url
    if url_query_result:
        response = {
            "hostname": url_query_result["url"],
            "port": url_query_result["port"],
            "block_status": url_query_result["block_status"],
            "original_path_and_query_string": original_path
        }

    else:
        response = {
            "hostname": hostname,
            "port": port,
            "block_status": False,
            "original_path_and_query_string": original_path
        }

    return jsonify(response)


#This is an endpoint that can be used to update the malware database
@app.route("/urlinfo/1/<string:hostname_and_port>", methods=['POST'])
def update_url_list(hostname_and_port):

    hostname, port = hostname_and_port.rsplit(':')
    new_url = URL(url=hostname,port=port,block_status=True)
    try:
        new_url.save()
        return jsonify({
            'success': True
        })
    except:
        return jsonify({
            'success': False,
            'operation': 'unable to update url database'
        })
    
#This is an endpoint to print all the urls in the malware database.
#Needed for testing purposes while building out api functionality.
@app.route("/urlinfo/1/url_db")
def get_url_list():

    all_url = URL.objects()

    output = [ url.format() for url in all_url ]
    return jsonify(output)

if __name__ == "__main__":
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    # app.run(host='0.0.0.0',port="3300",debug=True)
    app.run(host='0.0.0.0',port=ENVIRONMENT_PORT,debug=True)