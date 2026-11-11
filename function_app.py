import datetime
import json
import logging
import uuid
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */1 * * * *", arg_name="mytimer", run_on_startup=False)
@app.queue_output(arg_name="msg", queue_name="queue-lab-2", connection="QueueConn")
def timer_demo(mytimer: func.TimerRequest, msg: func.Out[str]) -> None:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if mytimer.past_due:
        logging.info("Timer is past due (a scheduled run was missed)")

    payload = {"id": str(uuid.uuid4()), "created": now, "text": "hello from the timer"}
    msg.set(json.dumps(payload))
    logging.info("Queued message %s at %s UTC", payload["id"], now)