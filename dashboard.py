import os
import csv
from datetime import datetime, date, timedelta
from collections import Counter

from flask import Flask, render_template_string

app = Flask(__name__)

LOG_FILES = ["smartroad_events.csv", "pothole_events.csv"]


def get_log_file():
    for path in LOG_FILES:
        if os.path.exists(path):
            return path
    return LOG_FILES[-1]


def load_events():
    log_file = get_log_file()
    events = []

    if not os.path.exists(log_file):
        return events, log_file

    with open(log_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = datetime.strptime(row["Timestamp"].strip(), "%Y-%m-%d %H:%M:%S")
                conf = float(row["Confidence"])
                events.append({"timestamp": ts, "confidence": conf})
            except Exception:
                continue

    events.sort(key=lambda x: x["timestamp"], reverse=True)
    return events, log_file


@app.route("/")
def index():
    events, log_file = load_events()

    total = len(events)
    avg_conf = round(sum(e["confidence"] for e in events) / total, 2) if total else 0.0
    latest_time = events[0]["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if events else "No detections yet"
    latest_conf = f'{events[0]["confidence"]:.2f}' if events else "-"

    today = date.today()
    detections_today = sum(1 for e in events if e["timestamp"].date() == today)

    day_counts = Counter(e["timestamp"].date() for e in events)
    last_7_days = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        last_7_days.append({
            "label": d.strftime("%a"),
            "date": d.strftime("%Y-%m-%d"),
            "count": day_counts.get(d, 0),
        })

    recent_events = events[:10]
    max_count = max((item["count"] for item in last_7_days), default=1)

    template = """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta http-equiv="refresh" content="5">
      <title>SmartRoadAI Dashboard</title>
      <style>
        :root {
          --bg: #0f1115;
          --panel: #171a21;
          --panel2: #1d2230;
          --text: #f2f4f8;
          --muted: #a9b1c3;
          --accent: #7c5cff;
          --accent2: #26d07c;
          --border: #2a3142;
        }
        * { box-sizing: border-box; }
        body {
          margin: 0;
          font-family: Arial, Helvetica, sans-serif;
          background: linear-gradient(180deg, #0b0d12 0%, #111522 100%);
          color: var(--text);
        }
        .wrap {
          max-width: 1200px;
          margin: 0 auto;
          padding: 28px 18px 40px;
        }
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 16px;
          margin-bottom: 22px;
          flex-wrap: wrap;
        }
        .title h1 {
          margin: 0 0 6px;
          font-size: 30px;
        }
        .title p {
          margin: 0;
          color: var(--muted);
        }
        .badge {
          display: inline-block;
          padding: 8px 12px;
          border: 1px solid var(--border);
          border-radius: 999px;
          background: rgba(124, 92, 255, 0.12);
          color: var(--text);
          font-size: 13px;
        }
        .grid {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 14px;
          margin-bottom: 18px;
        }
        .card {
          background: rgba(23, 26, 33, 0.95);
          border: 1px solid var(--border);
          border-radius: 18px;
          padding: 18px;
          box-shadow: 0 10px 30px rgba(0,0,0,.18);
        }
        .card .label {
          color: var(--muted);
          font-size: 13px;
          margin-bottom: 10px;
        }
        .card .value {
          font-size: 28px;
          font-weight: 700;
          line-height: 1.1;
        }
        .card .sub {
          margin-top: 8px;
          color: var(--muted);
          font-size: 13px;
        }
        .layout {
          display: grid;
          grid-template-columns: 1.2fr 1fr;
          gap: 14px;
        }
        .section-title {
          margin: 0 0 14px;
          font-size: 18px;
        }
        table {
          width: 100%;
          border-collapse: collapse;
        }
        th, td {
          text-align: left;
          padding: 12px 10px;
          border-bottom: 1px solid var(--border);
          font-size: 14px;
        }
        th {
          color: var(--muted);
          font-weight: 600;
        }
        .pill {
          display: inline-block;
          padding: 5px 10px;
          border-radius: 999px;
          background: rgba(38, 208, 124, 0.12);
          color: #7ff0b2;
          font-size: 12px;
          border: 1px solid rgba(38, 208, 124, 0.2);
        }
        .bar-row {
          display: grid;
          grid-template-columns: 52px 1fr 28px;
          align-items: center;
          gap: 10px;
          margin-bottom: 12px;
        }
        .bar-track {
          height: 12px;
          background: #121622;
          border-radius: 999px;
          overflow: hidden;
          border: 1px solid var(--border);
        }
        .bar-fill {
          height: 100%;
          background: linear-gradient(90deg, var(--accent), #4fd1c5);
          border-radius: 999px;
        }
        .footer {
          margin-top: 14px;
          color: var(--muted);
          font-size: 12px;
        }
        .empty {
          color: var(--muted);
          font-size: 14px;
          padding: 14px 0;
        }
        @media (max-width: 900px) {
          .grid, .layout { grid-template-columns: 1fr; }
        }
      </style>
    </head>
    <body>
      <div class="wrap">
        <div class="header">
          <div class="title">
            <h1>SmartRoadAI Dashboard</h1>
            <p>Real-time pothole monitoring and event analytics</p>
          </div>
          <div class="badge">Live log: {{ log_file }}</div>
        </div>

        <div class="grid">
          <div class="card">
            <div class="label">Total Detections</div>
            <div class="value">{{ total }}</div>
            <div class="sub">All logged pothole events</div>
          </div>
          <div class="card">
            <div class="label">Average Confidence</div>
            <div class="value">{{ avg_conf }}</div>
            <div class="sub">Mean confidence score</div>
          </div>
          <div class="card">
            <div class="label">Detections Today</div>
            <div class="value">{{ detections_today }}</div>
            <div class="sub">Events from {{ today }}</div>
          </div>
          <div class="card">
            <div class="label">Latest Detection</div>
            <div class="value" style="font-size:18px">{{ latest_time }}</div>
            <div class="sub">Confidence: {{ latest_conf }}</div>
          </div>
        </div>

        <div class="layout">
          <div class="card">
            <h2 class="section-title">Recent Detections</h2>
            {% if recent_events %}
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {% for e in recent_events %}
                <tr>
                  <td>{{ e.timestamp.strftime("%Y-%m-%d %H:%M:%S") }}</td>
                  <td><span class="pill">{{ "%.2f"|format(e.confidence) }}</span></td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
            {% else %}
            <div class="empty">No detections logged yet.</div>
            {% endif %}
          </div>

          <div class="card">
            <h2 class="section-title">Last 7 Days</h2>
            {% for item in last_7_days %}
            <div class="bar-row">
              <div style="color: var(--muted); font-size: 13px;">{{ item.label }}</div>
              <div class="bar-track">
                <div class="bar-fill" style="width: {{ (item.count / max_count * 100) if max_count else 0 }}%;"></div>
              </div>
              <div style="text-align:right;">{{ item.count }}</div>
            </div>
            {% endfor %}
          </div>
        </div>

        <div class="footer">
          Auto-refreshes every 5 seconds.
        </div>
      </div>
    </body>
    </html>
    """

    return render_template_string(
        template,
        total=total,
        avg_conf=f"{avg_conf:.2f}",
        latest_time=latest_time,
        latest_conf=latest_conf,
        detections_today=detections_today,
        recent_events=recent_events,
        last_7_days=last_7_days,
        max_count=max_count,
        today=today.strftime("%Y-%m-%d"),
        log_file=log_file,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)