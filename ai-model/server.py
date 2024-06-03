import io
from flask import Flask, jsonify, request, send_file
from persistance import get_all_records, get_picture_from_db, get_record_by_id, get_all_accepted_records, accept_record
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route("/pothole")
def getAllRecords():
    # return all potholes
    return get_all_records()


@app.route("/pothole/<id>")
def getRecordById(id):
    record = get_record_by_id(id)

    if record:
        return jsonify(record)
    else:
        return jsonify({"message": f"Record with ID {id} was not found"}), 404


@app.route("/pothole/picture/<id>")
def getRecordPicture(id):
    image = get_picture_from_db(id)
    if image:
        return send_file(
            io.BytesIO(image),
            mimetype='image/jpg',
            as_attachment=True,
            download_name='%s.jpg' % id)
    else:
        return jsonify({"message": f"Image with ID {id} was not found"}), 404


@app.route("/accepted_records")
def get_all_accepted_records():
    """
    API endpoint to retrieve all records with 'accepted' set to True.
    """
    records = get_all_accepted_records(
        database_file="my_database.db", table_name="places")
    return jsonify(records)  # Convert records to JSON for response


@app.route("/accept_record/<id>", methods=["PUT"])
def accept_record(id):
    """
    API endpoint to update the 'accepted' column to True for a record with the specified ID.
    """
    result = accept_record(database_file="my_database.db",
                           table_name="places", record_id=id)
    if result:
        return jsonify({"message": f"Record with ID {id} accepted successfully!"}), 200
    else:
        return jsonify({"error": "An error occurred while accepting the record."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
