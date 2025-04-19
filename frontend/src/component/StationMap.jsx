
import { useEffect, useRef } from "react"

const StationMap = ({ stations, selectedStation, zoom = 1, onSelectStation }) => {
  const mapRef = useRef(null)

  useEffect(() => {
    if (!mapRef.current) return

    const ctx = mapRef.current.getContext("2d")
    const width = mapRef.current.width
    const height = mapRef.current.height

    // Clear canvas
    ctx.clearRect(0, 0, width, height)

    // Draw background
    ctx.fillStyle = "#f0f0f0"
    ctx.fillRect(0, 0, width, height)

    // Draw grid lines
    ctx.strokeStyle = "#e0e0e0"
    ctx.lineWidth = 1

    // Vertical grid lines
    for (let x = 0; x < width; x += 50) {
      ctx.beginPath()
      ctx.moveTo(x, 0)
      ctx.lineTo(x, height)
      ctx.stroke()
    }

    // Horizontal grid lines
    for (let y = 0; y < height; y += 50) {
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(width, y)
      ctx.stroke()
    }

    // Find bounds of all stations
    const lats = stations.map((s) => s.location.latitude)
    const lngs = stations.map((s) => s.location.longitude)

    const minLat = Math.min(...lats)
    const maxLat = Math.max(...lats)
    const minLng = Math.min(...lngs)
    const maxLng = Math.max(...lngs)

    // Add some padding
    const latPadding = (maxLat - minLat) * 0.1
    const lngPadding = (maxLng - minLng) * 0.1

    // Apply zoom factor
    const centerLat = (maxLat + minLat) / 2
    const centerLng = (maxLng + minLng) / 2

    const zoomedLatRange = (maxLat - minLat + latPadding * 2) / zoom
    const zoomedLngRange = (maxLng - minLng + lngPadding * 2) / zoom

    const zoomedMinLat = centerLat - zoomedLatRange / 2
    const zoomedMaxLat = centerLat + zoomedLatRange / 2
    const zoomedMinLng = centerLng - zoomedLngRange / 2
    const zoomedMaxLng = centerLng + zoomedLngRange / 2

    // Draw stations
    stations.forEach((station) => {
      // Convert lat/lng to x/y coordinates
      const x = ((station.location.longitude - zoomedMinLng) / (zoomedMaxLng - zoomedMinLng)) * width
      const y = height - ((station.location.latitude - zoomedMinLat) / (zoomedMaxLat - zoomedMinLat)) * height

      // Check if the station is within the visible area
      if (x >= 0 && x <= width && y >= 0 && y <= height) {
        // Draw station marker
        ctx.beginPath()

        // Make selected station marker larger
        const markerSize = station.id === selectedStation?.id ? 12 : 8
        ctx.arc(x, y, markerSize, 0, Math.PI * 2)

        // Different colors for different statuses
        if (station.status === "a") {
          ctx.fillStyle = "rgba(40, 167, 69, 0.7)"
        } else if (station.status === "m") {
          ctx.fillStyle = "rgba(255, 193, 7, 0.7)"
        } else {
          ctx.fillStyle = "rgba(220, 53, 69, 0.7)"
        }

        ctx.fill()

        // Add highlight for selected station
        if (station.id === selectedStation?.id) {
          ctx.beginPath()
          ctx.arc(x, y, markerSize + 5, 0, Math.PI * 2)
          ctx.strokeStyle = "rgba(58, 134, 255, 0.7)"
          ctx.lineWidth = 2
          ctx.stroke()

          // Pulsing effect for selected station
          ctx.beginPath()
          ctx.arc(x, y, markerSize + 10, 0, Math.PI * 2)
          ctx.strokeStyle = "rgba(58, 134, 255, 0.3)"
          ctx.stroke()
        }

        // Draw station name
        ctx.font = station.id === selectedStation?.id ? "bold 12px Arial" : "12px Arial"
        ctx.fillStyle = "#333"
        ctx.textAlign = "center"
        ctx.fillText(station.name, x, y - 15)
      }
    })

    // Add click handler to select station
    const handleCanvasClick = (event) => {
      const rect = mapRef.current.getBoundingClientRect()
      const clickX = event.clientX - rect.left
      const clickY = event.clientY - rect.top

      // Find if a station was clicked
      for (const station of stations) {
        const x = ((station.location.longitude- zoomedMinLng) / (zoomedMaxLng - zoomedMinLng)) * width
        const y = height - ((station.location.latitude- zoomedMinLat) / (zoomedMaxLat - zoomedMinLat)) * height

        // Check if click is within station marker
        const distance = Math.sqrt(Math.pow(clickX - x, 2) + Math.pow(clickY - y, 2))
        if (distance <= 15) {
          // Slightly larger than marker for better UX
          onSelectStation(station)
          break
        }
      }
    }

    // Add and remove event listener
    mapRef.current.addEventListener("click", handleCanvasClick)

    return () => {
      if (mapRef.current) {
        mapRef.current.removeEventListener("click", handleCanvasClick)
      }
    }
  }, [stations, selectedStation, zoom, onSelectStation])

  return (
    <div className="station-map-container">
      <canvas ref={mapRef} width={800} height={400} style={{ width: "100%", height: "100%" }}></canvas>

      <div className="map-legend">
        <div className="legend-item">
          <div className="legend-marker active"></div>
          <span>Active</span>
        </div>
        <div className="legend-item">
          <div className="legend-marker maintenance"></div>
          <span>Maintenance</span>
        </div>
        <div className="legend-item">
          <div className="legend-marker inactive"></div>
          <span>Inactive</span>
        </div>
      </div>

      <div className="map-disclaimer">
        <p>
          Note: This is a simplified map visualization. In a production environment, this would use the Google Maps API.
        </p>
      </div>

      <style jsx>{`
        .station-map-container {
          position: relative;
          height: 400px;
          border-radius: 8px;
          overflow: hidden;
          border: 1px solid var(--border-color);
        }
        
        .map-legend {
          position: absolute;
          top: 10px;
          left: 10px;
          background-color: rgba(255, 255, 255, 0.8);
          padding: 8px;
          border-radius: 4px;
          display: flex;
          flex-direction: column;
          gap: 5px;
          font-size: 0.8rem;
        }
        
        .legend-item {
          display: flex;
          align-items: center;
          gap: 5px;
        }
        
        .legend-marker {
          width: 12px;
          height: 12px;
          border-radius: 50%;
        }
        
        .legend-marker.active {
          background-color: rgba(40, 167, 69, 0.7);
        }
        
        .legend-marker.maintenance {
          background-color: rgba(255, 193, 7, 0.7);
        }
        
        .legend-marker.inactive {
          background-color: rgba(220, 53, 69, 0.7);
        }
        
        .map-disclaimer {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          background-color: rgba(0, 0, 0, 0.7);
          color: white;
          padding: 8px;
          font-size: 0.8rem;
          text-align: center;
        }
      `}</style>
    </div>
  )
}

export default StationMap

