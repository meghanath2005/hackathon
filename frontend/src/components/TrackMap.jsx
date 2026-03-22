import { MapContainer, Marker, Polyline, TileLayer, Tooltip } from 'react-leaflet';

const colors = {
  actual: '#22d3ee',
  classical: '#f59e0b',
  hybrid: '#34d399',
};

export default function TrackMap({ actual = [], classical = [], hybrid = [] }) {
  const center = actual[0] ? [actual[0].lat, actual[0].lon] : [15, 85];
  return (
    <MapContainer center={center} zoom={5} className="h-[420px] w-full rounded-xl">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {actual.length > 0 && <Polyline positions={actual.map((p) => [p.lat, p.lon])} color={colors.actual} />}
      {classical.length > 0 && <Polyline positions={classical.map((p) => [p.lat, p.lon])} color={colors.classical} />}
      {hybrid.length > 0 && <Polyline positions={hybrid.map((p) => [p.lat, p.lon])} color={colors.hybrid} />}
      {actual.at(-1) && (
        <Marker position={[actual.at(-1).lat, actual.at(-1).lon]}>
          <Tooltip>Observed track endpoint</Tooltip>
        </Marker>
      )}
    </MapContainer>
  );
}
