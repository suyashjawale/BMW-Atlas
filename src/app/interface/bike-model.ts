import { BikeLocation } from "./bike-location";

export interface BikeModel {
  segment: string;
  modelCode: string;
  locations: BikeLocation[];
}