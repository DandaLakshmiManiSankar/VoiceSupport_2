from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone 

app = Flask(__name__)

# --- IN-MEMORY STORE FOR PARAMETER FIELDS (Fields 2-6) ---
TRANSCRIPTS = {
    2: {"text": "", "updated_at": None}, # Parameter 1
    3: {"text": "", "updated_at": None}, # Parameter 2
    4: {"text": "", "updated_at": None}, # Parameter 3
    5: {"text": "", "updated_at": None}, # Parameter 4 
    6: {"text": "", "updated_at": None}, # Parameter 5 
}
# --------------------------------------------------------

@app.route("/")
def index():
    # Serves templates/index2.html
    return render_template("index.html")

@app.route("/save_transcript", methods=["POST"])
def save_transcript():
    """
    API endpoint to receive and save the transcribed text for a specific field.
    Expects JSON: {"field": 2, "text": "Final text"}
    """
    data = request.get_json(force=True)
    # Ensure field is treated as int key
    field = int(data.get("field", 0))
    text = data.get("text", "").strip()

    if field not in TRANSCRIPTS:
        return jsonify({"success": False, "message": f"Invalid field number: {field} for this app."}), 400

    # Update the in-memory store
    TRANSCRIPTS[field]["text"] = text
    
    # Use timezone-aware datetime
    TRANSCRIPTS[field]["updated_at"] = datetime.now(timezone.utc).isoformat()

    return jsonify({
        "success": True, 
        "field": field, 
        "text": text, 
        "updated_at": TRANSCRIPTS[field]["updated_at"]
    })

@app.route("/get_transcripts", methods=["GET"])
def get_transcripts():
    """Return all saved transcripts (JSON)"""
    return jsonify({"success": True, "data": TRANSCRIPTS})

if __name__ == "__main__":
    # Run on a distinct port for easy concurrent testing
    app.run(host="0.0.0.0", port=5002, debug=True)
