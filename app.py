from flask import Flask, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates")

# ---- CRM public API config (read from .env) ----
CRM_API_BASE = os.getenv("CRM_API_BASE", "https://crm.nishahomes.com")
CRM_API_KEY = os.getenv("CRM_API_KEY")


def fetch_properties(listing_type="all"):
    """
    Server-side call to the CRM's public inventory feed. This runs on the
    backend only — the API key never reaches the browser, so there's
    nothing for a visitor to see in view-source or devtools.
    listing_type: "all" | "inventory" | "project"
    """
    if not CRM_API_KEY:
        print("[warn] CRM_API_KEY not set in .env — property fetches will return empty")
        return []

    try:
        resp = requests.get(
            f"{CRM_API_BASE}/api/public/inventory",
            params={"type": listing_type},
            headers={"X-API-Key": CRM_API_KEY},
            timeout=15
        )
        resp.raise_for_status()
        payload = resp.json()
        return payload.get("data", [])
    except Exception as e:
        print(f"[error] fetching properties (type={listing_type}): {e}")
        return []


@app.route("/")
def home():
    # Homepage teaser: up to 12 mixed listings (inventory + projects)
    properties = fetch_properties("all")[:12]
    return render_template("index.html", properties=properties)


@app.route("/inventory")
def inventory_page():
    properties = fetch_properties("inventory")
    return render_template(
        "properties.html",
        properties=properties,
        page_title="Inventory",
        active_filter="inventory"
    )


@app.route("/projects")
def projects_page():
    properties = fetch_properties("project")
    return render_template(
        "properties.html",
        properties=properties,
        page_title="Projects",
        active_filter="project"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5173)  # 🔥 unique port