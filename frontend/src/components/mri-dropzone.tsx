"use client";

import { useCallback, useRef, useState } from "react";
import { ScanLine, UploadCloud, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface MriDropzoneProps {
  file: File | null;
  onChange: (file: File | null) => void;
  isScanning?: boolean;
}

const ACCEPTED = [".nii", ".nii.gz", ".dcm", ".png", ".jpg", ".jpeg"];

export function MriDropzone({ file, onChange, isScanning }: MriDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFiles = useCallback(
    (files: FileList | null) => {
      const next = files?.[0] ?? null;
      onChange(next);
      if (next && next.type.startsWith("image/")) {
        setPreviewUrl(URL.createObjectURL(next));
      } else {
        setPreviewUrl(null);
      }
    },
    [onChange]
  );

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setIsDragging(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "relative flex h-56 w-full cursor-pointer flex-col items-center justify-center overflow-hidden rounded-md border border-dashed transition-colors",
          isDragging ? "border-indigo bg-indigo-soft" : "border-line hover:border-text-faint",
          file && "border-solid border-line"
        )}
      >
        {previewUrl ? (
          <img
            src={previewUrl}
            alt="MRI preview"
            className="absolute inset-0 h-full w-full object-contain bg-black grayscale contrast-125"
          />
        ) : file ? (
          <div className="flex flex-col items-center gap-2 text-text-muted">
            <ScanLine className="h-8 w-8" />
            <p className="font-mono text-sm">{file.name}</p>
            <p className="text-xs text-text-faint">
              {(file.size / 1024 / 1024).toFixed(1)} MB
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2 text-text-muted">
            <UploadCloud className="h-8 w-8" />
            <p className="text-sm">Drop an MRI series, or click to browse</p>
            <p className="text-xs text-text-faint">
              Accepts {ACCEPTED.join(", ")}
            </p>
          </div>
        )}

        {(isScanning || (file && !previewUrl)) && (
          <div className="pointer-events-none absolute inset-0">
            <div className="absolute inset-x-0 h-1/3 bg-gradient-to-b from-transparent via-teal/10 to-transparent animate-scan" />
          </div>
        )}

        {file && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onChange(null);
              setPreviewUrl(null);
            }}
            className="absolute right-2 top-2 rounded-sm bg-ink/80 p-1 text-text-muted hover:text-amber"
            aria-label="Remove file"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED.join(",")}
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
  );
}
