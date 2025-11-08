import base64
import io
import base64
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from flask import Blueprint, jsonify, request, session
from matplotlib.colors import TwoSlopeNorm
from pathlib import Path
from service.simulation.model import build_unet, to_tensor
from service.imagery.session_store import get_session_data

simulate_bp = Blueprint("simulate", __name__, url_prefix="/simulate")

weights_path = Path(__file__).resolve().parent.parent / "simulation" / "checkpoints" / "epoch_03.weights.h5"
model = build_unet()
model.load_weights(weights_path)
print(f"Model loaded from {weights_path}")

def _validate_query_params() -> Tuple[Optional[str], Optional[str]]:
    # Array with point types and coordinates
    point_types = request.args.get("types")
    point_latitudes = request.args.get("lons")
    point_longitudes = request.args.get("lats")

    # convert to float
    point_latitudes = [float(lat) for lat in point_latitudes.split(",") if lat]
    point_longitudes = [float(lon) for lon in point_longitudes.split(",") if lon]
    point_types = [point_type.strip() for point_type in point_types.split(",") if point_type]

    if not point_types or not point_latitudes or not point_longitudes:
        return None, None, None

    return point_types, point_latitudes, point_longitudes

@simulate_bp.route("", methods=["GET"], strict_slashes=False)
def simulate():
    point_types, point_latitudes, point_longitudes = _validate_query_params()

    session_id = session.get("session_id")
    if not session_id:
        return jsonify({"error": "Session ID not found"}), 400

    print(f"Session ID: {session_id}")
    session_data = get_session_data(session_id)

    if session_data is None:
        return jsonify({"error": "Session data not found"}), 400
    if not "heat_map" in session_data:
        return jsonify({"error": "Session data not found"}), 400
    if not "data" in session_data["heat_map"]:
        return jsonify({"error": "Heat map data not found"}), 400

    heat_map = session_data["heat_map"]["data"]
    bbox = session_data["heat_map"]["bbox"]
    heat_shape = heat_map.shape

    ndvi_delta = np.zeros(heat_shape)

    for point_type, point_latitude, point_longitude in zip(point_types, point_latitudes, point_longitudes):
        # map points to the ndvi_delta array
        lon_min, lat_min, lon_max, lat_max = bbox

        col = (point_longitude - lon_min) / (lon_max - lon_min) * heat_shape[1]
        row = (lat_max - point_latitude) / (lat_max - lat_min) * heat_shape[0]

        row = int(np.clip(row, 0, heat_shape[0] - 1))
        col = int(np.clip(col, 0, heat_shape[1] - 1))

        # clip the row and col to the heat map shape
        row = np.clip(row, 0, heat_shape[0] - 1)
        col = np.clip(col, 0, heat_shape[1] - 1)

        print(f"Row: {row}, Col: {col}")
        print(f"point_type: {point_type}")

        if point_type == "trees":
            ndvi_delta[row, col] += 0.3
        elif point_type == "shrubs":
            ndvi_delta[row, col] += 0.15
        elif point_type == "grass":
            ndvi_delta[row, col] += 0.05
        elif point_type == "buildings":
            ndvi_delta[row, col] -= 0.3
        elif point_type == "roads":
            ndvi_delta[row, col] -= 0.15
        elif point_type == "waterbodies":
            ndvi_delta[row, col] -= 0.9

        if ndvi_delta[row, col] != 0:
            print(f"NDVI Delta at {row}, {col}: {ndvi_delta[row, col]}")

        ndvi_delta[row, col] = np.clip(ndvi_delta[row, col], -2, 2)

    data_input = {
        "ndvi_delta": ndvi_delta,
    }

    # ndvi_tensor = to_tensor([data_input], "ndvi_delta")
    # predicted_delta = model.predict(ndvi_tensor)
    # predicted_delta = predicted_delta.squeeze()
    # predicted_delta = predicted_delta.numpy().tolist()

    # ndvi_tile = ndvi_tensor.squeeze()

    ndvi_tile = ndvi_delta

    ndvi_min = np.nanmin(ndvi_tile)
    ndvi_max = np.nanmax(ndvi_tile)
    ndvi_span = max(abs(ndvi_min), abs(ndvi_max)) or 1e-6

    print(f"NDVI Min: {ndvi_min}, NDVI Max: {ndvi_max}, NDVI Span: {ndvi_span}")
    print(f"MEAN NDVI: {np.mean(ndvi_tile)}")

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(
        ndvi_tile,
        cmap="RdBu",
        norm=TwoSlopeNorm(vmin=-ndvi_span, vcenter=0, vmax=ndvi_span),
    )
    ax.set_title("NDVI Δ (simulated)")
    ax.axis("off")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("NDVI Δ (unitless)")

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.show()
    plt.close(fig)
    buffer.seek(0)
    ndvi_image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    if not point_types or not point_latitudes or not point_longitudes:
        return jsonify({"error": "Missing required query parameters: types, lats, lons"}), 400

    return jsonify(
        {
            "message": "Simulation API is working",
            "ndvi_delta_image": ndvi_image_base64,
        }
    ), 200
