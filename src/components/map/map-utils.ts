/* eslint-disable @typescript-eslint/no-explicit-any */

/**
 * Utility functions untuk komponen peta interaktif.
 */

/**
 * Menggeser seluruh koordinat longitude dalam GeoJSON sejauh offset yang ditentukan.
 * Digunakan untuk merender salinan peta di sebelah kiri dan kanan (world wrapping).
 */
export function getShiftedGeoJSON(geojsonData: any, offset: number) {
  if (offset === 0) return geojsonData;

  const clonedData = JSON.parse(JSON.stringify(geojsonData));

  clonedData.features.forEach((feature: any) => {
    if (feature.geometry.type === 'Polygon') {
      feature.geometry.coordinates.forEach((ring: any) => {
        ring.forEach((coord: any) => { coord[0] += offset; });
      });
    } else if (feature.geometry.type === 'MultiPolygon') {
      feature.geometry.coordinates.forEach((polygon: any) => {
        polygon.forEach((ring: any) => {
          ring.forEach((coord: any) => { coord[0] += offset; });
        });
      });
    }
  });

  return clonedData;
}

/** Offset longitude untuk merender 3 salinan bumi */
export const WORLD_COPIES = [-360, 0, 360] as const;
