import { BikeModel } from "./bike-model";

export interface BikeDataMap {
  [modelName: string]: BikeModel;
}