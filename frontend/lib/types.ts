export interface ImageResponse {
  expr: string;
  result: string | number;
  assign: boolean;
}

export interface CalculateResponse {
  message: string;
  data: ImageResponse[];
  status: string;
  success: boolean;
}

export interface GeneratedResult {
  expression: string;
  answer: string | number;
}
