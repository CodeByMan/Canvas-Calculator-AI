"use client";
import React from "react";
import { Button } from "../ui/button";
import { COLORS } from "@/lib/constants";
import { Loader2Icon, RedoIcon, UndoIcon } from "lucide-react";

interface TopbarProps {
  setColor: (color: string) => void;
  color: string;
  resetCanvas: () => void;
  getResults: () => void;
  performUndo: () => void;
  performRedo: () => void;
  isPending: boolean;
}

export const Topbar: React.FC<TopbarProps> = ({
  color,
  setColor,
  resetCanvas,
  getResults,
  performUndo,
  performRedo,
  isPending,
}) => {
  return (
    <div className="z-10 flex max-md:flex-col max-md:py-4 items-center justify-between gap-2 sm:px-10 px-2 h-[80px] bg-black">
      {/* Operations */}
      <div className="flex items-center gap-2">
        <Button
          className="md:hidden sm:px-10 px-5 bg-green-600 hover:bg-green-700"
          onClick={getResults}
          disabled={isPending}
        >
          Run
        </Button>
        <Button
          className="sm:px-10 px-5 bg-red-500 hover:bg-red-600"
          onClick={resetCanvas}
        >
          Reset
        </Button>
        <Button className="" onClick={performUndo} aria-label="Undo last stroke">
          <UndoIcon size={14} />
        </Button>
        <Button className="" onClick={performRedo} aria-label="Redo last stroke">
          <RedoIcon size={14} />
        </Button>
      </div>
      {/* Color bar to select the color */}
      <div className="flex items-center justify-center gap-2 max-sm:overflow-x-scroll min-h-[50px] w-full">
        {COLORS.map((c) => (
          <button
            key={c}
            onClick={() => setColor(c)}
            aria-label={`Select ${c} drawing color`}
            aria-pressed={color === c}
            className={`w-8 h-8 rounded-full transition-all border-2 border-gray-600 ${
              color === c
                ? "border-white border-4 scale-105"
                : "hover:scale-105"
            }`}
            style={{ backgroundColor: c }}
          />
        ))}
      </div>
      {/* Run Button */}
      <Button
        className="max-md:hidden px-10 bg-green-600 hover:bg-green-700"
        onClick={getResults}
        disabled={isPending}
      >
        {isPending ? <Loader2Icon className="animate-spin w-4 h-4" /> : "Run"}
      </Button>
    </div>
  );
};
