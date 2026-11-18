import os
import sys
import math
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import webview

def get_template_dir():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "templates")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

app = Flask(__name__, template_folder=get_template_dir())

RATES = {"moto": 0.50, "car": 2.00}
slots = {f"M-{i:02d}": None for i in range(1, 13)}
slots.update({f"C-{i:02d}": None for i in range(1, 9)})

total_revenue = 0.0
ticket_counter = 1000
entry_ticket = None   # Holds newly created check-in ticket to display/print
last_receipt = None   # Holds exit payment receipt
alert_msg = None


@app.route("/", methods=["GET"])
def index():
    moto_free = sum(1 for k, v in slots.items() if k.startswith("M") and v is None)
    car_free = sum(1 for k, v in slots.items() if k.startswith("C") and v is None)
    return render_template(
        "index.html",
        slots=slots,
        moto_free=moto_free,
        car_free=car_free,
        total_revenue=total_revenue,
        entry_ticket=entry_ticket,
        last_receipt=last_receipt,
        alert_msg=alert_msg,
    )


@app.route("/park", methods=["POST"])
def park():
    global alert_msg, last_receipt, entry_ticket, ticket_counter
    last_receipt = None
    entry_ticket = None
    v_type = request.form.get("v_type")
    plate = request.form.get("plate", "").strip().upper()

    if not plate:
        alert_msg = ("error", "Please enter a valid license plate.")
        return redirect(url_for("index"))

    if any(v and v["plate"] == plate for v in slots.values()):
        alert_msg = ("error", f"Vehicle {plate} is already parked inside!")
        return redirect(url_for("index"))

    prefix = "M-" if v_type == "moto" else "C-"
    open_slot = next((s for s, v in slots.items() if s.startswith(prefix) and v is None), None)

    if not open_slot:
        alert_msg = ("error", f"No {v_type.upper()} slots available!")
        return redirect(url_for("index"))

    ticket_counter += 1
    ticket_id = f"TKT-{ticket_counter}"
    now = datetime.now()

    vehicle_data = {
        "ticket_id": ticket_id,
        "slot": open_slot,
        "plate": plate,
        "type": v_type,
        "entry_time": now,
        "entry_str": now.strftime("%Y-%m-%d %H:%M:%S"),
        "short_time": now.strftime("%H:%M:%S"),
    }

    slots[open_slot] = vehicle_data
    entry_ticket = vehicle_data
    alert_msg = None
    return redirect(url_for("index"))


def process_checkout(slot_id):
    global total_revenue, last_receipt, alert_msg, entry_ticket
    entry_ticket = None
    vehicle = slots.get(slot_id)

    if not vehicle:
        alert_msg = ("error", "Slot is already empty.")
        return

    exit_time = datetime.now()
    duration_sec = (exit_time - vehicle["entry_time"]).total_seconds()
    billed_hrs = max(1, math.ceil(duration_sec / 3600))
    fee = billed_hrs * RATES[vehicle["type"]]

    total_revenue += fee
    last_receipt = {
        "ticket_id": vehicle["ticket_id"],
        "slot": slot_id,
        "plate": vehicle["plate"],
        "type": vehicle["type"].upper(),
        "entry": vehicle["short_time"],
        "exit": exit_time.strftime("%H:%M:%S"),
        "hours": billed_hrs,
        "fee": f"{fee:.2f}",
    }

    slots[slot_id] = None
    alert_msg = None


@app.route("/exit/<slot_id>", methods=["POST"])
def exit_vehicle(slot_id):
    process_checkout(slot_id)
    return redirect(url_for("index"))


@app.route("/verify_exit", methods=["POST"])
def verify_exit():
    global alert_msg, entry_ticket, last_receipt
    query = request.form.get("query", "").strip().upper()
    if not query:
        alert_msg = ("error", "Enter a Ticket ID (e.g. TKT-1001) or License Plate.")
        return redirect(url_for("index"))

    # Match by Ticket ID or License Plate
    matched_slot = next(
        (s for s, v in slots.items() if v and (v["ticket_id"] == query or v["plate"] == query)),
        None,
    )

    if not matched_slot:
        entry_ticket = None
        last_receipt = None
        alert_msg = ("error", f"No active vehicle found for '{query}'.")
        return redirect(url_for("index"))

    process_checkout(matched_slot)
    return redirect(url_for("index"))


if __name__ == "__main__":
    webview.create_window(
        title="Smart Moto & Car Parking System",
        url=app,
        width=1180,
        height=850,
        min_size=(900, 650),
    )
    webview.start()