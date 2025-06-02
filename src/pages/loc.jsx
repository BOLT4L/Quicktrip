import { useState, useEffect, useRef } from "react";
import Sidebar from "../component/sidebar";
import Header from "../component/Header";
import api from "../api";
import { BRANCH } from "../constants";

export default function Loc() {
  const mapRef = useRef(null);
  const googleMapRef = useRef(null);
  const markersRef = useRef([]);
  const [vehicles, setVehicles] = useState([]);
  const [error, setError] = useState(null);

  const userBranchId = localStorage.getItem(BRANCH);

  const fetchVehicleLocations = async () => {
    try {
      const response = await api.get("/api/tracked-vehicles/");
      const data = response.data.filter(v => v.tracking && v.latitude && v.longitude);
      setVehicles(data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch vehicle locations.");
    }
  };

  useEffect(() => {
    fetchVehicleLocations();
    const interval = setInterval(fetchVehicleLocations, 10000);
    return () => clearInterval(interval);
  }, [userBranchId]);

  useEffect(() => {
    if (!mapRef.current || googleMapRef.current) return;

    googleMapRef.current = new window.google.maps.Map(mapRef.current, {
      zoom: 12,
      center: { lat: 9.03, lng: 38.74 },
    });
  }, []);

  useEffect(() => {
    if (!googleMapRef.current || vehicles.length === 0) return;

    markersRef.current.forEach(marker => marker.setMap(null));
    markersRef.current = [];

    const bounds = new window.google.maps.LatLngBounds();

    vehicles.forEach(vehicle => {
      const position = {
        lat: parseFloat(vehicle.latitude),
        lng: parseFloat(vehicle.longitude),
      };

      const marker = new window.google.maps.Marker({
        position,
        map: googleMapRef.current,
        title: vehicle.plate_number,
        label: {
          text: vehicle.plate_number,
          color: "#ffffff",
          fontSize: "12px",
          fontWeight: "bold",
        },
        icon: {
          path: window.google.maps.SymbolPath.CIRCLE,
          scale: 8,
          fillColor: "#3a86ff",
          fillOpacity: 0.8,
          strokeWeight: 1,
          strokeColor: "#fff",
        },
      });

      markersRef.current.push(marker);
      bounds.extend(position);
    });

    googleMapRef.current.fitBounds(bounds);
  }, [vehicles]);

  return (
    <div className="location-page">
      <Sidebar />
      <div className="right">
        <Header />
        <div className="page-header">
          <h1>Live Vehicle Location</h1>
        </div>

        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Tracked Vehicles</h2>
          </div>

          {error ? (
            <div className="alert alert-danger">{error}</div>
          ) : (
            <div className="location-content">
              {vehicles.length > 0 ? (
                <>
                  <div className="location-details">
                    {vehicles.map((v) => (
                      <div className="detail-item" key={v.id}>
                        <strong>{v.plate_number}</strong> – Lat:{" "}
                        {v.latitude.toFixed(6)}, Lng: {v.longitude.toFixed(6)}
                      </div>
                    ))}
                  </div>
                  <div className="map-container">
                    <div ref={mapRef} className="google-map"></div>
                  </div>
                </>
              ) : (
                <div className="no-location">
                  <p>No vehicles are currently being tracked in your branch.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .location-page {
          display: flex;
        }
        .right {
          width: 100%;
        }
        .page-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }
        .location-content {
          padding: 20px;
        }
        .location-details {
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 20px;
        }
        .map-container {
          height: 600px;
          border: 1px solid #ccc;
          border-radius: 8px;
          overflow: hidden;
        }
        .google-map {
          width: 100%;
          height: 100%;
        }
        .no-location {
          padding: 40px;
          text-align: center;
          background: #f0f0f0;
          border-radius: 8px;
        }
      `}</style>
    </div>
  );
}
