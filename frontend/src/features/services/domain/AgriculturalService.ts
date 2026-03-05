export interface AgriculturalService {
  id: string;
  name: string;
  description: string;
  unit: "Hora" | "Hectare" | "Empreitada";
  basePrice: number;
  active: boolean;
  is_deleted: boolean;
}
