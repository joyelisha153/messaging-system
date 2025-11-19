from flask import Flask, request, jsonify
from tasks import send_email_task, log_time_task

app = Flask(__name__)


@app.route("/action")
def action():
    sendmail = request.args.get("sendmail")
    talktome = request.args.get("talktome")

    if sendmail:
        # Trigger async email task
        result = send_email_task.delay(sendmail)
        return jsonify({
            "status": "queued",
            "task": "send_email_task",
            "recipient": sendmail,
            "task_id": result.id,
        })

    if talktome is not None:
        # Trigger async time logging task
        result = log_time_task.delay()
        return jsonify({
            "status": "queued",
            "task": "log_time_task",
            "task_id": result.id,
        })

    return jsonify({
        "error": "Please provide ?sendmail=<email> or ?talktome=1"
    }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

