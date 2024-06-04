import io
from flask import Flask, jsonify, request, send_file, redirect
from persistance import get_all_records, get_picture_from_db, get_record_by_id, get_all_accepted_records, accept_record
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def default():
    return redirect('/pothole', code=302)


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
    image_url = get_picture_from_db(record_id=id)
    if image_url:
        return send_file(
            image_url,
            mimetype='image/jpg',
            as_attachment=True,
            download_name='%s.jpg' % id)
    else:
        return jsonify({"message": f"Image with ID {id} was not found"}), 404


@app.route("/pothole/accepted_records")
def getAllAcceptedRecords():
    """
    API endpoint to retrieve all records with 'accepted' set t
    o True.
    """
    records = get_all_accepted_records()
    return jsonify(records)  # Convert records to JSON for response


@app.route("/pothole/accept_record/<id>", methods=["PUT"])
def acceptRecord(id):
    """
    API endpoint to update the 'accepted' column to True for a record with the specified ID.
    """
    if not get_record_by_id(id):
        return jsonify({"error": f"No record found with id {id}."}), 404

    result = accept_record(record_id=id)
    if result:
        return jsonify({"message": f"Record with ID {id} accepted successfully!"}), 200
    else:
        return jsonify({"error": "An error occurred while accepting the record."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
